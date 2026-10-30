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
# MODULE START : uro.nte.reward
# ---------------------------------------------------------------------
# FILE         : uro/nte/reward.py
# PURPOSE      : D1/D2 reward-punishment semantics, habit formation, and
#                bi-directional R/P fault tracing (RFC 31, 32).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"D1/D2 reward-punishment, habit formation, bi-directional R/P (RFC 31/32)."

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

__all__ = ["RewardOutcome", "reward_event", "is_habit", "habit_broken",
           "propagate_rp", "HABIT_TRUST_THRESHOLD"]

HABIT_TRUST_THRESHOLD = 90.0


@dataclass
class RewardOutcome:
    "PURPOSE: Typed D1/D2 result (RFC 31.1)."
    kind: str
    stimulation_factor: float
    trust_delta: float
    action_directive: str


def reward_event(success: bool, trust_weight: float = 1.0) -> RewardOutcome:
    "PURPOSE: D1 reward vs D2 punishment, trust-weighted (RFC 31.2.4)."
    w = max(0.0, float(trust_weight))
    if success:
        return RewardOutcome("D1", 1.0 + 0.5 * w, 1.0 * w, "affirm")
    return RewardOutcome("D2", max(0.1, 1.0 - 0.5 * w), -1.0 * w, "reconsider")


def is_habit(trust: float, threshold: float = HABIT_TRUST_THRESHOLD) -> bool:
    "PURPOSE: RFC 32.1: trust so high it becomes the go-to firing mechanism."
    return trust >= threshold


def habit_broken(habit_strength: float, new_rp_magnitude: float) -> bool:
    "PURPOSE: RFC 32.2: habit breaks only when new R/P outweighs the old."
    return new_rp_magnitude > habit_strength


def propagate_rp(chain: List[str], fault_index: Optional[int], reward: bool) -> dict:
    "PURPOSE: RFC 32.3 bi-directional R/P; punishment stops at fault else cascades."
    deltas = {node: 0.0 for node in chain}
    if reward:
        for node in chain:
            deltas[node] = 1.0
        return deltas
    if fault_index is None:
        for node in chain:
            deltas[node] = -1.0
        return deltas
    stop = max(fault_index + 1, len(chain) - 1)
    for node in chain[fault_index:stop]:
        deltas[node] = -1.0
    return deltas
# =====================================================================
# MODULE END   : uro.nte.reward
# =====================================================================
