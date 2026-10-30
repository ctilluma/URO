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


# =====================================================================
# MODULE START : uro.opar.base
# ---------------------------------------------------------------------
# FILE         : uro/opar/base.py
# PURPOSE      : OPARBase: canonical OPAR-24 capability base class with
#                stage isolation, grounded gate, receipt honesty contract
#                (RFC 10-15).
# STANDARD     : URO-STD-0001 OPAR-24
# =====================================================================
"Canonical OPAR-24 capability base class (RFC 10-15)."

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from uro.nte.axes import AXES_24
from uro.opar.stages import STAGES, StageResult

__all__ = ["OPARBase", "nte24", "BASELINE"]

logger = logging.getLogger("URO.OPAR")

BASELINE = 50.0


def nte24(state: Optional[Dict[str, float]]) -> Dict[str, float]:
    "PURPOSE: Full 24-axis state from partial input; axes canonical (ADR-011)."
    state = state or {}
    out: Dict[str, float] = {}
    for axis in AXES_24:
        value = state.get(axis)
        if value is None:
            for key in list(state):
                if str(getattr(key, "value", key)) == axis:
                    value = state[key]
                    break
        out[axis] = float(value if value is not None else BASELINE)
    return out


class OPARBase:
    "PURPOSE: Canonical OPAR capability; subclass and implement four stages."
    capability_id: str = "opar.capability"
    grounding_enabled: bool = True
    grounding_threshold: float = 0.5

    def __init__(self, bus=None, **kwargs) -> None:
        self.bus = bus

    async def observe(self, stimulus: Any, nte: Dict[str, float]) -> StageResult:
        "PURPOSE: Stage 1; subclasses override."
        raise NotImplementedError

    async def plan(self, observation: StageResult, nte: Dict[str, float]) -> StageResult:
        "PURPOSE: Stage 2; subclasses override."
        raise NotImplementedError

    async def act(self, plan: StageResult, nte: Dict[str, float]) -> StageResult:
        "PURPOSE: Stage 3; subclasses override."
        raise NotImplementedError

    async def review(self, observation: StageResult, plan: StageResult,
                     action: StageResult, nte: Dict[str, float]) -> StageResult:
        "PURPOSE: Stage 4; subclasses override."
        raise NotImplementedError

    async def _run_stage(self, name: str, fn, *args, nte: Dict[str, float]) -> StageResult:
        "PURPOSE: Non-fatal per-stage isolation wrapper (RFC 16 item 4)."
        t0 = time.time()
        try:
            res = await fn(*args, nte)
            if not isinstance(res, StageResult):
                res = StageResult(stage=name, data=res if isinstance(res, dict) else {"value": res})
            res.stage = name
            res.latency_ms = round((time.time() - t0) * 1000, 3)
            if not res.nte:
                res.nte = nte24(nte)
            return res
        except Exception as exc:
            logger.exception("OPAR stage %s failed in %s", name, self.capability_id)
            return StageResult(stage=name, status="INCAPABLE",
                               error=type(exc).__name__ + ": " + str(exc),
                               latency_ms=round((time.time() - t0) * 1000, 3),
                               nte=nte24(nte))

    async def execute(self, stimulus: Any, nte: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        "PURPOSE: Canonical driver and smart-loader entry point (RFC 13/14)."
        nte = nte24(nte)
        trace: List[StageResult] = []
        obs = await self._run_stage("observe", self.observe, stimulus, nte=nte)
        trace.append(obs)
        if obs.status == "INCAPABLE":
            return self._receipt("INCAPABLE", trace, nte)
        plan = await self._run_stage("plan", self.plan, obs, nte=nte)
        trace.append(plan)
        if plan.status == "INCAPABLE":
            return self._receipt("INCAPABLE", trace, nte)
        act = await self._run_stage("act", self.act, plan, nte=nte)
        trace.append(act)
        rev = await self._run_stage("review", self.review, obs, plan, act, nte=nte)
        trace.append(rev)
        gate = await self._grounding_gate(act, rev)
        status = self._final_status(trace, gate)
        return self._receipt(status, trace, nte, gate=gate)

    async def _grounding_gate(self, action: StageResult, review: StageResult) -> Dict[str, Any]:
        "PURPOSE: Grounded emission gate; non-fatal by mandate (RFC 15)."
        if not self.grounding_enabled:
            return {"gate": "skipped"}
        try:
            from uro.opar.grounding import get_grounding_engine
            artifact = action.data.get("artifact") or action.data
            if not isinstance(artifact, dict):
                return {"gate": "skipped", "reason": "no_artifact"}
            g = await get_grounding_engine().ground_artifact(artifact)
            blocked = g.refuted_count > 0 or g.overall_grounding < self.grounding_threshold
            gate = "blocked" if blocked else ("emit_with_flags" if g.emit_with_flags else "passed")
            return {"gate": gate, "score": g.overall_grounding,
                    "verified": g.verified_count, "refuted": g.refuted_count,
                    "unverifiable": g.unverifiable_count}
        except Exception as exc:
            logger.warning("grounding gate failed (non-fatal): %s", exc)
            return {"gate": "error", "reason": str(exc)}

    def _final_status(self, trace: List[StageResult], gate: Dict[str, Any]) -> str:
        "PURPOSE: RFC 15 status resolution from trace and gate."
        if any(s.status == "INCAPABLE" for s in trace):
            return "INCAPABLE"
        return "DEFERRED" if (gate or {}).get("gate") == "blocked" else "FULFILLED"

    def _receipt(self, status: str, trace: List[StageResult], nte: Dict[str, float],
                 gate: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        "PURPOSE: Receipt with trace, 24-axis NTE, grounding, provenance."
        return {
            "status": status,
            "capability_id": self.capability_id,
            "opar_trace": [{"stage": s.stage, "status": s.status,
                            "latency_ms": s.latency_ms, "error": s.error,
                            "data": s.data} for s in trace],
            "nte": nte24(nte),
            "_grounding": gate or {},
            "_gate": (gate or {}).get("gate", "unknown"),
            "_provenance": {"capability_id": self.capability_id,
                            "model": "24^24", "timestamp": time.time()},
        }

    def _modulate(self, nte: Dict[str, float], stage_result: StageResult, stage_name: str) -> Dict[str, float]:
        "PURPOSE: 24^24 modulation hook (RFC 15.1)."
        return nte24(stage_result.nte or nte)
# =====================================================================
# MODULE END   : uro.opar.base
# =====================================================================
