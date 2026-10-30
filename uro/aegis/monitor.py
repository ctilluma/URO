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


from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class AnomalyReport:
    dock_name: str
    severity: str  # "standard" or "critical"
    reasons: List[str]
    nte_snapshot: Dict[str, float] = field(default_factory=dict)

class AegisMonitor:
    """
    S7.11 Aegis Immune System: Monitors dock health via NTE and trust metrics.
    Triggers quarantine when thresholds are breached.
    """
    def __init__(self, epinephrine_threshold: float = 85.0, trust_threshold: float = 40.0):
        self.epinephrine_threshold = epinephrine_threshold
        self.trust_threshold = trust_threshold

    def evaluate(self, dock_name: str, nte_state: Dict[str, float], trust_score: float) -> Optional[AnomalyReport]:
        reasons = []
        epi = nte_state.get("EPINEPHRINE", 0.0)
        if epi > self.epinephrine_threshold:
            reasons.append(f"EPINEPHRINE {epi} > {self.epinephrine_threshold}")
        
        if trust_score < self.trust_threshold:
            reasons.append(f"trust {trust_score} < {self.trust_threshold}")

        if not reasons:
            return None

        severity = "critical" if len(reasons) >= 2 or epi > 95.0 else "standard"
        return AnomalyReport(
            dock_name=dock_name,
            severity=severity,
            reasons=reasons,
            nte_snapshot=nte_state,
        )
