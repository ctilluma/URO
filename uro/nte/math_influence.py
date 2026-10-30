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
# MODULE START : uro.nte.math_influence
# ---------------------------------------------------------------------
# FILE         : uro/nte/math_influence.py
# PURPOSE      : Weighting curves and reward/punishment cost formulas
#                (RFC 27, 27.1).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"Weighting curves and reward/punishment formulas (RFC 27)."

from __future__ import annotations

import math
from enum import Enum

__all__ = ["InfluenceType", "apply_influence", "reward_motivation",
           "punish_motivation", "cost_to_buy"]


class InfluenceType(str, Enum):
    "PURPOSE: The seven canonical influence curves (RFC 27)."
    DOMINATING = "dominating"
    STANDARD = "standard"
    MILD = "mild"
    WEAK = "weak"
    NONE = "none"
    WEAK_NEGATIVE = "weak_negative"
    MILD_NEGATIVE = "mild_negative"


def _mild_mag(x: float) -> float:
    "PURPOSE: sin(x*log(x-10)/128)*x with domain guard x>10 (RFC 27)."
    if x <= 10.0:
        return 0.0
    return math.sin(x * math.log(x - 10.0) / 128.0) * x


def _weak_mag(x: float) -> float:
    "PURPOSE: sin(x/128)*x (RFC 27)."
    return math.sin(x / 128.0) * x


def apply_influence(kind: InfluenceType, x: float) -> float:
    "PURPOSE: Evaluate the canonical weighting curve delta for x (RFC 27)."
    if kind == InfluenceType.DOMINATING:
        return x * math.log10(x + 10.0)
    if kind == InfluenceType.STANDARD:
        return x
    if kind == InfluenceType.MILD:
        return _mild_mag(x)
    if kind == InfluenceType.WEAK:
        return _weak_mag(x)
    if kind == InfluenceType.NONE:
        return 0.0
    if kind == InfluenceType.WEAK_NEGATIVE:
        return -_weak_mag(x)
    return -_mild_mag(x)


def reward_motivation(motivation: float, x: float) -> float:
    "PURPOSE: RFC 27.1 reward: Motivation += x*log10(X+10)."
    return motivation + apply_influence(InfluenceType.DOMINATING, x)


def punish_motivation(motivation: float, dopamine: float) -> float:
    "PURPOSE: RFC 27.1 punishment: Motivation += dopamine (decrease)."
    return motivation + dopamine


def cost_to_buy(points: float) -> float:
    "PURPOSE: RFC 27.1 marketplace cost (log10(X^3)^2)/3 capped at 100 points."
    raw = (math.log10(max(1e-9, points ** 3)) ** 2) / 3.0
    return min(100.0, raw)
# =====================================================================
# MODULE END   : uro.nte.math_influence
# =====================================================================
