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


# === START: uro_nte_normalizer ===
from __future__ import annotations
from typing import Dict, List, Optional

BASELINE = 50.0
CLAMP_MIN = 0.0
CLAMP_MAX = 100.0
CANONICAL_24_AXES: List[str] = [
    "GLUTAMATE","GABA","DOPAMINE","SEROTONIN","ACETYLCHOLINE",
    "NOREPINEPHRINE","EPINEPHRINE","CORTISOL","OXYTOCIN",
    "CANNABINOID","MELATONIN","ADENOSINE",
    "FOCUS","CREATIVITY","ANALYSIS_DEPTH","PATTERN_RECOGNITION",
    "ABSTRACTION_LEVEL","INFERENCE_SPEED","UNCERTAINTY_TOLERANCE",
    "COGNITIVE_FLEXIBILITY","METACOGNITION","ANALOGICAL_TRANSFER",
    "DIALECTICAL_BALANCE","INSIGHT_READINESS",
]
BIOLOGICAL_AXES = CANONICAL_24_AXES[:12]
COGNITIVE_AXES  = CANONICAL_24_AXES[12:]
_CANONICAL_SET  = set(CANONICAL_24_AXES)
ALIAS_MAP: Dict[str,str] = {a.lower(): a for a in CANONICAL_24_AXES}
ALIAS_MAP.update({
    "glu":"GLUTAMATE","glut":"GLUTAMATE","da":"DOPAMINE","dopa":"DOPAMINE",
    "5ht":"SEROTONIN","5_ht":"SEROTONIN","ser":"SEROTONIN","ach":"ACETYLCHOLINE",
    "ne":"NOREPINEPHRINE","noradrenaline":"NOREPINEPHRINE","epi":"EPINEPHRINE",
    "adrenaline":"EPINEPHRINE","cort":"CORTISOL","stress":"CORTISOL",
    "oxy":"OXYTOCIN","ot":"OXYTOCIN","cbd":"CANNABINOID","endocannabinoid":"CANNABINOID",
    "ecb":"CANNABINOID","anandamide":"CANNABINOID","mel":"MELATONIN",
    "ado":"ADENOSINE","fatigue":"ADENOSINE","analysis":"ANALYSIS_DEPTH",
    "depth":"ANALYSIS_DEPTH","pattern":"PATTERN_RECOGNITION","abstraction":"ABSTRACTION_LEVEL",
    "inference":"INFERENCE_SPEED","uncertainty":"UNCERTAINTY_TOLERANCE",
    "flexibility":"COGNITIVE_FLEXIBILITY","analogy":"ANALOGICAL_TRANSFER",
    "transfer":"ANALOGICAL_TRANSFER","dialectic":"DIALECTICAL_BALANCE","insight":"INSIGHT_READINESS",
})
def _resolve(key) -> Optional[str]:
    k = str(key).strip().lower().replace(" ","_").replace("-","_")
    if k in ALIAS_MAP: return ALIAS_MAP[k]
    up = k.upper()
    return up if up in _CANONICAL_SET else None
def clamp_state(state):
    return {k: max(CLAMP_MIN, min(CLAMP_MAX, float(v))) for k,v in state.items()}
def normalize_nte_state(partial_state: Optional[Dict[str,float]] = None) -> Dict[str,float]:
    out = {a: BASELINE for a in CANONICAL_24_AXES}
    for key, val in (partial_state or {}).items():
        axis = _resolve(key)
        if axis is None: continue
        try: out[axis] = float(val)
        except (TypeError, ValueError): continue
    return clamp_state(out)
def apply_cross_talk(state):
    s = normalize_nte_state(state)
    excess = (s["GLUTAMATE"] - s["GABA"]) - 20.0
    if excess > 0:
        s["GLUTAMATE"] -= 0.10*excess
        s["GABA"]      += 0.10*excess
    s["OXYTOCIN"]    -= 0.15*max(0.0, s["CORTISOL"]-50.0)
    s["CORTISOL"]    -= 0.10*max(0.0, s["MELATONIN"]-50.0)
    s["DOPAMINE"]    -= 0.10*max(0.0, s["ADENOSINE"]-50.0)
    s["EPINEPHRINE"] -= (0.10*max(0.0, s["OXYTOCIN"]-50.0) + 0.05*max(0.0, s["GABA"]-50.0))
    return clamp_state(s)
def decay_state(state, rate: float = 0.02):
    s = normalize_nte_state(state)
    return clamp_state({k: v + (BASELINE - v)*rate for k,v in s.items()})
def nte_vector(state):
    s = normalize_nte_state(state)
    return [s[a] for a in CANONICAL_24_AXES]
__all__ = ["BASELINE","CANONICAL_24_AXES","BIOLOGICAL_AXES","COGNITIVE_AXES",
           "normalize_nte_state","apply_cross_talk","decay_state","clamp_state","nte_vector"]
# === END: uro_nte_normalizer ===
