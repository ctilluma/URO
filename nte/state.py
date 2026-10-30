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


"""
Canonical NTE State Module (RFC S1.4, S24)
Provides the NTEStateURO class for managing 24-axis neurochemical state.
"""
from __future__ import annotations

from typing import Dict, Optional
try:
    from uro.nte.axes import AXES_24, BASELINE, CLAMP_MIN, CLAMP_MAX
except ImportError:
    AXES_24 = ("dopamine", "serotonin", "norepinephrine", "acetylcholine",
               "glutamate", "gaba", "endorphins", "oxytocin",
               "cortisol", "adrenaline", "melatonin", "anandamide",
               "focus", "creativity", "memory_retrieval", "pattern_recognition",
               "abstract_reasoning", "temporal_processing", "spatial_navigation",
               "language_processing", "emotional_regulation", "metacognition",
               "attention_control", "decision_confidence")
    BASELINE = 50.0
    CLAMP_MIN = 0.0
    CLAMP_MAX = 100.0

# If the real URO library has a Pydantic NTEStateURO, we yield to it.
# Otherwise, we provide a fallback.
try:
    # Try to import the real one first
    from uro.core.ntestate import NTEStateURO as _RealNTEStateURO
    NTEStateURO = _RealNTEStateURO
except ImportError:
    class NTEStateURO:
        def __init__(self, urid1: str = "0000000000000000000000000000000000000000000000000000000000000000", 
                     urid2: str = "0000000000000000000000000000000000000000000000000000000000000000"):
            self.urid1 = urid1
            self.urid2 = urid2
            self.levels: Dict[str, float] = {axis: BASELINE for axis in AXES_24}

        def clamp(self) -> None:
            for axis in self.levels:
                self.levels[axis] = max(CLAMP_MIN, min(CLAMP_MAX, self.levels[axis]))

        def to_dict(self) -> Dict[str, float]:
            return dict(self.levels)
