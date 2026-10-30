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

from typing import Any, Dict
from uro.nte.axes import NTEAxis

# Map legacy names to canonical NTEAxis values
LEGACY_MAP: Dict[str, str] = {
    "glu": "glutamate", "excitation": "glutamate",
    "inhibition": "gaba", "inhibitory": "gaba",
    "reward": "dopamine", "reward_learning": "dopamine",
    "decision": "serotonin", "patience": "serotonin",
    "plasticity": "acetylcholine",
    "endocannabinoid": "cannabinoid", "ecb": "cannabinoid", "forgetting": "cannabinoid",
    "consolidation": "melatonin",
    "sleep_pressure": "adenosine", "fatigue": "adenosine",
    "stress_acute": "epinephrine", "urgency": "epinephrine",
    "stress_chronic": "cortisol",
    "arousal": "norepinephrine", "noradrenaline": "norepinephrine",
    "trust": "oxytocin", "bonding": "oxytocin",
    "focus": "focus", "attention": "focus",
    "creativity": "creativity",
    "analysis": "analysis_depth", "analysis_depth": "analysis_depth",
    "pattern": "pattern_recognition", "pattern_recognition": "pattern_recognition",
    "abstraction": "abstraction_level", "abstraction_level": "abstraction_level",
    "inference": "inference_speed", "inference_speed": "inference_speed",
    "uncertainty": "uncertainty_tolerance", "uncertainty_tolerance": "uncertainty_tolerance",
    "flexibility": "cognitive_flexibility", "cognitive_flexibility": "cognitive_flexibility",
    "metacognition": "metacognition",
    "analogy": "analogical_transfer", "analogical_transfer": "analogical_transfer",
    "dialectical": "dialectical_balance", "dialectical_balance": "dialectical_balance",
    "insight": "insight_readiness", "insight_readiness": "insight_readiness",
}

BASELINE = 50.0

def normalize_nte_state(partial_state: Any = None) -> Dict[str, Any]:
    """
    S4.3 backwards-compatible normalizer.
    Returns a dict with 'levels' (uppercase canonical axis names) and 'axis_count'.
    """
    levels = {axis.value: BASELINE for axis in NTEAxis}
    
    if partial_state is None:
        raw = {}
    elif isinstance(partial_state, dict):
        raw = partial_state.get("levels", partial_state)
    elif hasattr(partial_state, "levels"):
        raw = getattr(partial_state, "levels", {})
        if isinstance(raw, dict):
            raw = {k.value if hasattr(k, 'value') else str(k): v for k, v in raw.items()}
    else:
        raw = {}

    if not isinstance(raw, dict):
        raw = {}

    for key, value in raw.items():
        canonical_key = str(key).strip().lower().replace("-", "_").replace(" ", "_")
        if canonical_key in LEGACY_MAP:
            canonical_key = LEGACY_MAP[canonical_key]
        
        if canonical_key in levels:
            try:
                levels[canonical_key] = max(0.0, min(100.0, float(value)))
            except (ValueError, TypeError):
                levels[canonical_key] = BASELINE

    # Convert to uppercase keys for S4.2 canonical representation
    upper_levels = {k.upper(): v for k, v in levels.items()}
    return {
        "levels": upper_levels,
        "axis_count": 24,
    }
