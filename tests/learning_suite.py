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
# === FILE: tests/learning_suite.py ===
# PURPOSE: Phase 10 validation: RFC 90 primitives, 91 dichos, 92 action
#          costing, 93 attention/daydream, 98 aloneness, 33/100 CAS loop.
# === END FILE HEADER ===
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.learning import (CauseEffectLedger, ExperimentLog, FeedbackLoop,
    ObservationRecord, SequenceTracker, segment_by_gaps, correlate_gaps,
    differentiate, correlate, DichoRegistry, ActionType, ActionCost,
    ActionURO, AttentionManager, AlonenessPropagator, CASLoop)
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 cause-effect ledger is bidirectional")
def c01():
    led = CauseEffectLedger()
    led.record("rain", "wet")
    led.record("rain", "wet")
    led.record("sprinkler", "wet")
    assert led.effects_of("rain")["wet"] == 2
    assert set(led.causes_of("wet")) == {"rain", "sprinkler"}
@check("02 experimentation only when not busy")
def c02():
    log = ExperimentLog()
    assert log.schedule("act", "tgt", busy=True) is None
    tid = log.schedule("act", "tgt", busy=False)
    assert tid == 0
    log.record_result(tid, 0.9)
    assert log.trials[tid]["result"] == 0.9
@check("03 feedback loop converges")
def c03():
    loop = FeedbackLoop(gain=0.5)
    current = 0.0
    for _ in range(60):
        current += loop.step(current, 10.0)
    assert abs(current - 10.0) < 1e-6
@check("04 observation and sequencing")
def c04():
    obs = ObservationRecord(stream="vision", payload=1)
    assert obs.stream == "vision"
    seq = SequenceTracker()
    for ev in ("A", "B", "A", "B"):
        seq.observe(ev)
    assert seq.predict_next("A") == "B"
    assert seq.predict_next("B") == "A"
@check("05 gaps segment patterns and correlate")
def c05():
    segs = segment_by_gaps([1, 2, 3, 50, 51, 52], 10)
    assert segs == [[1, 2, 3], [50, 51, 52]]
    assert correlate_gaps(segs, segs) == 2
@check("06 differentiate and correlate round-trip")
def c06():
    payload = {"a": 1, "b": 2}
    comps = differentiate(payload)
    assert len(comps) == 2
    assert correlate(comps) == payload
@check("07 dichos resolve to shared core ideas")
def c07():
    reg = DichoRegistry()
    reg.register("the last straw", "core:final_trigger")
    reg.register("la ultima gota", "core:final_trigger")
    assert reg.resolve("The Last Straw") == "core:final_trigger"
    assert reg.commonalities("the last straw", "la ultima gota") == "core:final_trigger"
    assert reg.structure_fallback("a b c", "b c d") == ["b", "c"]
@check("08 action costing roll-up by type")
def c08():
    leaves = [ActionURO(ActionType.SERIAL, cost=ActionCost(t, 2.0, 0.9)) for t in (1, 2, 3)]
    ser = ActionURO(ActionType.SERIAL, parts=list(leaves))
    par = ActionURO(ActionType.PARALLEL, parts=list(leaves))
    st = ser.total_cost()
    pt = par.total_cost()
    assert st.time == 6 and pt.time == 3
    assert st.price == pt.price == 6.0
    assert abs(st.reliability - 0.9 ** 3) < 1e-9
@check("09 attention overrides and daydream")
def c09():
    mgr = AttentionManager(["vision", "audio"])
    mgr.prioritize("vision", 2.0)
    mgr.prioritize("audio", 1.0)
    assert mgr.active_order() == ["vision", "audio"]
    mgr.override("audio")
    assert mgr.active_order() == ["audio", "vision"]
    mgr.daydream(True)
    assert mgr.active_order()[0] == "internal"
    mgr.daydream(False)
    assert mgr.active_order() == ["vision", "audio", "internal"]
@check("10 aloneness propagator and CAS prediction")
def c10():
    prop = AlonenessPropagator(input_threshold=2)
    prop.observe_input(1)
    assert prop.should_seek() is True
    prop.observe_input(5)
    assert prop.should_seek() is False
    prop.reset_window()
    assert prop.seek_action()["aloneness_override"] is True
    cas = CASLoop()
    cas.associate("ctx", 0.8)
    cas.associate("ctx", 0.8)
    assert abs(cas.predict("ctx") - 0.8) < 1e-9
    assert abs(cas.prediction_error("ctx", 1.0) - 0.2) < 1e-9
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
