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


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ledger.py — URO Pipeline Chain-of-Custody Ledger.

Tracks a single URO end-to-end through the coding pipeline and records a
cryptographically chained, INAHASH-signed seal at every stage:

    intake(CI/CD) -> architect -> refinery -> coder -> codereview
                  -> sast -> dast -> iast -> host_controller(write)

# === START: capabilities ===
* Tamper-evident custody chain (S7.8): seal_n hashes seal_{n-1}.
* INAHASH sealing (S7.2): Blake3-1024(SHA3-1024(MSG)); prefers the canonical
  swarm implementation and only falls back to a documented stdlib equivalent.
* Per-dock keyed signatures: every pipeline member signs its own seal, so an
  approval/denial is attributable and independently verifiable.
* URID pair identity (S2) and Time URO (S10.5, InSPa epoch) on every record.
* Optional 24-axis NTE snapshot (S4) captured with each decision.
* Gate enforcement: a stage records a gate warning if its prerequisites were
  not APPROVED; `can_deploy()` is the hard gate host_controller must consult
  before writing.
* Journey reporting: markdown + JSON, per-stage latency, denials, gaps.
* Dual persistence: append-only local ledger (always works) plus best-effort
  remote push to the lineage/coordinator dock (never fatal).
# === END: capabilities ===

Library use (3 lines in any dock):
    from uro.pipeline.ledger import seal_stage, can_deploy
    seal_stage(tracking_id, dock="sast", stage="sast",
               decision="APPROVED", artifact_file="/path/x.py", notes="clean")
    ok, reasons = can_deploy(tracking_id)
"""
# === START: imports ===
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
# === END: imports ===

# === START: constants ===
VERSION = "1.0.0"

INSPA_EPOCH = _dt.datetime(1973, 5, 14, 0, 12, 24, tzinfo=_dt.timezone.utc)

# Canonical pipeline order. `requires` = stages whose LATEST decision must be
# APPROVED/WARNING before this stage may deploy-gate cleanly.
STAGE_SPEC: Dict[str, Dict[str, Any]] = {
    "intake":          {"order": 1, "requires": [],             "role": "CI/CD trigger / request intake"},
    "architect":       {"order": 2, "requires": ["intake"],     "role": "design + capability approval"},
    "refinery":        {"order": 3, "requires": ["architect"],  "role": "compliance analysis + proposal"},
    "coder":           {"order": 4, "requires": ["refinery"],   "role": "implementation"},
    "codereview":      {"order": 5, "requires": ["coder"],      "role": "review approval/denial"},
    "sast":            {"order": 6, "requires": ["codereview"], "role": "static application security testing"},
    "dast":            {"order": 7, "requires": ["sast"],       "role": "dynamic application security testing"},
    "iast":            {"order": 8, "requires": ["dast"],       "role": "interactive application security testing"},
    "host_controller": {"order": 9, "requires": ["iast"],       "role": "authorised write / deployment"},
}
PIPELINE_ORDER: List[str] = sorted(STAGE_SPEC, key=lambda s: STAGE_SPEC[s]["order"])

# Hard gates: these MUST be APPROVED/WARNING before host_controller may write.
DEPLOY_GATES = ["architect", "coder", "codereview", "sast"]

DECISIONS = {"APPROVED", "DENIED", "DEFERRED", "WARNING", "SKIPPED"}
PASSING = {"APPROVED", "WARNING"}

SIG_SCHEME = "inahash-keyed-v1"
GENESIS = "0" * 128
# === END: constants ===

# === START: inahash ===
_CANON: Tuple[Any, str] = (None, "")


def _load_canonical_inahash() -> Tuple[Any, str]:
    """Prefer the swarm's canonical INAHASH (S14.7: do not re-implement)."""
    global _CANON
    if _CANON[0] is not None:
        return _CANON
    candidates = [
        ("uro.licm.hashutil", "inahash"),
        ("uro.security.inahash", "inahash"),
        ("uro.security.inahash", "compute_inahash"),
        ("uro.crypto.inahash", "inahash"),
    ]
    for mod_name, fn_name in candidates:
        try:
            mod = __import__(mod_name, fromlist=[fn_name])
            fn = getattr(mod, fn_name, None)
            if callable(fn):
                probe = fn(b"vauros-probe")
                hx = _coerce_hex(probe)
                if hx and len(hx) >= 64:
                    _CANON = (fn, f"canonical:{mod_name}.{fn_name}")
                    return _CANON
        except Exception:
            continue
    _CANON = (None, "")
    return _CANON


def _coerce_hex(out: Any) -> Optional[str]:
    """Normalise any hash-return shape to lowercase hex."""
    try:
        if hasattr(out, "hexdigest"):
            return str(out.hexdigest()).lower()
        if isinstance(out, (bytes, bytearray)):
            return out.hex().lower()
        s = str(out).strip().lower()
        if len(s) >= 32 and all(c in "0123456789abcdef" for c in s):
            return s
    except Exception:
        pass
    return None


def _local_inahash(raw: bytes) -> str:
    """Documented stdlib fallback honouring the S7.2 dual-standard, 1024-bit shape.

    inner = SHA3-512(MSG) || SHA512(MSG)            (1024 bits, dual standard)
    outer = Blake3-1024(inner) if blake3 available, else Blake2b-512||SHA3-512
    """
    inner = hashlib.sha3_512(raw).digest() + hashlib.sha512(raw).digest()
    try:
        import blake3  # type: ignore
        return blake3.blake3(inner, digest_size=64).hexdigest()
    except Exception:
        pass
    try:
        return (hashlib.blake2b(inner, digest_size=64).hexdigest()
                + hashlib.sha3_512(inner).hexdigest())
    except Exception:
        return hashlib.sha3_512(inner).hexdigest() * 2


def inahash(data: Any) -> str:
    """INAHASH (S7.2). Returns lowercase hex. Never raises."""
    if isinstance(data, (bytes, bytearray)):
        raw = bytes(data)
    elif isinstance(data, Path):
        try:
            raw = data.read_bytes()
        except Exception:
            raw = str(data).encode()
    else:
        raw = str(data).encode("utf-8", "replace")

    fn, _src = _load_canonical_inahash()
    if fn is not None:
        for attempt in (raw, raw.decode("utf-8", "replace")):
            try:
                hx = _coerce_hex(fn(attempt))
                if hx and len(hx) >= 64:
                    return hx
            except Exception:
                continue
    return _local_inahash(raw)


def inahash_scheme() -> str:
    """Which INAHASH implementation is active (for audit honesty)."""
    _fn, src = _load_canonical_inahash()
    return src or "fallback:blake3|blake2b-sha3-1024-local"


def inahash_file(path: Any) -> str:
    """INAHASH of a file's bytes; falls back to hashing the path string."""
    p = Path(path)
    try:
        return inahash(p.read_bytes())
    except Exception:
        return inahash(f"missing:{p}")
# === END: inahash ===

# === START: helpers ===
def _canon_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def time_uro(when: Optional[_dt.datetime] = None) -> Dict[str, Any]:
    """Time URO per S10.5 — seconds relative to the InSPa epoch."""
    when = when or _dt.datetime.now(_dt.timezone.utc)
    return {
        "type": "TIME",
        "value": round((when - INSPA_EPOCH).total_seconds(), 6),
        "unit": "seconds",
        "epoch": "1973-05-14T00:12:24Z",
        "iso": when.isoformat(),
    }


def _detect_swarm() -> Path:
    env = os.environ.get("SWARM_ROOT")
    if env and Path(env).is_dir():
        return Path(env)
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "docks").is_dir() and (parent / "uro").is_dir():
            return parent
    return Path.home() / "viridant-auraforge"


def _resolve_state_root() -> Path:
    """Pick the first WRITABLE ledger root (containers and host both work)."""
    swarm = _detect_swarm()
    env = os.environ.get("PIPELINE_STATE_ROOT")
    cands: List[Path] = []
    if env:
        cands.append(Path(env))
    sr = os.environ.get("STATE_ROOT", "/opt/uro_state")
    cands += [
        Path(sr) / "pipeline_ledger",
        swarm / "docks" / "shared" / "persistence" / "pipeline_ledger",
        Path.home() / ".vauros" / "pipeline_ledger",
        Path("/tmp/vauros_pipeline_ledger"),
    ]
    for c in cands:
        try:
            c.mkdir(parents=True, exist_ok=True)
            probe = c / ".write_probe"
            probe.write_text("ok")
            probe.unlink()
            return c
        except Exception:
            continue
    return Path("/tmp/vauros_pipeline_ledger")


STATE_ROOT = _resolve_state_root()
LEDGER_DIR = STATE_ROOT
KEY_DIR = STATE_ROOT / "keys"
INDEX_FILE = LEDGER_DIR / "_index.json"


def _ensure_dirs() -> None:
    try:
        LEDGER_DIR.mkdir(parents=True, exist_ok=True)
        KEY_DIR.mkdir(parents=True, exist_ok=True)
        os.chmod(KEY_DIR, 0o700)
    except Exception:
        pass


def dock_key(dock: str) -> str:
    """Per-dock signing key. Persisted 0600 so seals are attributable."""
    _ensure_dirs()
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in dock)
    kf = KEY_DIR / f"{safe}.key"
    try:
        if kf.exists():
            k = kf.read_text().strip()
            if k:
                return k
        import secrets
        k = secrets.token_hex(64)
        kf.write_text(k)
        try:
            os.chmod(kf, 0o600)
        except Exception:
            pass
        return k
    except Exception:
        return "ephemeral-" + hashlib.sha256(dock.encode()).hexdigest()


def sign(dock: str, seal_hash: str) -> str:
    """Keyed INAHASH signature over a seal hash (S7.6/S7.8 attributable seal)."""
    return inahash(f"{SIG_SCHEME}|{dock}|{seal_hash}|{dock_key(dock)}")


def verify_signature(dock: str, seal_hash: str, signature: str) -> bool:
    try:
        return sign(dock, seal_hash) == str(signature).lower()
    except Exception:
        return False


def ledger_path(tracking_id: str) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in tracking_id)
    return LEDGER_DIR / f"{safe}.jsonl"


def _read_index() -> Dict[str, Any]:
    try:
        return json.loads(INDEX_FILE.read_text()) if INDEX_FILE.exists() else {}
    except Exception:
        return {}


def _write_index(idx: Dict[str, Any]) -> None:
    _ensure_dirs()
    try:
        INDEX_FILE.write_text(_canon_json(idx))
    except Exception:
        pass


def _append_seal(tracking_id: str, seal: Dict[str, Any]) -> bool:
    _ensure_dirs()
    try:
        with open(ledger_path(tracking_id), "a", encoding="utf-8") as fh:
            fh.write(_canon_json(seal) + "\n")
        return True
    except Exception:
        return False


def read_seals(tracking_id: str) -> List[Dict[str, Any]]:
    p = ledger_path(tracking_id)
    out: List[Dict[str, Any]] = []
    if not p.exists():
        return out
    for line in p.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out
# === END: helpers ===

# === START: passport ===
def open_passport(tracking_id: Optional[str] = None,
                  urid1: str = "", urid2: str = "",
                  title: str = "", origin: str = "ci_cd",
                  artifact_ref: str = "", meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create (or return existing) pipeline passport for one URO."""
    tid = tracking_id or f"URO-PL-{time.strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    existing = get_passport(tid)
    if existing:
        return existing

    passport = {
        "schema": "uro.pipeline.passport",
        "version": VERSION,
        "tracking_id": tid,
        "urid_pair": [urid1 or origin, urid2 or tid],
        "title": title or artifact_ref or tid,
        "origin": origin,
        "artifact_ref": artifact_ref,
        "meta": meta or {},
        "opened": time_uro(),
        "inahash_scheme": inahash_scheme(),
        "sig_scheme": SIG_SCHEME,
        "genesis": GENESIS,
    }
    _ensure_dirs()
    try:
        (LEDGER_DIR / f"{tid}.passport.json").write_text(_canon_json(passport))
    except Exception:
        pass

    idx = _read_index()
    idx[tid] = {"opened": passport["opened"]["iso"], "title": passport["title"],
                "origin": origin, "status": "active", "seals": 0}
    _write_index(idx)
    return passport


def get_passport(tracking_id: str) -> Optional[Dict[str, Any]]:
    p = LEDGER_DIR / f"{tracking_id}.passport.json"
    try:
        return json.loads(p.read_text()) if p.exists() else None
    except Exception:
        return None


def list_passports(status: Optional[str] = None) -> List[Dict[str, Any]]:
    idx = _read_index()
    rows = []
    for tid, m in idx.items():
        if status and m.get("status") != status:
            continue
        rows.append({"tracking_id": tid, **m})
    rows.sort(key=lambda r: r.get("opened", ""), reverse=True)
    return rows
# === END: passport ===

# === START: sealing ===
def seal_stage(tracking_id: str,
               dock: str,
               stage: str,
               decision: str,
               artifact_file: Optional[str] = None,
               artifact_sha: Optional[str] = None,
               artifact_ref: Optional[str] = None,
               reviewer: Optional[str] = None,
               notes: str = "",
               evidence: Optional[Dict[str, Any]] = None,
               nte: Optional[Dict[str, Any]] = None,
               urid1: str = "", urid2: str = "",
               push_remote: bool = True) -> Dict[str, Any]:
    """Append an INAHASH-signed seal for one pipeline stage.

    Returns the seal dict (includes seal_hash, signature, gate_warnings).
    Never raises: on failure returns a seal with status='error'.
    """
    try:
        stage = (stage or "").strip().lower()
        decision = (decision or "").strip().upper()
        if decision not in DECISIONS:
            decision = "DEFERRED"

        seals = read_seals(tracking_id)
        prev_hash = seals[-1]["seal_hash"] if seals else GENESIS
        prev_stage = seals[-1].get("stage") if seals else None

        if artifact_sha:
            a_sha = str(artifact_sha).lower()
        elif artifact_file:
            a_sha = inahash_file(artifact_file)
        else:
            a_sha = inahash(artifact_ref or tracking_id)

        # ---- gate evaluation (S7.8 order + DEPLOY_GATES) -------------------
        latest = latest_decisions(seals)
        gate_warnings: List[str] = []
        spec = STAGE_SPEC.get(stage)
        if spec is None:
            gate_warnings.append(f"unknown_stage:{stage}")
        else:
            for req in spec["requires"]:
                d = latest.get(req)
                if d is None:
                    gate_warnings.append(f"missing_prereq:{req}")
                elif d not in PASSING:
                    gate_warnings.append(f"prereq_not_passed:{req}={d}")
            if prev_stage and prev_stage in STAGE_SPEC and stage in STAGE_SPEC:
                if STAGE_SPEC[stage]["order"] < STAGE_SPEC[prev_stage]["order"]:
                    gate_warnings.append(f"out_of_order:{prev_stage}->{stage}")

        payload = {
            "schema": "uro.pipeline.seal",
            "version": VERSION,
            "tracking_id": tracking_id,
            "seal_index": len(seals),
            "dock": dock,
            "stage": stage,
            "decision": decision,
            "reviewer": reviewer or f"{dock}@{os.environ.get('AURA_ENV','prod')}",
            "artifact_sha": a_sha,
            "artifact_ref": artifact_ref or artifact_file or "",
            "notes": notes or "",
            "evidence": evidence or {},
            "nte": nte or {},
            "urid_pair": [urid1 or dock, urid2 or tracking_id],
            "gate_warnings": gate_warnings,
            "time_uro": time_uro(),
            "inahash_scheme": inahash_scheme(),
            "sig_scheme": SIG_SCHEME,
        }
        payload["prev_hash"] = prev_hash
        payload["seal_hash"] = inahash(_canon_json(payload) + "|" + prev_hash)
        payload["signature"] = sign(dock, payload["seal_hash"])

        ok = _append_seal(tracking_id, payload)
        payload["persisted"] = ok

        idx = _read_index()
        ent = idx.get(tracking_id, {"opened": payload["time_uro"]["iso"],
                                    "title": tracking_id, "origin": "unknown"})
        ent["seals"] = len(seals) + 1
        ent["last_stage"] = stage
        ent["last_decision"] = decision
        ent["last_at"] = payload["time_uro"]["iso"]
        ent["status"] = ("denied" if decision == "DENIED"
                         else "deployed" if stage == "host_controller" and decision in PASSING
                         else "active")
        idx[tracking_id] = ent
        _write_index(idx)

        if push_remote:
            _push_remote(tracking_id, payload)
        return payload
    except Exception as exc:  # pragma: no cover - defensive
        return {"schema": "uro.pipeline.seal", "tracking_id": tracking_id,
                "stage": stage, "dock": dock, "decision": "DEFERRED",
                "status": "error", "error": str(exc)[:300],
                "seal_hash": "", "signature": "", "time_uro": time_uro()}


def _push_remote(tracking_id: str, seal: Dict[str, Any]) -> None:
    """Best-effort push to lineage/coordinator. NEVER fatal (transport lesson)."""
    if os.environ.get("PIPELINE_REMOTE_PUSH", "1") == "0":
        return
    targets = []
    for host in ("lineage_prod", "lineage", "coordinator_prod", "coordinator"):
        for port in (8000, 80):
            targets.append(f"http://{host}:{port}/pipeline/seal")
    body = _canon_json({"type": "pipeline.seal", "tracking_id": tracking_id, "seal": seal}).encode()
    for url in targets:
        try:
            import urllib.request
            req = urllib.request.Request(url, data=body, method="POST",
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=2) as r:
                if getattr(r, "status", 200) < 400:
                    return
        except Exception:
            continue
# === END: sealing ===

# === START: verification ===
def latest_decisions(seals: Optional[List[Dict[str, Any]]] = None,
                     tracking_id: Optional[str] = None) -> Dict[str, str]:
    if seals is None:
        seals = read_seals(tracking_id or "")
    out: Dict[str, str] = {}
    for s in seals:
        st = s.get("stage")
        if st:
            out[st] = s.get("decision", "DEFERRED")
    return out


def verify_chain(tracking_id: str) -> Dict[str, Any]:
    """Recompute every seal hash + signature; report tampering and gaps."""
    seals = read_seals(tracking_id)
    problems: List[Dict[str, Any]] = []
    prev = GENESIS
    sig_ok = 0
    hash_ok = 0

    for i, s in enumerate(seals):
        stored_hash = s.get("seal_hash", "")
        stored_sig = s.get("signature", "")
        dock = s.get("dock", "")

        if s.get("prev_hash") != prev:
            problems.append({"seal_index": i, "type": "chain_break",
                             "detail": f"prev_hash mismatch (expected {prev[:16]}…, got {str(s.get('prev_hash'))[:16]}…)"})

        recomputed = dict(s)
        for k in ("seal_hash", "signature", "persisted"):
            recomputed.pop(k, None)
        expect = inahash(_canon_json(recomputed) + "|" + str(s.get("prev_hash", "")))
        if expect == stored_hash:
            hash_ok += 1
        else:
            problems.append({"seal_index": i, "type": "hash_mismatch",
                             "detail": f"recomputed {expect[:16]}… != stored {str(stored_hash)[:16]}… (TAMPERED)"})

        if verify_signature(dock, stored_hash, stored_sig):
            sig_ok += 1
        else:
            problems.append({"seal_index": i, "type": "bad_signature",
                             "detail": f"signature invalid for dock '{dock}'"})

        prev = stored_hash or prev

    latest = latest_decisions(seals)
    missing = [g for g in DEPLOY_GATES if g not in latest]
    failing = {k: v for k, v in latest.items() if v == "DENIED"}
    deferred = {k: v for k, v in latest.items() if v in ("DEFERRED", "SKIPPED")}
    warned = [s.get("stage") for s in seals if s.get("gate_warnings")]

    return {
        "tracking_id": tracking_id,
        "seal_count": len(seals),
        "hash_verified": hash_ok,
        "signature_verified": sig_ok,
        "chain_valid": not any(p["type"] in ("chain_break", "hash_mismatch") for p in problems),
        "signatures_valid": sig_ok == len(seals) and len(seals) > 0,
        "tamper_evident": len(seals) > 0 and hash_ok == len(seals),
        "problems": problems,
        "latest_decisions": latest,
        "missing_deploy_gates": missing,
        "denied_stages": failing,
        "deferred_stages": deferred,
        "stages_with_gate_warnings": sorted({w for w in warned if w}),
        "stages_covered": sorted(latest),
        "stages_absent": [s for s in PIPELINE_ORDER if s not in latest],
        "inahash_scheme": inahash_scheme(),
    }


def can_deploy(tracking_id: str) -> Tuple[bool, List[str]]:
    """Hard gate host_controller MUST consult before writing (S7.10/S7.11)."""
    v = verify_chain(tracking_id)
    reasons: List[str] = []
    if v["seal_count"] == 0:
        return False, ["no_seals: passport has no custody records"]
    if not v["chain_valid"]:
        reasons.append("chain_invalid: custody chain broken or tampered")
    if not v["signatures_valid"]:
        reasons.append("signatures_invalid: one or more seals fail INAHASH verification")
    for g in v["missing_deploy_gates"]:
        reasons.append(f"missing_gate:{g}")
    for st, dec in v["denied_stages"].items():
        reasons.append(f"denied:{st}")
    for st in ("dast", "iast"):
        d = v["latest_decisions"].get(st)
        if d is None:
            reasons.append(f"missing_gate:{st}")
        elif d not in PASSING:
            reasons.append(f"gate_not_passed:{st}={d}")
    for st in ("architect", "coder", "codereview", "sast"):
        d = v["latest_decisions"].get(st)
        if d is not None and d not in PASSING:
            reasons.append(f"gate_not_passed:{st}={d}")
    return (len(reasons) == 0), reasons


def get_passport_report(tracking_id: str) -> Dict[str, Any]:
    seals = read_seals(tracking_id)
    v = verify_chain(tracking_id)
    ok, reasons = can_deploy(tracking_id)
    stages: List[Dict[str, Any]] = []
    prev_t = None
    for s in seals:
        t = s.get("time_uro", {})
        iso = t.get("iso")
        delta = None
        try:
            if prev_t and iso:
                a = _dt.datetime.fromisoformat(prev_t)
                b = _dt.datetime.fromisoformat(iso)
                delta = round((b - a).total_seconds(), 3)
        except Exception:
            delta = None
        prev_t = iso or prev_t
        stages.append({
            "seal_index": s.get("seal_index"),
            "stage": s.get("stage"),
            "dock": s.get("dock"),
            "decision": s.get("decision"),
            "reviewer": s.get("reviewer"),
            "at": iso,
            "seconds_since_prev": delta,
            "artifact_sha": (s.get("artifact_sha") or "")[:32],
            "seal_hash": (s.get("seal_hash") or "")[:32],
            "signature_valid": verify_signature(s.get("dock", ""), s.get("seal_hash", ""), s.get("signature", "")),
            "gate_warnings": s.get("gate_warnings", []),
            "notes": s.get("notes", ""),
        })
    return {
        "schema": "uro.pipeline.report",
        "tracking_id": tracking_id,
        "passport": get_passport(tracking_id) or {},
        "journey": stages,
        "verification": v,
        "deploy_authorised": ok,
        "deploy_blockers": reasons,
        "generated": time_uro(),
    }


def render_markdown(tracking_id: str) -> str:
    r = get_passport_report(tracking_id)
    v = r["verification"]
    L: List[str] = []
    L.append(f"# URO PIPELINE PASSPORT — `{tracking_id}`")
    L.append("")
    p = r.get("passport") or {}
    L.append(f"**Title:** {p.get('title','-')}  ")
    L.append(f"**URID pair (S2):** `{p.get('urid_pair')}`  ")
    L.append(f"**Origin:** {p.get('origin','-')}  ")
    L.append(f"**INAHASH scheme (S7.2):** `{v.get('inahash_scheme')}`  ")
    L.append(f"**Signature scheme:** `{r['journey'][0]['stage'] and ''}{p.get('sig_scheme','')}`")
    L.append("")
    L.append("## Deploy Authorisation")
    L.append("")
    if r["deploy_authorised"]:
        L.append("> ✅ **AUTHORISED** — host_controller may write.")
    else:
        L.append("> ⛔ **BLOCKED** — host_controller MUST NOT write.")
        for b in r["deploy_blockers"]:
            L.append(f"> - {b}")
    L.append("")
    L.append("## Chain Integrity (S7.8)")
    L.append("")
    L.append(f"- Seals: **{v['seal_count']}**")
    L.append(f"- Hash-verified: **{v['hash_verified']}/{v['seal_count']}**")
    L.append(f"- Signature-verified: **{v['signature_verified']}/{v['seal_count']}**")
    L.append(f"- Chain valid: **{v['chain_valid']}** | Tamper-evident: **{v['tamper_evident']}**")
    if v["problems"]:
        L.append("")
        L.append("| seal | problem | detail |")
        L.append("|---|---|---|")
        for pr in v["problems"][:20]:
            L.append(f"| {pr['seal_index']} | {pr['type']} | {pr['detail'][:90]} |")
    L.append("")
    L.append("## Journey")
    L.append("")
    L.append("| # | stage | dock | decision | sig | Δs | reviewer | notes |")
    L.append("|---|---|---|---|---|---|---|---|")
    for s in r["journey"]:
        sig = "✅" if s["signature_valid"] else "❌"
        dec = s["decision"]
        icon = {"APPROVED": "✅", "DENIED": "⛔", "WARNING": "⚠️",
                "DEFERRED": "⏸", "SKIPPED": "↷"}.get(dec, "")
        gw = f" ‹{','.join(s['gate_warnings'])}›" if s["gate_warnings"] else ""
        L.append(f"| {s['seal_index']} | {s['stage']} | {s['dock']} | {icon} {dec} | {sig} | "
                 f"{s['seconds_since_prev'] if s['seconds_since_prev'] is not None else '-'} | "
                 f"{s['reviewer']} | {(s['notes'] or '')[:60]}{gw} |")
    L.append("")
    L.append("## Stage Coverage")
    L.append("")
    L.append(f"- Covered: {', '.join(v['stages_covered']) or '(none)'}")
    L.append(f"- Absent: {', '.join(v['stages_absent']) or '(none)'}")
    L.append(f"- Denied: {', '.join(f'{k}={x}' for k,x in v['denied_stages'].items()) or '(none)'}")
    L.append("")
    L.append("## Seal Hashes (custody chain)")
    L.append("")
    L.append("```")
    for s in r["journey"]:
        L.append(f"[{s['seal_index']}] {str(s['stage']):<16} {s['seal_hash']}…")
    L.append("```")
    return "\n".join(L)
# === END: verification ===

# === START: cli ===
def _add_common(sp: argparse.ArgumentParser) -> None:
    sp.add_argument("--tracking-id", "-t", required=True)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        prog="ledger.py",
        description="URO pipeline chain-of-custody ledger (INAHASH-signed, S7.2/S7.8)")
    sub = ap.add_subparsers(dest="cmd")

    s = sub.add_parser("open", help="open a pipeline passport for one URO")
    s.add_argument("--tracking-id", "-t")
    s.add_argument("--urid1", default="")
    s.add_argument("--urid2", default="")
    s.add_argument("--title", default="")
    s.add_argument("--origin", default="ci_cd")
    s.add_argument("--artifact-ref", default="")

    s = sub.add_parser("seal", help="append a signed stage seal")
    _add_common(s)
    s.add_argument("--dock", required=True)
    s.add_argument("--stage", required=True)
    s.add_argument("--decision", required=True,
                   help="APPROVED|DENIED|DEFERRED|WARNING|SKIPPED")
    s.add_argument("--artifact-file")
    s.add_argument("--artifact-sha")
    s.add_argument("--artifact-ref")
    s.add_argument("--reviewer")
    s.add_argument("--notes", default="")
    s.add_argument("--evidence", default="", help="JSON object")

    s = sub.add_parser("verify", help="verify chain + signatures")
    _add_common(s)

    s = sub.add_parser("gate", help="deploy authorisation gate (host_controller)")
    _add_common(s)

    s = sub.add_parser("report", help="full journey report")
    _add_common(s)
    s.add_argument("--json", action="store_true")
    s.add_argument("--out")

    s = sub.add_parser("list", help="list passports")
    s.add_argument("--status")

    s = sub.add_parser("hash", help="print INAHASH of a file/string")
    s.add_argument("--file")
    s.add_argument("--string")

    s = sub.add_parser("info", help="ledger environment info")

    args = ap.parse_args(argv)

    if args.cmd == "open":
        p = open_passport(tracking_id=args.tracking_id, urid1=args.urid1, urid2=args.urid2,
                          title=args.title, origin=args.origin, artifact_ref=args.artifact_ref)
        print(json.dumps({"tracking_id": p["tracking_id"], "urahash": p.get("inahash_scheme"),
                          "inahash_scheme": p["inahash_scheme"], "ledger": str(LEDGER_DIR)}, indent=2))
        return 0

    if args.cmd == "seal":
        ev = {}
        if args.evidence:
            try:
                ev = json.loads(args.evidence)
            except Exception as e:
                print(f"[warn] --evidence not valid JSON: {e}", file=sys.stderr)
        seal = seal_stage(args.tracking_id, dock=args.dock, stage=args.stage,
                          decision=args.decision, artifact_file=args.artifact_file,
                          artifact_sha=args.artifact_sha, artifact_ref=args.artifact_ref,
                          reviewer=args.reviewer, notes=args.notes, evidence=ev)
        print(json.dumps({"tracking_id": args.tracking_id, "stage": seal.get("stage"),
                          "decision": seal.get("decision"),
                          "seal_hash": seal.get("seal_hash"),
                          "signature": (seal.get("signature") or "")[:32] + "…",
                          "gate_warnings": seal.get("gate_warnings", []),
                          "persisted": seal.get("persisted")}, indent=2))
        return 0

    if args.cmd == "verify":
        print(json.dumps(verify_chain(args.tracking_id), indent=2))
        return 0

    if args.cmd == "gate":
        ok, reasons = can_deploy(args.tracking_id)
        print(json.dumps({"tracking_id": args.tracking_id, "deploy_authorised": ok,
                          "blockers": reasons}, indent=2))
        return 0 if ok else 3

    if args.cmd == "report":
        if args.json:
            txt = json.dumps(get_passport_report(args.tracking_id), indent=2)
        else:
            txt = render_markdown(args.tracking_id)
        if args.out:
            Path(args.out).write_text(txt)
            print(f"[report] written -> {args.out}")
        else:
            print(txt)
        return 0

    if args.cmd == "list":
        print(json.dumps(list_passports(args.status), indent=2))
        return 0

    if args.cmd == "hash":
        if args.file:
            print(inahash_file(args.file))
        elif args.string:
            print(inahash(args.string))
        else:
            print("[hash] pass --file or --string", file=sys.stderr)
            return 2
        return 0

    if args.cmd == "info":
        print(json.dumps({"version": VERSION, "ledger_dir": str(LEDGER_DIR),
                          "key_dir": str(KEY_DIR), "inahash_scheme": inahash_scheme(),
                          "sig_scheme": SIG_SCHEME, "pipeline_order": PIPELINE_ORDER,
                          "deploy_gates": DEPLOY_GATES, "passports": len(_read_index())}, indent=2))
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
# === END: cli ===


# === START: validation_registration_telemetry ===
# Validation / Registration / Telemetry layer (full Loom dock tracking).
# Enhances every seal_stage() with: pre/post chain validation (S7.8),
# dock + action registration, and a Loom-consumable telemetry event.
# Additive, idempotent, never fatal. Local JSONL is the source of truth;
# remote push to Loom/Observer is best-effort.

REGISTRY_FILE = LEDGER_DIR / "_registry.json"
ACTIONS_FILE = LEDGER_DIR / "_actions.jsonl"
LOOM_EVENTS_FILE = LEDGER_DIR / "_loom_events.jsonl"
TELEMETRY_TARGETS_FILE = LEDGER_DIR / "_telemetry_targets.json"


def _now_iso():
    return time_uro()["iso"]


def _read_registry():
    try:
        return json.loads(REGISTRY_FILE.read_text()) if REGISTRY_FILE.exists() else {"docks": {}}
    except Exception:
        return {"docks": {}}


def _write_registry(reg):
    _ensure_dirs()
    try:
        REGISTRY_FILE.write_text(_canon_json(reg))
    except Exception:
        pass


def _append_jsonl(path, record):
    _ensure_dirs()
    try:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(_canon_json(record) + "\n")
        return True
    except Exception:
        return False


def register_dock(dock, role="", capabilities=None, meta=None):
    """Register/refresh a dock in the swarm registry (S13.1/S13.2)."""
    try:
        reg = _read_registry()
        entry = reg.get("docks", {}).get(dock, {})
        entry.update({
            "dock": dock,
            "role": role or entry.get("role", ""),
            "capabilities": capabilities or entry.get("capabilities", []),
            "registered": entry.get("registered", _now_iso()),
            "last_seen": _now_iso(),
            "meta": meta or entry.get("meta", {}),
        })
        reg.setdefault("docks", {})[dock] = entry
        _write_registry(reg)
        _emit_loom_event({"event_type": "dock_registered", "dock": dock,
                          "detail": {"role": entry.get("role", ""),
                                     "capabilities": entry.get("capabilities", [])}})
        return entry
    except Exception:
        return {"dock": dock, "error": "registration_failed"}


def register_action(tracking_id, dock, stage, action, detail=None, inahash="", decision=""):
    """Append a fine-grained action record to the registration trail."""
    try:
        rec = {
            "schema": "uro.pipeline.action",
            "tracking_id": tracking_id,
            "dock": dock,
            "stage": stage,
            "action": action,
            "decision": decision,
            "inahash": inahash,
            "detail": detail or {},
            "time_uro": time_uro(),
        }
        _append_jsonl(ACTIONS_FILE, rec)
        reg = _read_registry()
        if dock in reg.get("docks", {}):
            reg["docks"][dock]["last_seen"] = rec["time_uro"]["iso"]
            reg["docks"][dock]["actions"] = reg["docks"][dock].get("actions", 0) + 1
            _write_registry(reg)
        else:
            register_dock(dock, role=stage)
        return rec
    except Exception:
        return {}


def _load_telemetry_targets():
    try:
        if TELEMETRY_TARGETS_FILE.exists():
            t = json.loads(TELEMETRY_TARGETS_FILE.read_text())
            if isinstance(t, dict) and t.get("targets"):
                return t["targets"]
    except Exception:
        pass
    return ["http://loom_prod:8000/uro/ingest",
            "http://observer_prod:8000/uro/ingest",
            "http://127.0.0.1:8000/uro/ingest"]


def _emit_loom_event(partial):
    """Write a Loom-consumable event locally + best-effort remote push.

    Never raises. Local JSONL is the durable source of truth.
    """
    try:
        event = {"schema": "uro.loom.event", "event_id": uuid.uuid4().hex,
                 "time_uro": time_uro()}
        event.update(partial)
        _append_jsonl(LOOM_EVENTS_FILE, event)
        if os.environ.get("PIPELINE_REMOTE_PUSH", "1") != "0":
            body = _canon_json(event).encode()
            for url in _load_telemetry_targets():
                try:
                    import urllib.request
                    req = urllib.request.Request(url, data=body, method="POST",
                                                 headers={"Content-Type": "application/json"})
                    with urllib.request.urlopen(req, timeout=2) as r:
                        if getattr(r, "status", 200) < 400:
                            break
                except Exception:
                    continue
        return event
    except Exception:
        return {}


def dock_timeline(dock, limit=500):
    """Every registered action for one dock (the Loom per-dock view)."""
    out = []
    try:
        if ACTIONS_FILE.exists():
            for line in ACTIONS_FILE.read_text(errors="replace").splitlines():
                try:
                    rec = json.loads(line)
                    if rec.get("dock") == dock:
                        out.append(rec)
                except Exception:
                    continue
    except Exception:
        pass
    return out[-limit:]


def full_timeline(tracking_id, limit=1000):
    """Merge seals + registered actions for one URO, ordered by time."""
    items = []
    for s in read_seals(tracking_id):
        items.append({"kind": "seal", "time": s.get("time_uro", {}).get("iso", ""),
                      "dock": s.get("dock"), "stage": s.get("stage"),
                      "decision": s.get("decision"), "hash": s.get("seal_hash", "")})
    try:
        if ACTIONS_FILE.exists():
            for line in ACTIONS_FILE.read_text(errors="replace").splitlines():
                try:
                    rec = json.loads(line)
                    if rec.get("tracking_id") == tracking_id:
                        items.append({"kind": "action", "time": rec.get("time_uro", {}).get("iso", ""),
                                      "dock": rec.get("dock"), "stage": rec.get("stage"),
                                      "decision": rec.get("decision", ""),
                                      "hash": rec.get("inahash", ""),
                                      "action": rec.get("action")})
                except Exception:
                    continue
    except Exception:
        pass
    items.sort(key=lambda x: x.get("time", ""))
    return items[-limit:]


# ---- enhance seal_stage: validation + registration + telemetry -------------
if not getattr(seal_stage, "_uro_enhanced", False):
    _seal_stage_core = seal_stage

    def seal_stage(tracking_id, dock, stage, decision, *args, **kwargs):  # noqa: F811
        try:
            pre = verify_chain(tracking_id)
        except Exception:
            pre = {"chain_valid": True, "seal_count": 0}
        try:
            register_dock(dock, role=stage)
        except Exception:
            pass
        result = _seal_stage_core(tracking_id, dock, stage, decision, *args, **kwargs)
        try:
            post = verify_chain(tracking_id)
        except Exception:
            post = {"chain_valid": False, "seal_count": 0}
        try:
            register_action(tracking_id, dock, stage, "seal",
                            detail={"notes": kwargs.get("notes", ""),
                                    "gate_warnings": result.get("gate_warnings", [])},
                            inahash=result.get("seal_hash", ""), decision=decision)
        except Exception:
            pass
        try:
            _emit_loom_event({
                "event_type": "pipeline_seal",
                "tracking_id": tracking_id,
                "dock": dock,
                "stage": stage,
                "decision": decision,
                "inahash": result.get("seal_hash", ""),
                "signature": (result.get("signature") or "")[:32],
                "chain_valid_before": pre.get("chain_valid"),
                "chain_valid_after": post.get("chain_valid"),
                "seal_count": post.get("seal_count"),
                "gate_warnings": result.get("gate_warnings", []),
                "nte": kwargs.get("nte") or {},
            })
        except Exception:
            pass
        try:
            result["chain_valid_before"] = pre.get("chain_valid")
            result["chain_valid_after"] = post.get("chain_valid")
            result["registered"] = True
            result["telemetry_emitted"] = True
        except Exception:
            pass
        return result

    seal_stage._uro_enhanced = True


# ---- enhance render_markdown: append registration + telemetry trail --------
if not getattr(render_markdown, "_uro_enhanced", False):
    _render_markdown_core = render_markdown

    def render_markdown(tracking_id):  # noqa: F811
        base = _render_markdown_core(tracking_id)
        lines = [base, "", "## Registration & Telemetry Trail", ""]
        tl = full_timeline(tracking_id)
        if tl:
            lines.append("| time | kind | dock | stage | decision | hash |")
            lines.append("|---|---|---|---|---|---|")
            for it in tl[-40:]:
                lines.append(f"| {it.get('time','')} | {it.get('kind','')} | {it.get('dock','')} | "
                             f"{it.get('stage','')} | {it.get('decision','')} | "
                             f"{str(it.get('hash',''))[:16]}… |")
        else:
            lines.append("(no registration/telemetry records yet)")
        reg = _read_registry()
        if reg.get("docks"):
            lines += ["", "## Registered Docks", "",
                      "| dock | role | actions | last_seen |", "|---|---|---|---|"]
            for d, e in reg["docks"].items():
                lines.append(f"| {d} | {e.get('role','')} | {e.get('actions',0)} | {e.get('last_seen','')} |")
        return "\n".join(lines)

    render_markdown._uro_enhanced = True
# === END: validation_registration_telemetry ===
