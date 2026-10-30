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
# === FILE: tests/memory_suite.py ===
# PURPOSE: Phase 7 validation: tiers, movement rules, four-outcome use counter,
#          consolidation triggers, decay, sleep mode, reflection, cache rule.
# === END FILE HEADER ===
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.memory import MemoryEngine, MemoryItem, MemoryTier
from uro.memory.decay import apply_cognitive_decay
def _item(u1="a", u2="b", **kw):
    return MemoryItem(urid_pair={"urid1": u1, "urid2": u2}, payload="x", **kw)
PAIR = {"urid1": "a", "urid2": "b"}
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 four tiers map to SF/F/M/S hardware")
def c01():
    vals = {t.value for t in MemoryTier}
    assert {"SF_REGISTER", "F_RAM", "M_SSD", "S_HD"} <= vals
@check("02 retrieve promotes long to short then short to working")
def c02():
    eng = MemoryEngine()
    eng.store(_item(tier=MemoryTier.LONG))
    assert eng.retrieve(PAIR).tier == MemoryTier.SHORT
    assert eng.retrieve(PAIR).tier == MemoryTier.WORKING
@check("03 use counter increments per retrieve")
def c03():
    eng = MemoryEngine()
    eng.store(_item())
    eng.retrieve(PAIR)
    eng.retrieve(PAIR)
    assert eng.retrieve(PAIR).use_count == 3
@check("04 connection pass yields the four RFC 66 outcomes")
def c04():
    eng = MemoryEngine()
    now = time.time()
    deny = _item(); assert eng.connection_pass(deny, acl_permit=False) == "DROP_SHORT"
    hu = _item(use_count=5, last_accessed=now)
    assert eng.connection_pass(hu) == "SAVE_LONG_KEEP_SHORT"
    hs = _item(use_count=5, last_accessed=now - 25 * 3600)
    assert eng.connection_pass(hs) == "SAVE_LONG_DROP_SHORT"
    lr = _item(use_count=1, last_accessed=now)
    assert eng.connection_pass(lr) == "KEEP_SHORT_ONLY"
    ls = _item(use_count=1, last_accessed=now - 25 * 3600)
    assert eng.connection_pass(ls) == "DROP_SHORT"
    at = _item(attachment=0.9, last_accessed=now)
    assert eng.connection_pass(at) == "SAVE_LONG_KEEP_SHORT"
@check("05 apply pass executes outcomes incl dual residence")
def c05():
    eng = MemoryEngine()
    it = _item(); eng.store(it)
    eng.apply_pass(it, "SAVE_LONG_KEEP_SHORT")
    assert it.saved_long and it.tier == MemoryTier.SHORT and it.key in eng._store
    eng.apply_pass(it, "DROP_SHORT")
    assert it.tier == MemoryTier.LONG and it.key in eng._store
    fresh = _item(u1="z"); eng.store(fresh)
    eng.apply_pass(fresh, "DROP_SHORT")
    assert fresh.key not in eng._store
@check("06 consolidation by counter, attachment, and epinephrine")
def c06():
    eng = MemoryEngine()
    a = _item(u1="c", use_count=5); eng.store(a)
    b = _item(u1="d", attachment=0.9); eng.store(b)
    c = _item(u1="e", use_count=4); eng.store(c)
    assert eng.consolidate() == 2
    assert c.tier == MemoryTier.SHORT
    assert eng.consolidate(epinephrine=80.0) == 1
    assert c.tier == MemoryTier.LONG and c.saved_long
@check("07 introspection clears work to short and short to long")
def c07():
    eng = MemoryEngine()
    w = _item(u1="w", tier=MemoryTier.WORKING); eng.store(w)
    s = _item(u1="s", tier=MemoryTier.SHORT); eng.store(s)
    moved = eng.introspect()
    assert moved == {"working_to_short": 1, "short_to_long": 1}
    assert w.tier == MemoryTier.SHORT and s.tier == MemoryTier.LONG
@check("08 cognitive decay and pruning")
def c08():
    assert apply_cognitive_decay(1.0, 0.0) == 1.0
    assert apply_cognitive_decay(1.0, 10.0) < 1.0
    eng = MemoryEngine()
    weak = _item(u1="w2", confidence=0.05); eng.store(weak)
    assert weak.key in eng.decay_all()
@check("09 sleep mode reduces ACL and morning questions queue")
def c09():
    eng = MemoryEngine()
    res = eng.sleep_mode(authorized_inputs=["clock"])
    assert res["reduced_acl"] is True and res["authorized_inputs"] == ["clock"]
    eng.queue_morning_question("why did path X fail?")
    assert eng.drain_morning_questions() == ["why did path X fail?"]
    assert eng.drain_morning_questions() == []
@check("10 downtime reflection and cache frequency rule")
def c10():
    eng = MemoryEngine()
    ref = eng.downtime_reflection(failed_pathing_counts={"p1": 3, "p2": 2})
    assert ref["learn_frequency"] == ["p1"]
    assert set(ref) == {"learn_object", "handle_differently", "resolve_better", "learn_frequency"}
    it = _item(use_count=4)
    assert eng.cache_time(it) == 4.0
passed = 0
for name, fn in checks:
    try:
        fn()
        passed += 1
        print("PASS  " + name)
    except Exception as e:
        print("FAIL  " + name + " :: " + type(e).__name__ + ": " + str(e))
print("%d/10 checks passed" % passed)
sys.exit(0 if passed == 10 else 1)
