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
# === FILE: tests/quad_suite.py ===
# PURPOSE: Phase 12 validation: quad dimensions, composite and remediation,
#          innovation affinity, CROATE traits, character/condition drift.
# === END FILE HEADER ===
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.quad.quad_capability import (QuadDimension, QuadCapabilityRecord,
    innovation_affinity, GAP_REMEDIATION_THRESHOLD)
from uro.quad.character_condition import CharacterCondition, SD_UNIT
from uro.quad.croate import CROATE, TRAIT_NTE_MAP, trait_from_nte
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 four quad dimensions per RFC 45")
def c01():
    assert [d.value for d in QuadDimension] == ["base", "gap_remediation", "best_practice", "world_first"]
@check("02 composite is the four-dimension mean")
def c02():
    r = QuadCapabilityRecord("cap.x", base=80, gap_remediation=60, best_practice=70, world_first=90)
    assert abs(r.composite() - 75.0) < 1e-9
@check("03 gap remediation flag below threshold")
def c03():
    low = QuadCapabilityRecord("cap.low", gap_remediation=40.0)
    high = QuadCapabilityRecord("cap.high", gap_remediation=60.0)
    assert low.remediation_required() and not high.remediation_required()
@check("04 innovation affinity from creativity and transfer")
def c04():
    hi = {"creativity": 90.0, "analogical_transfer": 90.0}
    lo = {"creativity": 10.0, "analogical_transfer": 10.0}
    assert abs(innovation_affinity(hi) - 0.9) < 1e-9
    assert abs(innovation_affinity(lo) - 0.1) < 1e-9
@check("05 CROATE has six traits")
def c05():
    assert len(list(CROATE)) == 6
    assert set(TRAIT_NTE_MAP) == set(CROATE)
@check("06 trait scores are means of mapped axes")
def c06():
    levels = {a.value: 50.0 for a in __import__("uro.nte.axes", fromlist=["NTEAxis"]).NTEAxis}
    levels["oxytocin"] = 90.0
    traits = trait_from_nte(levels)
    assert traits[CROATE.TRUST] == 90.0 and traits[CROATE.AGREEABLENESS] == 90.0
    assert traits[CROATE.REWARD] == 50.0
@check("07 returns within 1 SD leave character untouched")
def c07():
    cc = CharacterCondition(character={"t": 50.0})
    cc.set_condition("t", 55.0)
    assert cc.apply_period("t", sustained_periods=10) == 50.0
@check("08 sustained deviation drifts character toward condition")
def c08():
    cc = CharacterCondition(character={"t": 50.0})
    cc.set_condition("t", 90.0)
    new = cc.apply_period("t", sustained_periods=5)
    assert 50.0 < new <= 90.0
@check("09 drift is monotonic and bounded by condition")
def c09():
    cc = CharacterCondition(character={"t": 50.0})
    cc.set_condition("t", 90.0)
    seq = [cc.apply_period("t", sustained_periods=1) for _ in range(5)]
    assert all(b >= a for a, b in zip(seq, seq[1:]))
    assert seq[-1] <= 90.0
@check("10 equilibrium copy and condition clamping")
def c10():
    cc = CharacterCondition(character={"t": 50.0})
    cc.set_condition("t", 150.0)
    assert cc.condition["t"] == 100.0
    eq = cc.equilibrium()
    eq["t"] = 1.0
    assert cc.character["t"] == 50.0
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
