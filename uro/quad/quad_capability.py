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
# MODULE START : uro.quad.quad_capability
# ---------------------------------------------------------------------
# FILE         : uro/quad/quad_capability.py
# PURPOSE      : Quad-Capability four-dimension evaluation: Base, Gap
#                Remediation, Best Practice, World-First Innovation
#                (RFC 45).
# STANDARD     : URO-STD-0001 S-Quad
# =====================================================================
"Quad-Capability four-dimension evaluation (RFC 45)."

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List

from uro.nte.axes import NTEAxis

__all__ = ["QuadDimension", "QuadCapabilityRecord", "innovation_affinity",
           "GAP_REMEDIATION_THRESHOLD"]

GAP_REMEDIATION_THRESHOLD = 50.0


class QuadDimension(str, Enum):
    "PURPOSE: The four evaluation dimensions (RFC 45)."
    BASE = "base"
    GAP_REMEDIATION = "gap_remediation"
    BEST_PRACTICE = "best_practice"
    WORLD_FIRST = "world_first"


@dataclass
class QuadCapabilityRecord:
    "PURPOSE: Scores across the four evaluation dimensions (RFC 45)."
    capability_id: str
    base: float = 0.0
    gap_remediation: float = 0.0
    best_practice: float = 0.0
    world_first: float = 0.0
    notes: List[str] = field(default_factory=list)

    def composite(self) -> float:
        "PURPOSE: Mean of the four dimension scores."
        return (self.base + self.gap_remediation + self.best_practice + self.world_first) / 4.0

    def remediation_required(self) -> bool:
        "PURPOSE: Gap dimension below threshold flags self-correction work."
        return self.gap_remediation < GAP_REMEDIATION_THRESHOLD


def innovation_affinity(levels: Dict) -> float:
    "PURPOSE: RFC 45.4 world-first affinity from creativity and analogical_transfer."
    c = levels.get(NTEAxis.CREATIVITY)
    if c is None:
        c = levels.get("creativity", 50.0)
    a = levels.get(NTEAxis.ANALOGICAL_TRANSFER)
    if a is None:
        a = levels.get("analogical_transfer", 50.0)
    return (float(c) + float(a)) / 200.0
# =====================================================================
# MODULE END   : uro.quad.quad_capability
# =====================================================================
