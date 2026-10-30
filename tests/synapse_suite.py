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
# === FILE: tests/synapse_suite.py ===
# PURPOSE:
#   The RFC 160 10-check validation suite for the synapse protocol.
#   Validates canonical imports, vector construction, 24-axis state,
#   baseline, outcome contract, modulation, engine-owned cross-talk,
#   homeostatic decay, persistence round-trip, and non-fatal bus modulation.
#   Exit code 0 only when all ten checks pass.
# RFC ANCHORS: 16-17 (compliance/conformance), 35-44 (synapse protocol),
#   160 item 4 (run the 10-check suite after core edits).
# NOTE: test-only construction of NTE levels is permitted here; production
#   code MUST NOT mutate nte_state.levels directly (160 item 7).
# === END FILE HEADER ===

# === START: imports ===
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

os.environ["URO_STATE_ROOT"] = tempfile.mkdtemp(prefix="uro_suite_state_")

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RESULTS = []
# === END: imports ===


# === START: check ===
def check(name):
    """PURPOSE: register a numbered validation check in declaration order."""
    def wrap(fn):
        RESULTS.append((name, fn))
        return fn
    return wrap
# === END: check ===


# === START: helpers ===
def _axes():
    """PURPOSE: return the canonical 24 axis names from the enums."""
    from uro.nte.axes import NTEAxis, CognitiveAxis
    return [a.value for a in NTEAxis] + [a.value for a in CognitiveAxis]


def _syn():
    """PURPOSE: shared helper returning a synapse for the fixed test pair."""
    import uro.synapse.persistence as persistence
    return persistence.get_or_create_synapse("0" * 64, "1" * 64)


def _syn_id(syn):
    """PURPOSE: stable identity string for a synapse URID."""
    u = syn.synapse_urid
    return u.to_hex() if hasattr(u, "to_hex") else str(u)
# === END: helpers ===


# === START: checks ===
@check("01 canonical imports resolve")
def c01():
    """PURPOSE: prove direct canonical imports work without compat stubs."""
    import uro.synapse.engine as engine
    import uro.synapse.persistence as persistence
    from uro.synapse.vector import SynapseVectorURO
    from uro.nte.axes import NTEAxis, CognitiveAxis
    assert engine and persistence and SynapseVectorURO and NTEAxis and CognitiveAxis


@check("02 synapse constructs between two endpoints")
def c02():
    """PURPOSE: create or fetch a synapse for an endpoint pair."""
    syn = _syn()
    assert syn is not None and syn.urid1 is not None and syn.urid2 is not None


@check("03 NTE state has exactly 24 axes")
def c03():
    """PURPOSE: assert the composite 24-axis state (DD-1)."""
    assert len(_syn().nte_state.levels) == 24


@check("04 all axes initialize at baseline 50.0")
def c04():
    """PURPOSE: assert equilibrium baseline on fresh synapse state."""
    levels = _syn().nte_state.levels
    assert all(abs(v - 50.0) < 1e-9 for v in levels.values())


@check("05 InteractionOutcome tolerates partial payloads")
def c05():
    """PURPOSE: success mandatory, all other keys default neutral."""
    import uro.synapse.engine as engine
    o = engine.InteractionOutcome(success=True)
    assert o["success"] is True
    assert o.get("novelty", 0.0) == 0.0
    assert o.get("load", 0.0) == 0.0
    assert o.get("trust_signal", 0.0) == 0.0


@check("06 record_interaction modulates all 24 axes")
def c06():
    """PURPOSE: keys preserved at 24 and values move on a strong outcome."""
    import uro.synapse.engine as engine
    syn = _syn()
    before = dict(syn.nte_state.levels)
    syn.record_interaction(engine.InteractionOutcome(
        success=True, novelty=0.8, load=0.2, trust_signal=0.5, latency_ms=10.0))
    after = syn.nte_state.levels
    assert set(after) == set(before) and len(after) == 24
    assert any(abs(after[k] - before[k]) > 1e-9 for k in after)


@check("07 cross-talk is engine-owned (E/I balance observable)")
def c07():
    """PURPOSE: the 24x24 second pass lives in the engine, not callers."""
    import uro.synapse.engine as engine
    fn = None
    for name in ("apply_cross_talk", "cross_talk_pass", "_cross_talk", "apply_crosstalk"):
        candidate = getattr(engine, name, None)
        if callable(candidate):
            fn = candidate
            break
    assert callable(fn), "engine exposes no cross-talk pass"
    levels = {k: 50.0 for k in _axes()}
    levels["glutamate"] = 90.0
    levels["gaba"] = 10.0
    probe = dict(levels)
    out = fn(probe)
    out = out if isinstance(out, dict) else probe
    assert out["glutamate"] < 90.0 and out["gaba"] > 10.0


@check("08 decay_synapse moves axes toward 50.0")
def c08():
    """PURPOSE: homeostatic decay pulls extremes back to baseline."""
    import uro.synapse.engine as engine
    syn = _syn()
    syn.nte_state.levels["glutamate"] = 90.0  # test-only construction
    engine.decay_synapse(syn, rate=0.02)
    assert syn.nte_state.levels["glutamate"] < 90.0


@check("09 persistence round-trips identity and levels")
def c09():
    """PURPOSE: write-behind flush then reload yields the same synapse."""
    import uro.synapse.engine as engine
    import uro.synapse.persistence as persistence
    syn = persistence.get_or_create_synapse("0" * 64, "1" * 64)
    syn.record_interaction(engine.InteractionOutcome(success=True, novelty=0.3))
    persistence.mark_dirty(syn)
    persistence.flush_dirty()
    again = persistence.get_or_create_synapse("0" * 64, "1" * 64)
    assert _syn_id(again) == _syn_id(syn)
    for k, v in syn.nte_state.levels.items():
        assert abs(again.nte_state.levels[k] - v) < 1e-9


@check("10 CoordinatorBus modulation is non-fatal")
def c10():
    """PURPOSE: a raising synapse must never break message flow."""
    from uro.coordinator_bus import CoordinatorBus

    class Boom:
        def record_interaction(self, outcome):
            """PURPOSE: always raise to prove non-fatal handling."""
            raise RuntimeError("boom")

        def record_use(self, success):
            """PURPOSE: also raise on the legacy path."""
            raise RuntimeError("boom")

    CoordinatorBus(dock_name="test_dock")._modulate_synapse_obj(Boom(), {"success": True})
# === END: checks ===


# === START: main ===
def main():
    """PURPOSE: run every registered check and report the gate result."""
    passed = 0
    for name, fn in RESULTS:
        try:
            fn()
            passed += 1
            print("PASS  " + name)
        except Exception as exc:
            print("FAIL  " + name + " :: " + type(exc).__name__ + ": " + str(exc))
    total = len(RESULTS)
    print("%d/%d checks passed" % (passed, total))
    return 0 if passed == total == 10 else 1
# === END: main ===


if __name__ == "__main__":
    raise SystemExit(main())
