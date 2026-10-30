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
# === FILE: tests/opar_suite.py ===
# PURPOSE: Phase 11 validation: RFC 12-17 OPAR-24 contract, receipt honesty,
#          grounded gate semantics, compliance checklist, conformance test.
# === END FILE HEADER ===
import asyncio
import inspect
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.opar import (STAGES, StageResult, OPARBase, nte24, OPARCapability,
                      checklist, run_conformance, source_has_no_op_stub)
import uro.opar.base as basemod

class EchoCap(OPARBase):
    "PURPOSE: Reference capability for conformance measurement."
    capability_id = "test.echo"

    async def observe(self, stimulus, nte):
        self._stim = stimulus
        return StageResult(stage="observe", data={"seen": stimulus})

    async def plan(self, observation, nte):
        return StageResult(stage="plan", data={"plan": "echo"})

    async def act(self, plan, nte):
        stim = getattr(self, "_stim", {})
        if isinstance(stim, dict) and stim.get("fail_act"):
            raise RuntimeError("act boom")
        if isinstance(stim, dict) and stim.get("false_claim"):
            artifact = {"claims": [{"grounded": False}]}
        else:
            artifact = {"claims": [{"grounded": True}]}
        return StageResult(stage="act", data={"artifact": artifact})

    async def review(self, observation, plan, action, nte):
        return StageResult(stage="review", data={"ok": True})

checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 STAGES order per RFC 12")
def c01():
    assert STAGES == ("observe", "plan", "act", "review")
@check("02 nte24 baseline and partial fill")
def c02():
    full = nte24(None)
    assert len(full) == 24 and all(v == 50.0 for v in full.values())
    part = nte24({"glutamate": 70.0})
    assert part["glutamate"] == 70.0 and part["gaba"] == 50.0
@check("03 StageResult defaults per RFC 12")
def c03():
    sr = StageResult(stage="observe")
    assert sr.status == "FULFILLED" and sr.data == {} and sr.nte == {}
    assert sr.latency_ms == 0.0 and sr.error is None and sr.provenance == []
@check("04 valid stimulus yields FULFILLED with full trace")
def c04():
    r = asyncio.run(EchoCap().execute({"ok": True}))
    assert r["status"] == "FULFILLED"
    assert [s["stage"] for s in r["opar_trace"]] == ["observe", "plan", "act", "review"]
@check("05 failing act is INCAPABLE and isolated")
def c05():
    r = asyncio.run(EchoCap().execute({"fail_act": True}))
    assert r["status"] == "INCAPABLE"
    assert len(r["opar_trace"]) == 4
    assert r["opar_trace"][2]["status"] == "INCAPABLE"
@check("06 false claim is DEFERRED with blocked gate")
def c06():
    r = asyncio.run(EchoCap().execute({"false_claim": True}))
    assert r["status"] == "DEFERRED" and r["_gate"] == "blocked"
    assert r["_grounding"]["refuted"] == 1
@check("07 receipt honesty contract")
def c07():
    r = asyncio.run(EchoCap().execute({"ok": True}))
    assert len(r["nte"]) == 24
    assert {"capability_id", "model", "timestamp"} <= set(r["_provenance"])
    assert "_grounding" in r and "_gate" in r
@check("08 grounding disabled skips gate")
def c08():
    cap = EchoCap()
    cap.grounding_enabled = False
    r = asyncio.run(cap.execute({"false_claim": True}))
    assert r["status"] == "FULFILLED" and r["_gate"] == "skipped"
@check("09 reference satisfies OPARCapability protocol")
def c09():
    assert isinstance(EchoCap(), OPARCapability)
@check("10 checklist and conformance harness pass")
def c10():
    cap = EchoCap()
    assert all(checklist(cap).values())
    conf = run_conformance(cap, {"ok": True}, {"fail_act": True}, {"false_claim": True})
    assert all(conf.values())
    assert source_has_no_op_stub(Path(inspect.getsourcefile(basemod))) is False
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
