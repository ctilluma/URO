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
# MODULE START : uro.opar.stages
# ---------------------------------------------------------------------
# FILE         : uro/opar/stages.py
# PURPOSE      : Stage envelope types exchanged between OPAR stages
#                (RFC 12).
# STANDARD     : URO-STD-0001 OPAR-24
# =====================================================================
"Stage envelope types (RFC 12)."

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

__all__ = ["STAGES", "StageResult"]

STAGES = ("observe", "plan", "act", "review")


@dataclass
class StageResult:
    "PURPOSE: Typed envelope exchanged between OPAR stages (RFC 12)."
    stage: str
    status: str = "FULFILLED"
    data: Dict[str, Any] = field(default_factory=dict)
    nte: Dict[str, float] = field(default_factory=dict)
    latency_ms: float = 0.0
    error: Optional[str] = None
    provenance: List[Dict[str, Any]] = field(default_factory=list)
# =====================================================================
# MODULE END   : uro.opar.stages
# =====================================================================
