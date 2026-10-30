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
# MODULE START : uro.nte.firing
# ---------------------------------------------------------------------
# FILE         : uro/nte/firing.py
# PURPOSE      : Firing calculation, signal transmission, and
#                potentiator/receptor mechanics (RFC 29, 30).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"Firing calculation and potentiator/receptor mechanics (RFC 29/30)."

from __future__ import annotations

__all__ = ["fire_decision", "transmit_signal", "fire_multiplier",
           "activity", "min_fire_chance", "max_fire_chance"]


def fire_decision(chance_pct: float, rand_1_100: float) -> bool:
    "PURPOSE: RFC 29.1: fire when the random draw is at or below the chance."
    return rand_1_100 <= chance_pct


def transmit_signal(fires_fraction: float) -> float:
    "PURPOSE: RFC 29.2: transmit signal in the 0-2 range (fires fraction x 2)."
    return max(0.0, min(1.0, fires_fraction)) * 2.0


def fire_multiplier(fired: bool) -> float:
    "PURPOSE: RFC 29.2: 1.06 when fired else 0.40."
    return 1.06 if fired else 0.40


def activity(antagonists: float, protagonists: float) -> float:
    "PURPOSE: RFC 30.2: Activity = antagonists - protagonists."
    return antagonists - protagonists


def min_fire_chance(antagonists: float, receptors: float) -> float:
    "PURPOSE: RFC 30.3 min bound percent; 0 when antags exceed receptors."
    if receptors <= 0:
        return 0.0
    if antagonists > receptors:
        return 0.0
    return (antagonists / receptors) * 100.0


def max_fire_chance(protagonists: float, receptors: float) -> float:
    "PURPOSE: RFC 30.3 max bound percent; 100 when protags exceed receptors."
    if receptors <= 0:
        return 100.0
    if protagonists > receptors:
        return 100.0
    return (protagonists / receptors) * 100.0
# =====================================================================
# MODULE END   : uro.nte.firing
# =====================================================================
