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
# === FILE: tests/nte_math_suite.py ===
# PURPOSE: Phase 5 validation: polarity table, weighting curves, firing and
#          receptor mechanics, D1/D2 reward, habit/R-P propagation, ANS.
# === END FILE HEADER ===
import math
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.nte.axes import NTEAxis
from uro.nte.polarity import POLARITY, polarity_for
from uro.nte.math_influence import InfluenceType, apply_influence, cost_to_buy
from uro.nte.firing import (fire_decision, transmit_signal, fire_multiplier,
                            activity, min_fire_chance, max_fire_chance)
from uro.nte.reward import reward_event, is_habit, habit_broken, propagate_rp
from uro.nte.ans import dominant_branch, regulation_actions
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 polarity covers 24 axes with descriptors")
def c01():
    assert set(POLARITY) == set(NTEAxis)
    neg, pos = polarity_for(NTEAxis.GLUTAMATE)
    assert "conservative" in neg.lower() and "excitation" in pos.lower()
@check("02 weighting curves match RFC 27")
def c02():
    assert abs(apply_influence(InfluenceType.DOMINATING, 10.0) - 10.0 * math.log10(20.0)) < 1e-9
    assert apply_influence(InfluenceType.STANDARD, 7.0) == 7.0
    assert abs(apply_influence(InfluenceType.WEAK, 128.0) - math.sin(1.0) * 128.0) < 1e-9
    assert apply_influence(InfluenceType.NONE, 42.0) == 0.0
    assert apply_influence(InfluenceType.WEAK_NEGATIVE, 128.0) == -apply_influence(InfluenceType.WEAK, 128.0)
    assert apply_influence(InfluenceType.MILD, 5.0) == 0.0
    assert math.isfinite(apply_influence(InfluenceType.MILD, 20.0))
@check("03 engine remains sole cross-talk executor")
def c03():
    src = (ROOT / "uro" / "synapse" / "engine.py").read_text(encoding="utf-8")
    assert "uro.nte.cross_talk" not in src
@check("04 cost to buy capped at 100")
def c04():
    assert abs(cost_to_buy(10.0) - 3.0) < 1e-9
    assert cost_to_buy(1e6) == 100.0
@check("05 firing decisions match RFC 29.1 examples")
def c05():
    assert fire_decision(30.0, 17.0) is True
    assert fire_decision(90.0, 91.0) is False
    assert fire_decision(60.0, 30.0) is True
    assert fire_decision(45.0, 60.0) is False
    assert transmit_signal(0.5) == 1.0
    assert fire_multiplier(True) == 1.06 and fire_multiplier(False) == 0.40
@check("06 receptor min/max bounds per RFC 30.3")
def c06():
    assert min_fire_chance(30.0, 20.0) == 0.0
    assert abs(min_fire_chance(10.0, 40.0) - 25.0) < 1e-9
    assert max_fire_chance(30.0, 20.0) == 100.0
    assert abs(max_fire_chance(10.0, 40.0) - 25.0) < 1e-9
@check("07 activity is antagonists minus protagonists")
def c07():
    assert activity(22.0, 25.0) == -3.0
@check("08 D1/D2 asymmetry and trust weighting")
def c08():
    d1 = reward_event(True, 2.0)
    d2 = reward_event(False, 2.0)
    assert d1.kind == "D1" and d1.action_directive == "affirm"
    assert d2.kind == "D2" and d2.action_directive == "reconsider"
    assert d1.trust_delta > 0 and d2.trust_delta < 0
    assert d1.stimulation_factor > 1.0 > d2.stimulation_factor
    assert abs(d1.trust_delta) > abs(reward_event(True, 1.0).trust_delta)
@check("09 habit and bi-directional R/P propagation")
def c09():
    assert is_habit(95.0) and not is_habit(50.0)
    assert habit_broken(10.0, 12.0) and not habit_broken(10.0, 8.0)
    chain = ["CRO1", "CRO2", "CRO3"]
    r = propagate_rp(chain, None, True)
    assert all(v == 1.0 for v in r.values())
    p = propagate_rp(chain, 1, False)
    assert p["CRO1"] == 0.0 and p["CRO2"] == -1.0 and p["CRO3"] == 0.0
    c = propagate_rp(chain, None, False)
    assert all(v == -1.0 for v in c.values())
@check("10 ANS branches and regulation thresholds")
def c10():
    sym = {a.value: 50.0 for a in NTEAxis}
    sym["epinephrine"] = 90.0
    sym["cortisol"] = 85.0
    assert dominant_branch(sym) == "sympathetic"
    assert "fight_flight" in regulation_actions(sym)
    par = {a.value: 50.0 for a in NTEAxis}
    par["adenosine"] = 80.0
    par["melatonin"] = 80.0
    acts = regulation_actions(par)
    assert "load_shedding" in acts and "consolidation_window" in acts
    assert "rest_digest" in acts
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
