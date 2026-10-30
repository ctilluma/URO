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
V.A.U.R.O.S. Autonomic Nervous System (ANS)
Manages neurotransmitter equivalents (NTE) for all docks.
"""
import math
import logging

logger = logging.getLogger("VAUROS.ANS")

class AutonomicNervousSystem:
    """Manages NTE vectors and autonomic responses."""
    
    def __init__(self, dock_name: str):
        self.dock_name = dock_name
        self.nte = {
            "dopamine": 50.0,
            "serotonin": 50.0,
            "epinephrine": 0.0,
            "cannabinoid": 0.0,
            "oxytocin": 0.0,
            "norepinephrine": 0.0,
            "acetylcholine": 50.0,
            "gaba": 0.0
        }
    
    def modulate_neurotransmitter(self, name: str, delta: float):
        """Modulate a specific neurotransmitter."""
        if name in self.nte:
            self.nte[name] = max(0.0, min(100.0, self.nte[name] + delta))
            logger.debug(f"[{self.dock_name}] {name}: {self.nte[name]:.1f}")
    
    def apply_reward(self, intensity: float):
        """Apply dopamine reward based on intensity."""
        dopamine_gain = intensity * math.log10(intensity + 10)
        self.modulate_neurotransmitter("dopamine", dopamine_gain)
        self.modulate_neurotransmitter("serotonin", intensity * 0.1)
        self.modulate_neurotransmitter("epinephrine", -intensity * 0.5)
    
    def apply_punishment(self, intensity: float):
        """Apply epinephrine punishment based on intensity."""
        self.modulate_neurotransmitter("epinephrine", intensity)
        self.modulate_neurotransmitter("dopamine", -intensity * 0.5)
    
    def get_nte_snapshot(self) -> dict:
        """Return current NTE vector."""
        return self.nte.copy()
    
    def is_stressed(self) -> bool:
        """Check if dock is under stress."""
        return self.nte.get("epinephrine", 0) > 70.0
    
    def is_idle(self) -> bool:
        """Check if dock is idle and safe."""
        return (self.nte.get("epinephrine", 0) < 20.0 and 
                self.nte.get("serotonin", 0) > 60.0)
