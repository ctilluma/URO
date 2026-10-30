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
# MODULE START : uro.learning.cas_loop
# ---------------------------------------------------------------------
# FILE         : uro/learning/cas_loop.py
# PURPOSE      : VTA-CAS loop: Context-Association-System linking context
#                to reward for predictive behavior (RFC 33, 100).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"VTA-CAS context-association-reward loop (RFC 33, 100)."

from __future__ import annotations

from collections import defaultdict
from typing import List

__all__ = ["CASLoop"]


class CASLoop:
    "PURPOSE: Link contexts to rewards enabling predictive behavior."

    def __init__(self) -> None:
        self._rewards = defaultdict(list)

    def associate(self, context: str, reward: float) -> None:
        "PURPOSE: Record one context-reward pairing (VTA reward circuit)."
        self._rewards[context].append(float(reward))

    def predict(self, context: str) -> float:
        "PURPOSE: Expected reward for a context (mean of associations)."
        vals = self._rewards.get(context)
        if not vals:
            return 0.0
        return sum(vals) / len(vals)

    def prediction_error(self, context: str, actual: float) -> float:
        "PURPOSE: VTA reward-prediction-error for novel/unexpected rewards."
        return float(actual) - self.predict(context)
# =====================================================================
# MODULE END   : uro.learning.cas_loop
# =====================================================================
