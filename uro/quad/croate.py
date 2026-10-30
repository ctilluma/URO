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
# MODULE START : uro.quad.croate
# ---------------------------------------------------------------------
# FILE         : uro/quad/croate.py
# PURPOSE      : CROATE personality model: six traits with canonical NTE
#                axis mappings (RFC 47).
# STANDARD     : URO-STD-0001 S-Quad
# =====================================================================
"CROATE personality model and NTE mappings (RFC 47)."

from __future__ import annotations

from enum import Enum
from typing import Dict

from uro.nte.axes import NTEAxis

__all__ = ["CROATE", "TRAIT_NTE_MAP", "trait_from_nte"]


class CROATE(str, Enum):
    "PURPOSE: The six personality traits (RFC 47)."
    CONSCIENTIOUSNESS = "conscientiousness"
    REWARD = "reward"
    OPENNESS = "openness"
    AGREEABLENESS = "agreeableness"
    TRUST = "trust"
    EXTRAVERSION = "extraversion"


TRAIT_NTE_MAP = {
    CROATE.CONSCIENTIOUSNESS: (NTEAxis.FOCUS, NTEAxis.METACOGNITION),
    CROATE.REWARD: (NTEAxis.DOPAMINE, NTEAxis.SEROTONIN),
    CROATE.OPENNESS: (NTEAxis.COGNITIVE_FLEXIBILITY, NTEAxis.UNCERTAINTY_TOLERANCE),
    CROATE.AGREEABLENESS: (NTEAxis.OXYTOCIN,),
    CROATE.TRUST: (NTEAxis.OXYTOCIN,),
    CROATE.EXTRAVERSION: (NTEAxis.NOREPINEPHRINE,),
}


def trait_from_nte(levels: Dict) -> Dict[CROATE, float]:
    "PURPOSE: Derive six trait scores as means of mapped NTE axes (RFC 47)."
    out: Dict[CROATE, float] = {}
    for trait, axes in TRAIT_NTE_MAP.items():
        vals = []
        for axis in axes:
            v = levels.get(axis)
            if v is None:
                v = levels.get(axis.value, 50.0)
            vals.append(float(v))
        out[trait] = sum(vals) / len(vals)
    return out
# =====================================================================
# MODULE END   : uro.quad.croate
# =====================================================================
