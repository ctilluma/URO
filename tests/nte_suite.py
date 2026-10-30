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
# === FILE: tests/nte_suite.py ===
# PURPOSE: Phase 4 validation: canonical 24-axis taxonomy (ADR-011), governance
#          coverage, baseline/clamp/seal semantics, legacy view compliance.
# === END FILE HEADER ===
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.core.urid import URID
from uro.nte.axes import (
    NTEAxis, CognitiveAxis, AXES_24, BIOLOGICAL_AXES, COGNITIVE_AXES,
    NTE_AXES, normalize_nte_state,
)
from uro.nte.state import NTEStateURO
from uro.nte.neurotransmitters import NTEState as LegacyNTEState
from uro.nte.nte_state import NTEState as AliasNTEState
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 NTEAxis has 24 members")
def c01():
    assert len(list(NTEAxis)) == 24
@check("02 AXES_24 matches enum order and length")
def c02():
    assert AXES_24 == tuple(a.value for a in NTEAxis)
    assert len(AXES_24) == 24
@check("03 12/12 partition disjoint and complete")
def c03():
    assert len(BIOLOGICAL_AXES) == 12 and len(COGNITIVE_AXES) == 12
    assert not set(BIOLOGICAL_AXES) & set(COGNITIVE_AXES)
    assert set(BIOLOGICAL_AXES) | set(COGNITIVE_AXES) == set(AXES_24)
@check("04 CognitiveAxis is a compat subset of NTEAxis")
def c04():
    assert {c.value for c in CognitiveAxis} <= {a.value for a in NTEAxis}
@check("05 governance covers all 24 axes")
def c05():
    assert set(NTE_AXES) == set(NTEAxis)
    for axis in NTEAxis:
        g = NTE_AXES[axis]
        assert g.niche and g.governance_role
@check("06 fresh state is 24 keys at baseline 50")
def c06():
    st = NTEStateURO(urid1=URID.new(), urid2=URID.new())
    assert len(st.levels) == 24
    assert all(abs(v - 50.0) < 1e-9 for v in st.levels.values())
@check("07 set_level clamps to [0, 100]")
def c07():
    st = NTEStateURO(urid1=URID.new(), urid2=URID.new())
    st.set_level(NTEAxis.GLUTAMATE, 150.0)
    assert st.levels[NTEAxis.GLUTAMATE] == 100.0
    st.set_level(NTEAxis.GLUTAMATE, -5.0)
    assert st.levels[NTEAxis.GLUTAMATE] == 0.0
@check("08 seal integrity stable")
def c08():
    st = NTEStateURO(urid1=URID.new(), urid2=URID.new())
    st.seal()
    assert st.inahash and st.inahash == st.compute_inahash()
@check("09 normalize pads partial state to 24")
def c09():
    full = normalize_nte_state({"glutamate": 70.0})
    assert len(full) == 24
    assert full["glutamate"] == 70.0
    assert full["gaba"] == 50.0
@check("10 legacy views are 24-compliant")
def c10():
    legacy = LegacyNTEState()
    assert len(legacy.levels) == 24
    canon = legacy.to_canonical()
    assert len(canon) == 24
    assert all(0.0 <= v <= 100.0 for v in canon.values())
    assert (AliasNTEState is NTEStateURO) or len(AliasNTEState().as_dict()) == 24
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
