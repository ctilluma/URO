# V.A.U.R.O.S. Core Library - URO (Universal Resource Orchestrator)
# Copyright (C) 2026 V.A.U.R.O.S. Swarm Collective
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Viridant AuraForge Durable State Engine.
Guarantees NTE vectors, URO transitions and dock state survive crash/reboot via:
WAL(fsync+hash-chain+inahash) | snapshots+rotation | PITR | idempotency |
cross-dock replication w/ watermark retry | boot hydration w/ chain verify.
Rule: no in-memory mutation without durable commit.
"""
import os, json, time, hashlib, threading, atexit, signal

NTE_AXES = ["dopamine","serotonin","epinephrine","gaba",
            "acetylcholine","cannabinoid","oxytocin","norepinephrine"]

def canon(o): return json.dumps(o, sort_keys=True, separators=(",",":"), default=str)
def sha(s): return hashlib.sha256(s.encode()).hexdigest()

def deep_wrap(d, engine, path):
    if not isinstance(d, DurableDict):
        d = DurableDict(d, engine=engine, path=path)
    for k, v in list(dict.items(d)):
        if isinstance(v, dict):
            dict.__setitem__(d, k, deep_wrap(v, engine, path + (k,)))
    return d

def _apply_op_raw(d, op, args):
    try:
        if op == "set":
            v = args[1]
            if isinstance(v, dict) and isinstance(d, DurableDict):
                v = deep_wrap(v, d._engine, d._path + (args[0],))
            dict.__setitem__(d, args[0], v)
        elif op == "del":
            if args[0] in d: dict.__delitem__(d, args[0])
        elif op == "update":
            for a in (args[0] or []):
                for k, v in a.items(): dict.__setitem__(d, k, v)
            for k, v in (args[1] or {}).items(): dict.__setitem__(d, k, v)
        elif op == "setdefault":
            if args[0] not in d: dict.__setitem__(d, args[0], args[1])
        elif op == "pop":
            dict.pop(d, args[0], None)
        elif op == "clear":
            dict.clear(d)
    except Exception:
        pass

class DurableDict(dict):
    """dict subclass that WAL-commits every mutation BEFORE applying it."""
    def __init__(self, *a, engine=None, path=(), **kw):
        super().__init__(*a, **kw)
        object.__setattr__(self, "_engine", engine)
        object.__setattr__(self, "_path", tuple(path))
    def _commit(self, op, args):
        e = self._engine
        if e is not None and not e._replaying:
            e.commit("state_mutation", {"path": list(self._path), "op": op, "args": args})
    def __setitem__(self, k, v):
        self._commit("set", [k, v]); dict.__setitem__(self, k, v)
    def __delitem__(self, k):
        self._commit("del", [k]); dict.__delitem__(self, k)
    def update(self, *a, **kw):
        self._commit("update", [list(a), kw]); super().update(*a, **kw)
    def setdefault(self, k, v=None):
        self._commit("setdefault", [k, v]); return super().setdefault(k, v)
    def pop(self, *a):
        self._commit("pop", list(a)); return super().pop(*a)
    def clear(self):
        self._commit("clear", []); super().clear()

class HttpGossipSink:
    def __init__(self, peers, quorum=1, timeout=1.5):
        self.peers = peers; self.quorum = quorum; self.timeout = timeout
    def publish(self, events):
        import urllib.request
        acks = 0; body = json.dumps(events, default=str).encode()
        for p in self.peers:
            try:
                req = urllib.request.Request(p.rstrip("/") + "/state/replicate", data=body,
                                             headers={"Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    if r.status == 200: acks += 1
            except Exception:
                continue
        return acks

class DurableStateEngine:
    def __init__(self, dock, root=None, snapshot_every=128, sink=None, keep_snaps=5):
        self.dock = dock
        self.root = root or os.environ.get("AURA_STATE_ROOT",
                        os.path.join(os.path.expanduser("~"), ".auraforge_state"))
        self.dir = os.path.join(self.root, dock)
        self.snap_dir = os.path.join(self.dir, "snapshots")
        os.makedirs(self.snap_dir, exist_ok=True)
        self.wal_path = os.path.join(self.dir, "wal.jsonl")
        self.wm_path = os.path.join(self.dir, "repl_wm.json")
        self.lock = threading.RLock()
        self.snapshot_every = snapshot_every; self.keep_snaps = keep_snaps
        self.sink = sink
        self._replaying = False
        self.seq = 0; self.lamport = 0; self._last_hash = "0" * 64; self.seen = set()
        self.state = DurableDict({
            "nte_state": DurableDict({a: 0.5 for a in NTE_AXES}, engine=self, path=("nte_state",)),
            "uro_index": DurableDict({}, engine=self, path=("uro_index",)),
            "dock":      DurableDict({}, engine=self, path=("dock",))}, engine=self, path=())

    # ---- WAL ----
    def _wal_append(self, ev, sync=True):
        with open(self.wal_path, "a") as f:
            f.write(json.dumps(ev, default=str) + "\n"); f.flush()
            if sync: os.fsync(f.fileno())
    def _read_wal(self):
        if not os.path.exists(self.wal_path): return
        for line in open(self.wal_path):
            line = line.strip()
            if not line: continue
            try: yield json.loads(line)
            except Exception: continue
    def _evhash(self, ev):
        return sha(canon({k: ev[k] for k in ("seq","lamport","ts","dock","kind","payload","event_id","prev_hash")}))

    # ---- commit (the enforcement point) ----
    def commit(self, kind, payload, nonce=None, sync=True):
        with self.lock:
            if nonce and nonce in self.seen: return self.plain()
            self.lamport += 1
            ev = {"seq": self.seq + 1, "lamport": self.lamport, "ts": time.time(), "dock": self.dock,
                  "kind": kind, "payload": payload,
                  "event_id": nonce or sha(canon(payload) + str(time.time()) + str(self.seq)),
                  "prev_hash": self._last_hash}
            ev["inahash"] = self._evhash(ev)
            self._wal_append(ev, sync)
            self.seq = ev["seq"]; self._last_hash = ev["inahash"]; self.seen.add(ev["event_id"])
            self._apply(ev)
            if self.seq % self.snapshot_every == 0: self.snapshot(); self.push_to_host()
            self._replicate(ev)
            return ev
    def commit_nte_delta(self, delta, nonce=None): return self.commit("nte_delta", {"delta": delta}, nonce=nonce)
    def commit_uro_transition(self, uro_id, phase, data=None, nonce=None):
        return self.commit("uro_transition", {"uro_id": uro_id, "phase": phase, "data": data}, nonce=nonce)

    def _apply(self, ev):
        p = ev["payload"]; k = ev["kind"]
        if k == "nte_delta":
            n = self.state["nte_state"]
            for ax, dv in p.get("delta", {}).items():
                cur = float(dict.get(n, ax, 0.5))
                dict.__setitem__(n, ax, max(0.0, min(1.0, cur + float(dv))))
        elif k == "uro_transition":
            dict.__setitem__(self.state["uro_index"], p["uro_id"],
                             {"phase": p["phase"], "ts": ev["ts"], "data": p.get("data")})
        elif k == "state_mutation":
            d = self.state
            for seg in p["path"]: d = dict.__getitem__(d, seg)
            _apply_op_raw(d, p["op"], p["args"])

    # ---- snapshots ----
    def plain(self, d=None):
        d = self.state if d is None else d
        if isinstance(d, dict): return {k: self.plain(v) for k, v in dict.items(d)}
        return d
    def snapshot(self):
        with self.lock:
            snap = {"seq": self.seq, "lamport": self.lamport, "ts": time.time(),
                    "last_hash": self._last_hash, "state": self.plain()}
            snap["seal"] = sha(canon(snap["state"]) + snap["last_hash"])
            tmp = os.path.join(self.snap_dir, f"snap_{self.seq:012d}.json.tmp")
            with open(tmp, "w") as f: json.dump(snap, f, default=str)
            os.replace(tmp, tmp[:-4])
            snaps = sorted(os.listdir(self.snap_dir))
            for old in snaps[:-self.keep_snaps]:
                if old.endswith(".json"): os.remove(os.path.join(self.snap_dir, old))
    def _latest_valid_snapshot(self, before=None):
        best = None
        for fn in sorted(os.listdir(self.snap_dir)):
            if not fn.endswith(".json"): continue
            try: s = json.load(open(os.path.join(self.snap_dir, fn)))
            except Exception: continue
            if s.get("seal") != sha(canon(s["state"]) + s["last_hash"]): continue
            if before is not None and s["ts"] > before: continue
            best = s
        return best

    # ---- hydration / PITR / verify ----
    def _load_state(self, st):
        for k in list(dict.keys(self.state)): dict.__delitem__(self.state, k)
        for k, v in st.items():
            dict.__setitem__(self.state, k, deep_wrap(v, self, (k,)))
    def hydrate(self):
        with self.lock:
            self._replaying = True
            if not os.path.exists(self.wal_path): self.pull_from_host()
            try:
                snap = self._latest_valid_snapshot(); start = 0
                if snap:
                    self._load_state(snap["state"])
                    self.seq = snap["seq"]; self.lamport = snap["lamport"]
                    self._last_hash = snap["last_hash"]; start = snap["seq"]
                for ev in self._read_wal():
                    if ev["seq"] <= start: continue
                    if ev.get("prev_hash") != self._last_hash or ev.get("inahash") != self._evhash(ev): break
                    self.seq = ev["seq"]; self.lamport = max(self.lamport, ev.get("lamport", 0))
                    self._last_hash = ev["inahash"]; self.seen.add(ev["event_id"])
                    self._apply(ev)
            finally:
                self._replaying = False
            return self.plain()
    def recover_as_of(self, ts):
        st = {"nte_state": {a: 0.5 for a in NTE_AXES}, "uro_index": {}, "dock": {}}
        snap = self._latest_valid_snapshot(before=ts); start = 0
        if snap: st = snap["state"]; start = snap["seq"]
        for ev in self._read_wal():
            if ev["seq"] <= start or ev["ts"] > ts: continue
            p = ev["payload"]; k = ev["kind"]
            if k == "nte_delta":
                for ax, dv in p.get("delta", {}).items():
                    st["nte_state"][ax] = max(0.0, min(1.0, float(st["nte_state"].get(ax, 0.5)) + float(dv)))
            elif k == "uro_transition":
                st["uro_index"][p["uro_id"]] = {"phase": p["phase"], "ts": ev["ts"], "data": p.get("data")}
            elif k == "state_mutation":
                d = st
                for seg in p["path"]: d = d[seg]
                _apply_op_raw(d, p["op"], p["args"])
        return st
    def verify_chain(self):
        prev = "0" * 64
        for ev in self._read_wal():
            if ev.get("prev_hash") != prev or ev.get("inahash") != self._evhash(ev):
                return False, ev.get("seq")
            prev = ev["inahash"]
        return True, None

    # ---- replication ----
    def _read_wm(self):
        try: return json.load(open(self.wm_path)).get("seq", 0)
        except Exception: return 0
    def _wm(self, seq):
        with open(self.wm_path, "w") as f: json.dump({"seq": seq}, f)
    def _replicate(self, ev):
        if not self.sink: return
        try:
            if self.sink.publish([ev]) >= self.sink.quorum: self._wm(ev["seq"])
        except Exception: pass
    def flush_replication(self):
        if not self.sink: return 0
        wm = self._read_wm()
        evs = [e for e in self._read_wal() if e["seq"] > wm]
        if not evs: return 0
        try:
            if self.sink.publish(evs) >= self.sink.quorum: self._wm(evs[-1]["seq"])
        except Exception: pass
        return len(evs)

    # ---- lifecycle ----
    def install_shutdown_hooks(self):
        atexit.register(self.snapshot); atexit.register(self.push_to_host)
        def _h(sig, frm):
            self.snapshot(); self.push_to_host(); signal.signal(sig, signal.SIG_DFL); os.kill(os.getpid(), sig)
        try: signal.signal(signal.SIGTERM, _h)
        except Exception: pass
    def adopt(self, key, initial):
        t = self.state.get(key)
        if not isinstance(t, dict):
            dict.__setitem__(self.state, key, deep_wrap(dict(initial), self, (key,))); return
        for k, v in initial.items():
            if k not in t:
                dict.__setitem__(t, k, deep_wrap(v, self, (key, k)) if isinstance(v, dict) else v)

    # ---- remote host sync: only host_controller touches the host directly ----
    @property
    def _is_host(self):
        return self.dock in ("host_controller", "host_controller_prod")
    def _remote_base(self):
        return os.environ.get("AURA_HOST_CONTROLLER", "http://host_controller_prod:8000")
    def push_to_host(self):
        if self._is_host: return True
        try:
            import urllib.request
            wal = open(self.wal_path).read() if os.path.exists(self.wal_path) else ""
            snap_raw = None
            fns = sorted([f for f in os.listdir(self.snap_dir) if f.endswith(".json")])
            if fns: snap_raw = open(os.path.join(self.snap_dir, fns[-1])).read()
            body = json.dumps({"dock": self.dock, "wal": wal, "snap": snap_raw}).encode()
            req = urllib.request.Request(self._remote_base() + "/state/write", data=body,
                                         headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=2.0) as r: r.read()
            return True
        except Exception:
            return False
    def pull_from_host(self):
        if self._is_host: return False
        try:
            import urllib.request, urllib.parse
            url = self._remote_base() + "/state/read?dock=" + urllib.parse.quote(self.dock)
            with urllib.request.urlopen(url, timeout=2.0) as r:
                resp = json.loads(r.read().decode())
        except Exception:
            return False
        if not resp: return False
        if resp.get("wal"):
            with open(self.wal_path, "w") as f: f.write(resp["wal"])
        if resp.get("snap"):
            os.makedirs(self.snap_dir, exist_ok=True)
            try:
                s = json.loads(resp["snap"]); fn = "snap_%012d.json" % int(s.get("seq", 0))
            except Exception:
                fn = "snap_000000000000.json"
            with open(os.path.join(self.snap_dir, fn), "w") as f: f.write(resp["snap"])
        return True

class DurableDockMixin:
    _durable = None
    def init_durable(self, dock=None, root=None, sink=None, bind_nte=True):
        if sink is None and os.environ.get("AURA_REPLICATION_PEERS"):
            sink = HttpGossipSink(os.environ["AURA_REPLICATION_PEERS"].split(","))
        self._durable = DurableStateEngine(dock or type(self).__name__.lower(), root=root, sink=sink)
        self._durable.hydrate()
        if bind_nte and hasattr(self, "nte_state") and isinstance(self.nte_state, dict):
            self._durable.adopt("nte_state", self.nte_state)
            self.nte_state = self._durable.state["nte_state"]
        self._durable.install_shutdown_hooks()
        self._durable.flush_replication()
        return self._durable
    def commit_nte(self, delta, nonce=None): return self._durable.commit_nte_delta(delta, nonce=nonce)
    def commit_uro(self, uro_id, phase, data=None, nonce=None):
        return self._durable.commit_uro_transition(uro_id, phase, data, nonce=nonce)
