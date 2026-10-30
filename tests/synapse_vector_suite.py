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
# === FILE: tests/synapse_vector_suite.py ===
# PURPOSE: Phase 6 validation: RFC 36.1 field census, 36.2 method semantics,
#          genesis trust delegation, non-fatal mandate, durable round-trip.
# === END FILE HEADER ===
import os
import sys
import tempfile
from pathlib import Path
os.environ["URO_STATE_ROOT"] = tempfile.mkdtemp(prefix="uro_vector_state_")
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.core.urid import URID
from uro.nte.state import NTEStateURO
from uro.synapse.vector import SynapseVectorURO
from uro.synapse.engine import InteractionOutcome
from uro.synapse.persistence import get_or_create_synapse, mark_dirty, flush_dirty
FIELDS = ("urid1", "urid2", "synapse_urid", "nte_state", "topic_trusts",
          "overall_trust", "use_count", "success_count", "last_used",
          "inahash", "created_at", "last_updated")
def _mk(parent=None):
    s = URID.new()
    return SynapseVectorURO(urid1=URID.new(), urid2=URID.new(), synapse_urid=s,
                            nte_state=NTEStateURO(urid1=s, urid2=URID.new()),
                            parent_inahash=parent)
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 all twelve RFC 36.1 fields present")
def c01():
    syn = _mk()
    assert all(hasattr(syn, f) for f in FIELDS)
    assert len(syn.nte_state.levels) == 24
@check("02 record_interaction books and modulates")
def c02():
    syn = _mk()
    before = dict(syn.nte_state.levels)
    syn.record_interaction(InteractionOutcome(success=True, novelty=0.8,
                                              load=0.2, trust_signal=0.5))
    assert syn.use_count == 1 and syn.success_count == 1
    assert any(syn.nte_state.levels[k] != before[k] for k in before)
@check("03 record_use is counters-only")
def c03():
    syn = _mk()
    before = dict(syn.nte_state.levels)
    syn.record_use(True)
    assert syn.use_count == 1 and syn.success_count == 1
    assert syn.nte_state.levels == before
@check("04 topic trust updates directionally and clamps")
def c04():
    syn = _mk()
    syn.update_topic_trust("t", 10.0, {})
    a = syn.get_topic_trust("t").trust_level
    syn.update_topic_trust("t", -30.0, {})
    b = syn.get_topic_trust("t").trust_level
    syn.update_topic_trust("t", -1000.0, {})
    c = syn.get_topic_trust("t").trust_level
    assert b < a and c >= 0.0
@check("05 overall trust aggregates within bounds")
def c05():
    syn = _mk()
    syn.update_topic_trust("alpha", 30.0, {})
    assert 0.0 <= syn.overall_trust <= 100.0
    assert syn.overall_trust > 0.0
@check("06 success rate math")
def c06():
    syn = _mk()
    assert syn.get_success_rate() == 0.0
    syn.record_use(True)
    syn.record_use(False)
    assert syn.get_success_rate() == 50.0
@check("07 seal integrity stable")
def c07():
    syn = _mk()
    syn.seal()
    assert syn.inahash and syn.inahash == syn.compute_inahash()
@check("08 genesis trust delegates to lineage rule")
def c08():
    assert _mk().genesis_trust_level() == 0.0
    assert _mk(parent="f" * 64).genesis_trust_level() == 100.0
@check("09 hostile outcome is non-fatal")
def c09():
    syn = _mk()
    syn.record_interaction({"success": True, "novelty": object()})
    assert syn.use_count == 1
@check("10 persistence round-trips counters and topics")
def c10():
    syn = get_or_create_synapse("a" * 64, "b" * 64)
    syn.record_interaction(InteractionOutcome(success=True, novelty=0.5))
    syn.update_topic_trust("persist", 5.0, {})
    mark_dirty(syn)
    flush_dirty()
    again = get_or_create_synapse("a" * 64, "b" * 64)
    assert again.use_count == syn.use_count
    assert "persist" in again.topic_trusts
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
