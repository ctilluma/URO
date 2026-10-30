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

BIOLOGICAL_AXES = ("dopamine", "serotonin", "norepinephrine", "acetylcholine",
    "glutamate", "gaba", "endorphins", "oxytocin", "cortisol", "adrenaline", "melatonin", "anandamide")
COGNITIVE_AXES = ("focus", "creativity", "memory_retrieval", "pattern_recognition",
    "abstract_reasoning", "temporal_processing", "spatial_navigation", "language_processing",
    "emotional_regulation", "metacognition", "attention_control", "decision_confidence")
AXES_24 = BIOLOGICAL_AXES + COGNITIVE_AXES
BASELINE, CLAMP_MIN, CLAMP_MAX = 50.0, 0.0, 100.0

class NTEAxis:
    """Iterable over the 24 canonical axis names."""
    def __init__(self, name: str = "default", baseline: float = BASELINE):
        self.name, self.baseline, self.value = name, baseline, baseline
    def clamp(self): self.value = max(CLAMP_MIN, min(CLAMP_MAX, self.value))
    @classmethod
    def default(cls): return cls()
    def __iter__(self): return iter(AXES_24)
    def __len__(self): return len(AXES_24)

def normalize_nte_state(state):
    if isinstance(state, dict):
        return {axis: state.get(axis, BASELINE) for axis in AXES_24}
    return state
