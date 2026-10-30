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


# V.A.U.R.O.S AUTO-GENERATED
# ======================================================================= #
# MODULE INTENT: Standard OPAR (Observe, Plan, Act, Review) Engine.
# ======================================================================= #
import logging
from typing import Callable, Optional
from uro.vauros_uro import OrchestrationURO

logger = logging.getLogger("VAUROS.OPAR")

class BaseOPAREngine:
    async def execute_lifecycle(self, uro: OrchestrationURO, action_func: Optional[Callable] = None) -> OrchestrationURO:
        logger.info(f"[OBSERVE] Processing URO: {uro.urid1_source} -> {uro.urid2_instance}")
        self.observe(uro)
        
        logger.info("[PLAN] Formulating execution context.")
        self.plan(uro)
        
        logger.info("[ACT] Executing defined capability.")
        success = await self.act(uro, action_func)
        
        logger.info("[REVIEW] Mutating NTE state based on outcome.")
        self.review(uro, success)
        
        uro.seal_uro()
        return uro

    def observe(self, uro: OrchestrationURO):
        """Observe phase: Capture and log the current state of the URO.
        
        This implementation records the URO's current state, validates its
        integrity, and logs relevant metadata for traceability.
        """
        # Validate URO integrity
        if not uro.urid1_source or not uro.urid2_instance:
            logger.warning(f"URO missing source or instance identifiers: {uro.urid1_source} -> {uro.urid2_instance}")
        
        # Log observation metadata
        logger.debug(f"Observed URO state - Source: {uro.urid1_source}, Instance: {uro.urid2_instance}")
        
        # Record observation timestamp if available
        if hasattr(uro, 'metadata') and uro.metadata is not None:
            import time
            uro.metadata['last_observed'] = time.time()
        
        # Ensure NTE vector is initialized
        if not hasattr(uro, 'nte_vector') or uro.nte_vector is None:
            logger.warning("NTE vector not initialized, creating default")
            from uro.vauros_nte import NTEVector
            uro.nte_vector = NTEVector()

    def plan(self, uro: OrchestrationURO):
        """Plan phase: Prepare execution strategy and validate prerequisites.
        
        This implementation checks that all required fields are present,
        validates the action function availability, and prepares the
        execution context.
        """
        # Validate required fields
        if not uro.urid1_source:
            raise ValueError("URO source identifier is required for planning")
        
        if not uro.urid2_instance:
            raise ValueError("URO instance identifier is required for planning")
        
        # Log planning decisions
        logger.debug(f"Planning execution for URO: {uro.urid1_source} -> {uro.urid2_instance}")
        
        # Prepare execution context
        if not hasattr(uro, 'execution_context') or uro.execution_context is None:
            uro.execution_context = {}
        
        # Set default execution parameters
        uro.execution_context['planned_at'] = __import__('time').time()
        uro.execution_context['strategy'] = 'standard_opar'
        
        # Validate NTE vector state
        if uro.nte_vector is not None:
            logger.debug(f"NTE vector state before execution: reward={uro.nte_vector.reward}, punishment={uro.nte_vector.punishment}")

    async def act(self, uro: OrchestrationURO, action_func: Callable) -> bool:
        """Act phase: Execute the defined capability.
        
        Args:
            uro: The URO being processed
            action_func: Optional callable to execute. If None, returns True
                        as a no-op success.
        
        Returns:
            bool: True if execution succeeded, False otherwise
        """
        if action_func is None:
            logger.info("No action function provided, treating as no-op success")
            return True
        
        try:
            # Execute the action function
            result = action_func(uro)
            
            # Handle async results
            if hasattr(result, '__await__'):
                result = await result
            
            # Interpret result
            if isinstance(result, bool):
                return result
            elif result is None:
                logger.warning("Action function returned None, treating as success")
                return True
            else:
                # Non-boolean result, treat as success if no exception
                logger.debug(f"Action function returned non-boolean result: {type(result)}")
                return True
                
        except Exception as e:
            logger.error(f"Action execution failed: {str(e)}")
            return False

    def review(self, uro: OrchestrationURO, success: bool):
        """Review phase: Evaluate execution outcome and update NTE state.
        
        Args:
            uro: The URO being processed
            success: Whether the action execution succeeded
        """
        if success:
            uro.nte_vector.mutate_reward(10.0)
            logger.info(f"Execution successful, reward applied. NTE state: reward={uro.nte_vector.reward}")
        else:
            uro.nte_vector.mutate_punishment(10.0)
            logger.warning(f"Execution failed, punishment applied. NTE state: punishment={uro.nte_vector.punishment}")
        
        # Log review summary
        logger.debug(f"Review complete for URO: {uro.urid1_source} -> {uro.urid2_instance}")