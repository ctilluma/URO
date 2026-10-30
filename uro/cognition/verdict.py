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


"""
MODULE: Verdict Dynamics
INTENT: Holds a verdict DISTRIBUTION over time (not a locked decision) plus
        its rate of change, entropy, and a meta-verdict. This is how the swarm
        avoids cognitive dissonance: it knows when to re-examine.
STANDARD: URO-STD-0001 S24

WHY: Humans lock a verdict and defend it against new data. The swarm instead
     holds P(verdict|evidence) and its dynamics, and triggers re-evaluation
     when the distribution is actively shifting or uncertainty is rising.
"""
from __future__ import annotations
import math
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict

from uro.core.urid import URID
from uro.security.hashing import inahash

__all__ = ["VerdictDynamics"]


class VerdictDynamics(BaseModel):
    """A verdict held as a living distribution with dynamics."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    urid1: URID = Field(...)
    urid2: URID = Field(...)

    # The current distribution over outcomes
    current: Dict[str, float] = Field(default_factory=dict)
    # Historical snapshots (for dynamics)
    history: List[Dict[str, float]] = Field(default_factory=list)

    inahash: str = Field(default="")

    # --- Dynamics ---
    def update(self, dist: Dict[str, float]) -> None:
        """Record a new distribution snapshot."""
        self.history.append(self.current)
        self.current = dist

    def entropy(self, dist: Optional[Dict[str, float]] = None) -> float:
        d = dist if dist is not None else self.current
        e = 0.0
        for p in d.values():
            if p > 0:
                e -= p * math.log2(p)
        return e

    def delta_p(self) -> float:
        """Total-variation distance between the last two snapshots (dP/dt)."""
        if not self.history:
            return 0.0
        prev = self.history[-1]
        keys = set(prev) | set(self.current)
        return 0.5 * sum(abs(self.current.get(k, 0) - prev.get(k, 0)) for k in keys)

    def entropy_rate(self) -> float:
        if not self.history:
            return 0.0
        return self.entropy() - self.entropy(self.history[-1])

    def meta_verdict(self) -> str:
        """Classify the current belief state."""
        e = self.entropy()
        er = self.entropy_rate()
        dp = self.delta_p()
        if dp > 0.2:
            return "shifting"
        if e > 1.5 and er > 0:
            return "destabilizing"
        if e > 1.0 and er <= 0:
            return "consolidating"
        return "stable"

    def should_reevaluate(self, orthogonal_evidence: bool = False) -> bool:
        """Trigger deeper re-examination when the belief state demands it."""
        return (
            self.delta_p() > 0.2
            or self.entropy_rate() > 0
            or orthogonal_evidence
        )

    def top(self) -> Optional[str]:
        if not self.current:
            return None
        return max(self.current, key=self.current.get)

    def seal(self) -> None:
        data = self.model_dump(exclude={"inahash"})
        self.inahash = inahash(str(data).encode()).hex()
