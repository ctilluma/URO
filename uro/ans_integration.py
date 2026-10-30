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
V.A.U.R.O.S. Core URO Library - ANS Integration Mixin
Provides automatic ANS lifecycle management for any FastAPI dock.

Usage in any dock's api.py:
    from uro.ans_integration import ANSIntegrationMixin
    
    class MyDockApp(ANSIntegrationMixin):
        dock_name = "my_dock"
        
    # Or use the standalone functions:
    from uro.ans_integration import setup_ans, get_ans, apply_stress
"""
import asyncio
import logging
from typing import Dict, Optional
from uro.autonomic_nervous_system import AutonomicNervousSystem, get_ans_for_dock

logger = logging.getLogger("VAUROS.ANS.INTEGRATION")

# Global registry for dock ANS instances
_dock_ans_instances: Dict[str, AutonomicNervousSystem] = {}


def setup_ans(dock_name: str, **kwargs) -> AutonomicNervousSystem:
    """
    Create and register an ANS for a dock.
    Call this during dock startup.
    
    Args:
        dock_name: Unique identifier for the dock
        **kwargs: Custom baselines, spring_constant, damping_coefficient, tick_rate
        
    Returns:
        The ANS instance for this dock
    """
    if dock_name not in _dock_ans_instances:
        _dock_ans_instances[dock_name] = AutonomicNervousSystem(dock_name, **kwargs)
        logger.info(f"[{dock_name}] ANS registered via integration layer")
    return _dock_ans_instances[dock_name]


async def start_ans(dock_name: str):
    """Start the ANS regulation loop for a dock."""
    if dock_name in _dock_ans_instances:
        await _dock_ans_instances[dock_name].start()
    else:
        logger.warning(f"[{dock_name}] ANS not registered. Call setup_ans first.")


async def stop_ans(dock_name: str):
    """Stop the ANS regulation loop for a dock."""
    if dock_name in _dock_ans_instances:
        await _dock_ans_instances[dock_name].stop()


def get_ans(dock_name: str) -> Optional[AutonomicNervousSystem]:
    """Get the ANS instance for a dock."""
    return _dock_ans_instances.get(dock_name)


def apply_stress(dock_name: str, intensity: float = 50.0):
    """Apply stress stimulus to a dock's ANS."""
    if dock_name in _dock_ans_instances:
        _dock_ans_instances[dock_name].apply_stress(intensity)


def apply_reward(dock_name: str, intensity: float = 20.0):
    """Apply reward stimulus to a dock's ANS."""
    if dock_name in _dock_ans_instances:
        _dock_ans_instances[dock_name].apply_reward(intensity)


def get_stress_level(dock_name: str) -> str:
    """Get current stress level for a dock."""
    if dock_name in _dock_ans_instances:
        return _dock_ans_instances[dock_name].get_stress_level()
    return "UNKNOWN"


def is_at_homeostasis(dock_name: str) -> bool:
    """Check if a dock is at homeostasis."""
    if dock_name in _dock_ans_instances:
        return _dock_ans_instances[dock_name].is_at_homeostasis()
    return False


def get_all_dock_states() -> Dict[str, Dict]:
    """Get ANS state for all registered docks."""
    return {
        name: ans.get_full_diagnostic() 
        for name, ans in _dock_ans_instances.items()
    }


class ANSIntegrationMixin:
    """
    Mixin class that provides automatic ANS lifecycle management.
    
    Any dock that inherits from this mixin gets:
    - Automatic ANS creation on init
    - Automatic ANS startup/shutdown
    - Convenience methods for stress/reward application
    """
    
    dock_name: str = "unknown_dock"
    _ans: Optional[AutonomicNervousSystem] = None
    
    def setup_ans(self, **kwargs):
        """Initialize the ANS for this dock."""
        self._ans = setup_ans(self.dock_name, **kwargs)
        return self._ans
    
    async def start_ans(self):
        """Start the ANS regulation loop."""
        if self._ans:
            await self._ans.start()
    
    async def stop_ans(self):
        """Stop the ANS regulation loop."""
        if self._ans:
            await self._ans.stop()
    
    @property
    def ans(self) -> Optional[AutonomicNervousSystem]:
        """Get the ANS instance."""
        return self._ans
    
    def apply_stress(self, intensity: float = 50.0):
        """Apply stress to this dock."""
        if self._ans:
            self._ans.apply_stress(intensity)
    
    def apply_reward(self, intensity: float = 20.0):
        """Apply reward to this dock."""
        if self._ans:
            self._ans.apply_reward(intensity)
    
    @property
    def stress_level(self) -> str:
        """Current stress level."""
        if self._ans:
            return self._ans.get_stress_level()
        return "UNKNOWN"
    
    @property
    def is_homeostatic(self) -> bool:
        """Whether this dock is at homeostasis."""
        if self._ans:
            return self._ans.is_at_homeostasis()
        return False
