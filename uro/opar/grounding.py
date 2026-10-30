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
# MODULE START : uro.opar.grounding
# ---------------------------------------------------------------------
# FILE         : uro/opar/grounding.py
# PURPOSE      : Grounded emission gate engines (RFC 15): dock cap_37
#                preferred when importable, open local heuristic fallback.
# STANDARD     : URO-STD-0001 OPAR-24
# =====================================================================
"Grounded emission gate engines (RFC 15, ADR-022)."

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

__all__ = ["GroundingResult", "LocalGroundingEngine", "get_grounding_engine"]


@dataclass
class GroundingResult:
    "PURPOSE: Typed grounding verdict for one artifact (RFC 15)."
    verified_count: int = 0
    refuted_count: int = 0
    unverifiable_count: int = 0
    overall_grounding: float = 1.0
    emit_with_flags: bool = False


class LocalGroundingEngine:
    "PURPOSE: Open-library claim grounding heuristic (ADR-022 fallback)."

    async def ground_artifact(self, artifact: Dict[str, Any]) -> GroundingResult:
        "PURPOSE: Count verified/refuted/unverifiable claims in an artifact."
        claims = artifact.get("claims", []) if isinstance(artifact, dict) else []
        claims = [c for c in claims if isinstance(c, dict)]
        verified = sum(1 for c in claims if c.get("grounded") is True)
        refuted = sum(1 for c in claims if c.get("grounded") is False)
        unverifiable = len(claims) - verified - refuted
        overall = (verified / len(claims)) if claims else 1.0
        return GroundingResult(verified, refuted, unverifiable, overall, unverifiable > 0)


def get_grounding_engine():
    "PURPOSE: Resolve dock cap_37 engine first, else local heuristic (ADR-022)."
    try:
        from capabilities.cap_37_grounded_emission import get_grounding_engine as dock_get
        return dock_get()
    except Exception:
        return LocalGroundingEngine()
# =====================================================================
# MODULE END   : uro.opar.grounding
# =====================================================================
