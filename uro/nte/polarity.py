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
# MODULE START : uro.nte.polarity
# ---------------------------------------------------------------------
# FILE         : uro/nte/polarity.py
# PURPOSE      : Polarity table for all 24 NTE axes: negative/antagonist
#                and positive/protagonist descriptors (RFC 25.1/25.2).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"Polarity table for all 24 NTE axes (RFC 25)."

from __future__ import annotations

from typing import Dict, Tuple

from uro.nte.axes import NTEAxis

__all__ = ["POLARITY", "polarity_for"]

# RFC 25.1 biological and 25.2 cognitive descriptors, verbatim.
_RAW = {
    "glutamate": ("Conservative, reduced activation", "Strong excitation, active learning"),
    "gaba": ("Inhibitory, reduce likelihood", "Excitatory, increase likelihood"),
    "dopamine": ("Punishment", "Reward"),
    "serotonin": ("Wanting, scarce resources", "Satisfaction, bountiful resources"),
    "acetylcholine": ("Aversion, do not want to do", "Desire, want to do"),
    "norepinephrine": ("Internal focus, optimization", "External focus, exploration"),
    "epinephrine": ("Fear, flight, overwhelmed", "Confidence, consistent performance"),
    "cortisol": ("Chronic stress, resource reallocation", "Calm, normal operation"),
    "oxytocin": ("Disconnected, unlikely to fulfill", "Together, likely to fulfill"),
    "cannabinoid": ("Attached, need to save", "Unattached, need to purge"),
    "melatonin": ("Active processing mode", "Consolidation, maintenance window"),
    "adenosine": ("Full resources, alert", "Fatigue, shed load, power-save"),
    "focus": ("Distributed attention, scanning", "Tunnel focus, deep concentration"),
    "creativity": ("Convergent, routine, established", "Divergent, novel, unconventional"),
    "analysis_depth": ("Surface heuristic, shallow", "Deep recursion, multi-layer"),
    "pattern_recognition": ("Misses correlations", "Detects subtle structures"),
    "abstraction_level": ("Concrete details, instances", "Abstract principles, schemas"),
    "inference_speed": ("Deliberate, slow, thorough", "Rapid conclusions"),
    "uncertainty_tolerance": ("Requires certainty, cautious", "Acts on partial data, explores"),
    "cognitive_flexibility": ("Rigid, locked to current model", "Rapid re-framing, strategy switch"),
    "metacognition": ("Blind to own errors", "Self-monitoring, self-correcting"),
    "analogical_transfer": ("Domain-locked", "Cross-domain mapping, free transfer"),
    "dialectical_balance": ("Binary thinking, one side", "Synthesizes contradictions"),
    "insight_readiness": ("Far from insight, still gathering", "On verge of breakthrough"),
}

POLARITY: Dict[NTEAxis, Tuple[str, str]] = {NTEAxis(k): v for k, v in _RAW.items()}


def polarity_for(axis: NTEAxis) -> Tuple[str, str]:
    "PURPOSE: Return (negative/antagonist, positive/protagonist) descriptors (RFC 25)."
    return POLARITY[axis]
# =====================================================================
# MODULE END   : uro.nte.polarity
# =====================================================================
