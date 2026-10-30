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
# MODULE START : uro.phases.opar
# ---------------------------------------------------------------------
# FILE         : uro/phases/opar.py
# PURPOSE      : The OPAR lifecycle - Observe, Plan, Act, Review.
# STANDARD     : URO-STD-0001 S8
# =====================================================================
"""OPAR - the four-phase lifecycle of an active URO."""

from __future__ import annotations

from collections import deque
from enum import Enum, auto
from typing import Any, Deque, List, Optional

from uro.core.uro import URO

__all__ = ["OPARPhase", "OPARCycle"]


class OPARPhase(Enum):
    """The four OPAR lifecycle phases."""
    OBSERVE = auto()
    PLAN = auto()
    ACT = auto()
    REVIEW = auto()


class OPARCycle:
    """Drives a URO through Observe -> Plan -> Act -> Review."""

    def __init__(self, uro: URO) -> None:
        """Bind an OPAR cycle to a URO."""
        self.uro = uro
        self.phase: OPARPhase = OPARPhase.OBSERVE
        self.input_queue: Deque[Any] = deque()
        self.history: List[OPARPhase] = []
        self._observations: List[Any] = []
        self._plan: Optional[Any] = None

    def observe(self) -> List[Any]:
        """Observe internal state and external inputs."""
        self.phase = OPARPhase.OBSERVE
        observations: List[Any] = []
        while self.input_queue:
            observations.append(self.input_queue.popleft())
        observations.append({
            "self": repr(self.uro),
            "children": len(self.uro.children),
            "associations": len(self.uro.associations),
        })
        self._observations = observations
        self.history.append(OPARPhase.OBSERVE)
        return observations

    def plan(self) -> Any:
        """Plan how to process the current observations."""
        self.phase = OPARPhase.PLAN
        self._plan = {"observations": len(self._observations),
                      "strategy": "process-all"}
        self.history.append(OPARPhase.PLAN)
        return self._plan

    def act(self) -> Any:
        """Act on the plan, producing output."""
        self.phase = OPARPhase.ACT
        result = {"processed": len(self._observations), "plan": self._plan}
        self.history.append(OPARPhase.ACT)
        return result

    def review(self) -> Any:
        """Review the outcome, evaluate, improve."""
        self.phase = OPARPhase.REVIEW
        summary = {"phases_run": len(self.history),
                   "processed": len(self._observations),
                   "status": "ok"}
        self.history.append(OPARPhase.REVIEW)
        self._observations = []
        self._plan = None
        return summary

    def enqueue(self, stimulus: Any) -> None:
        """Add an external stimulus to the input queue."""
        self.input_queue.append(stimulus)

    def run(self, iterations: int = 1) -> List[Any]:
        """Run the full OPAR cycle one or more times."""
        summaries = []
        for _ in range(iterations):
            self.observe()
            self.plan()
            self.act()
            summaries.append(self.review())
        return summaries
# =====================================================================
# MODULE END   : uro.phases.opar
# =====================================================================
