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
V.A.U.R.O.S. Core URO Library - Autonomic Nervous System (ANS)
Universal homeostasis engine inherited by ALL docks in the swarm.

The ANS implements a Damped Harmonic Oscillator for NTE state regulation,
ensuring every dock naturally returns to its ideal equilibrium after
experiencing stress, reward, or any other stimulus.

PHYSICS MODEL:
  - Spring Force (k): Pulls chemicals back to baseline equilibrium
  - Damping Force (c): Prevents infinite oscillation, ensures settling
  - Momentum (v): Allows natural pendulum swings past baseline
  - Boundary Collision: Inelastic bounce at 0.0 and 100.0 limits

USAGE (inherited by all docks):
  from uro.autonomic_nervous_system import AutonomicNervousSystem
  
  # Create ANS for this dock
  ans = AutonomicNervousSystem(dock_name="cognitive")
  await ans.start()
  
  # Apply stimulus (stress, reward, etc.)
  ans.apply_stimulus("epinephrine", 80.0)
  
  # ANS automatically returns to homeostasis via background loop
  # Query current state anytime:
  state = ans.get_state()
  
  # Stop when dock shuts down
  await ans.stop()

INTEGRATION WITH URO:
  The ANS is designed to work seamlessly with URO's NTE vectors.
  Any URO that carries an NTE state can reference the ANS for
  autonomous regulation. Docks can override baselines and damping
  coefficients to customize their homeostasis profile.
"""
import asyncio
import logging
import time
from typing import Dict, Optional, Callable, List

logger = logging.getLogger("VAUROS.ANS")


class AutonomicNervousSystem:
    """
    Universal homeostasis engine for NTE regulation.
    
    Implements damped harmonic oscillation to naturally return
    neurotransmitter levels to their ideal baselines after stimuli.
    
    Attributes:
        dock_name: Identifier for the dock this ANS belongs to
        baselines: Ideal equilibrium values for each neurotransmitter
        nte: Current neurotransmitter levels
        velocities: Current momentum for each neurotransmitter
        spring_constant: How strongly chemicals are pulled to baseline
        damping_coefficient: How quickly oscillations settle
        tick_rate: Seconds between ANS update cycles
    """
    
    # Default baselines (can be overridden per dock)
    DEFAULT_BASELINES = {
        "dopamine": 50.0,
        "serotonin": 100.0,
        "epinephrine": 10.0,
        "cannabinoid": 10.0,
        "oxytocin": 30.0,
        "norepinephrine": 20.0,
        "acetylcholine": 40.0,
        "gaba": 30.0
    }
    
    def __init__(
        self,
        dock_name: str,
        baselines: Optional[Dict[str, float]] = None,
        spring_constant: float = 0.02,
        damping_coefficient: float = 0.15,
        tick_rate: float = 1.0
    ):
        """
        Initialize the Autonomic Nervous System.
        
        Args:
            dock_name: Name of the dock this ANS serves
            baselines: Custom baseline values (defaults to DEFAULT_BASELINES)
            spring_constant: Pull strength toward baseline (higher = faster return)
            damping_coefficient: Resistance to movement (higher = less oscillation)
            tick_rate: Seconds between update cycles
        """
        self.dock_name = dock_name
        self.baselines = (baselines or self.DEFAULT_BASELINES).copy()
        self.nte = self.baselines.copy()
        self.velocities = {k: 0.0 for k in self.baselines}
        
        # Physics constants
        self.spring_constant = spring_constant
        self.damping_coefficient = damping_coefficient
        self.tick_rate = tick_rate
        
        # State tracking
        self.running = False
        self.task: Optional[asyncio.Task] = None
        self.last_stress_time = time.time()
        self.stress_event_count = 0
        self.homeostasis_achievements = 0
        
        # Callbacks for when homeostasis is achieved
        self._homeostasis_callbacks: List[Callable] = []
        
        logger.debug(f"[{dock_name}] ANS initialized. Baselines: {self.baselines}")
    
    # =========================================================================
    # LIFECYCLE MANAGEMENT
    # =========================================================================
    
    async def start(self):
        """Start the ANS background regulation loop."""
        if not self.running:
            self.running = True
            self.task = asyncio.create_task(self._regulation_loop())
            logger.info(f"[{self.dock_name}] ANS started.")
    
    async def stop(self):
        """Stop the ANS background regulation loop."""
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            self.task = None
            logger.info(f"[{self.dock_name}] ANS stopped.")
    
    @property
    def is_running(self) -> bool:
        """Check if the ANS is actively regulating."""
        return self.running
    
    # =========================================================================
    # STIMULUS APPLICATION
    # =========================================================================
    
    def apply_stimulus(self, neurotransmitter: str, intensity: float):
        """
        Apply a stimulus to a neurotransmitter.
        
        Positive intensity = spike (stress, reward, focus)
        Negative intensity = suppression (calming, inhibition)
        
        The ANS will automatically regulate back to baseline.
        """
        if neurotransmitter not in self.nte:
            logger.warning(f"[{self.dock_name}] Unknown neurotransmitter: {neurotransmitter}")
            return
        
        # Add momentum for pendulum effect
        self.velocities[neurotransmitter] += intensity * 0.5
        
        # Immediate spike/suppression
        self.nte[neurotransmitter] = max(
            0.0, 
            min(100.0, self.nte[neurotransmitter] + intensity)
        )
        
        # Track stress events
        if neurotransmitter == "epinephrine" and intensity > 0:
            self.last_stress_time = time.time()
            self.stress_event_count += 1
        
        logger.info(
            f"[{self.dock_name}] Stimulus: {neurotransmitter} "
            f"{'+' if intensity > 0 else ''}{intensity:.1f} "
            f"-> {self.nte[neurotransmitter]:.1f}"
        )
    
    def apply_stress(self, intensity: float = 50.0):
        """Apply epinephrine spike (stress response)."""
        self.apply_stimulus("epinephrine", intensity)
        self.apply_stimulus("norepinephrine", intensity * 0.5)
    
    def apply_reward(self, intensity: float = 20.0):
        """Apply dopamine spike (reward response)."""
        self.apply_stimulus("dopamine", intensity)
        self.apply_stimulus("serotonin", intensity * 0.3)
    
    def apply_focus(self, intensity: float = 30.0):
        """Apply acetylcholine spike (focus response)."""
        self.apply_stimulus("acetylcholine", intensity)
    
    def apply_calm(self, intensity: float = 20.0):
        """Apply GABA spike (calming response)."""
        self.apply_stimulus("gaba", intensity)
        self.apply_stimulus("serotonin", intensity * 0.5)
    
    # =========================================================================
    # STATE QUERYING
    # =========================================================================
    
    def get_state(self) -> Dict[str, float]:
        """Get current neurotransmitter levels."""
        return {k: round(v, 2) for k, v in self.nte.items()}
    
    def get_velocities(self) -> Dict[str, float]:
        """Get current momentum for each neurotransmitter."""
        return {k: round(v, 4) for k, v in self.velocities.items()}
    
    def is_at_homeostasis(self, threshold: float = 5.0) -> bool:
        """
        Check if all neurotransmitters are within threshold of baseline.
        
        Args:
            threshold: Maximum allowed deviation from baseline
            
        Returns:
            True if all chemicals are near their baselines
        """
        for chem in self.baselines:
            deviation = abs(self.nte[chem] - self.baselines[chem])
            if deviation > threshold:
                return False
        return True
    
    def get_stress_level(self) -> str:
        """Get a human-readable stress level classification."""
        epi = self.nte.get("epinephrine", 10.0)
        if epi > 80:
            return "CRITICAL"
        elif epi > 60:
            return "HIGH"
        elif epi > 30:
            return "MODERATE"
        elif epi > 15:
            return "LOW"
        else:
            return "HOMEOSTASIS"
    
    def get_full_diagnostic(self) -> Dict:
        """Get complete ANS diagnostic information."""
        return {
            "dock": self.dock_name,
            "running": self.running,
            "nte": self.get_state(),
            "velocities": self.get_velocities(),
            "baselines": self.baselines,
            "stress_level": self.get_stress_level(),
            "at_homeostasis": self.is_at_homeostasis(),
            "stress_events_total": self.stress_event_count,
            "homeostasis_achievements": self.homeostasis_achievements,
            "seconds_since_last_stress": round(time.time() - self.last_stress_time, 1),
            "spring_constant": self.spring_constant,
            "damping_coefficient": self.damping_coefficient
        }
    
    # =========================================================================
    # CALLBACK REGISTRATION
    # =========================================================================
    
    def on_homeostasis_achieved(self, callback: Callable):
        """
        Register a callback to be called when homeostasis is achieved.
        
        Args:
            callback: Async or sync function to call when equilibrium is reached
        """
        self._homeostasis_callbacks.append(callback)
    
    async def _fire_homeostasis_callbacks(self):
        """Fire all registered homeostasis callbacks."""
        for callback in self._homeostasis_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(self)
                else:
                    callback(self)
            except Exception as e:
                logger.error(f"[{self.dock_name}] Homeostasis callback error: {e}")
    
    # =========================================================================
    # CORE REGULATION LOOP (Damped Harmonic Oscillator)
    # =========================================================================
    
    async def _regulation_loop(self):
        """
        The core regulation loop. Runs at tick_rate frequency.
        
        Applies damped harmonic oscillation physics to each neurotransmitter:
        
        F_spring = -k * x       (pulls toward baseline)
        F_damping = -c * v      (resists movement)
        a = F_spring + F_damping (total acceleration)
        v += a                   (update velocity)
        x += v                   (update position)
        """
        k = self.spring_constant
        c = self.damping_coefficient
        was_at_homeostasis = False
        
        while self.running:
            await asyncio.sleep(self.tick_rate)
            
            for chem in self.baselines:
                baseline = self.baselines[chem]
                current = self.nte[chem]
                v = self.velocities[chem]
                
                # Displacement from baseline
                x = current - baseline
                
                # Spring force: pulls back toward baseline
                F_spring = -k * x
                
                # Damping force: resists movement (prevents infinite oscillation)
                F_damping = -c * v
                
                # Total acceleration
                a = F_spring + F_damping
                
                # Update velocity (momentum)
                v += a
                
                # Update position (neurotransmitter level)
                current += v
                
                # Clamp to biological limits [0, 100]
                current = max(0.0, min(100.0, current))
                
                # Inelastic collision at boundaries (energy loss on bounce)
                if current <= 0.0 or current >= 100.0:
                    v = -v * 0.5  # Lose 50% energy on boundary hit
                
                self.nte[chem] = current
                self.velocities[chem] = v
            
            # Check for homeostasis achievement
            is_at_homeostasis = self.is_at_homeostasis()
            
            if is_at_homeostasis and not was_at_homeostasis:
                # Just achieved homeostasis
                self.homeostasis_achievements += 1
                logger.info(
                    f"[{self.dock_name}] HOMEOSTASIS ACHIEVED "
                    f"(achievement #{self.homeostasis_achievements})"
                )
                await self._fire_homeostasis_callbacks()
            
            was_at_homeostasis = is_at_homeostasis
    
    # =========================================================================
    # SERIALIZATION (for URO integration)
    # =========================================================================
    
    def to_dict(self) -> Dict:
        """Serialize ANS state for storage in URO."""
        return {
            "dock_name": self.dock_name,
            "nte": self.get_state(),
            "velocities": self.get_velocities(),
            "baselines": self.baselines,
            "running": self.running,
            "stress_events": self.stress_event_count,
            "homeostasis_achievements": self.homeostasis_achievements
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "AutonomicNervousSystem":
        """Deserialize ANS state from URO storage."""
        ans = cls(
            dock_name=data.get("dock_name", "unknown"),
            baselines=data.get("baselines")
        )
        ans.nte = data.get("nte", ans.baselines.copy())
        ans.stress_event_count = data.get("stress_events", 0)
        ans.homeostasis_achievements = data.get("homeostasis_achievements", 0)
        return ans
    
    def __repr__(self):
        stress = self.get_stress_level()
        return f"ANS({self.dock_name}, stress={stress}, running={self.running})"


# =============================================================================
# CONVENIENCE: Global ANS instance factory
# =============================================================================

_dock_registry: Dict[str, AutonomicNervousSystem] = {}

def get_ans_for_dock(dock_name: str, **kwargs) -> AutonomicNervousSystem:
    """
    Get or create an ANS instance for a specific dock.
    Ensures each dock has exactly one ANS instance.
    
    Args:
        dock_name: Name of the dock
        **kwargs: Additional arguments passed to AutonomicNervousSystem
        
    Returns:
        The ANS instance for this dock
    """
    if dock_name not in _dock_registry:
        _dock_registry[dock_name] = AutonomicNervousSystem(dock_name, **kwargs)
    return _dock_registry[dock_name]

def get_all_ans() -> Dict[str, AutonomicNervousSystem]:
    """Get all registered ANS instances across the swarm."""
    return _dock_registry.copy()
