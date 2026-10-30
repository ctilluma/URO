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
# MODULE START : uro.nte.ans
# ---------------------------------------------------------------------
# FILE         : uro/nte/ans.py
# PURPOSE      : Autonomic Nervous System branch mapping and involuntary
#                regulation thresholds (RFC 34).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"Autonomic Nervous System branch mapping and thresholds (RFC 34)."

from __future__ import annotations

from typing import Dict, List

from uro.nte.axes import NTEAxis

__all__ = ["SYMPATHETIC_AXES", "PARASYMPATHETIC_AXES", "dominant_branch",
           "regulation_actions", "LOAD_SHED_THRESHOLD",
           "CONSOLIDATION_THRESHOLD"]

LOAD_SHED_THRESHOLD = 70.0
CONSOLIDATION_THRESHOLD = 70.0

# RFC 34.3 branch drivers.
SYMPATHETIC_AXES = (NTEAxis.EPINEPHRINE, NTEAxis.NOREPINEPHRINE,
                    NTEAxis.CORTISOL, NTEAxis.GLUTAMATE)
PARASYMPATHETIC_AXES = (NTEAxis.MELATONIN, NTEAxis.SEROTONIN,
                        NTEAxis.ADENOSINE, NTEAxis.CANNABINOID)


def _get(levels: Dict, axis: NTEAxis) -> float:
    "PURPOSE: Tolerant level lookup for enum- or string-keyed states."
    value = levels.get(axis)
    if value is None:
        value = levels.get(axis.value, 50.0)
    return float(value)


def _branch_score(levels: Dict, axes) -> float:
    "PURPOSE: Mean level over a branch axis set (RFC 34.2)."
    return sum(_get(levels, a) for a in axes) / len(axes)


def dominant_branch(levels: Dict) -> str:
    "PURPOSE: Classify fight/flight vs rest/digest from levels (RFC 34.3)."
    sym = _branch_score(levels, SYMPATHETIC_AXES)
    par = _branch_score(levels, PARASYMPATHETIC_AXES)
    if sym == par:
        return "balanced"
    return "sympathetic" if sym > par else "parasympathetic"


def regulation_actions(levels: Dict) -> List[str]:
    "PURPOSE: Threshold-driven involuntary actions (RFC 34.3 items 3-4)."
    actions = []
    if _get(levels, NTEAxis.ADENOSINE) > LOAD_SHED_THRESHOLD:
        actions.append("load_shedding")
    if _get(levels, NTEAxis.MELATONIN) > CONSOLIDATION_THRESHOLD:
        actions.append("consolidation_window")
    branch = dominant_branch(levels)
    if branch == "sympathetic":
        actions.append("fight_flight")
    elif branch == "parasympathetic":
        actions.append("rest_digest")
    return actions
# =====================================================================
# MODULE END   : uro.nte.ans
# =====================================================================
