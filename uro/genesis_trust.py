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
MODULE: Genesis Trust Enforcement
INTENT: Enforce the Genesis Rule: child UROs start at 100% trust to parent,
        new (genesis) UROs start at 0% trust and must earn.
STANDARD: URO-STD-0001 S13
"""
from __future__ import annotations

from typing import Optional
from uro.core.urid import URID
from uro.base import BaseURO
from uro.synapse.vector import SynapseVectorURO

__all__ = ["GenesisTrustEnforcer"]


class GenesisTrustEnforcer:
    """
    Enforces the Genesis Trust Rule.
    
    Child UROs (with parent_inahash) start at 100% trust.
    Genesis UROs (no parent) start at 0% trust.
    """
    
    @staticmethod
    def get_initial_trust(uro: BaseURO) -> float:
        """
        Get the initial trust level for a URO.
        
        Args:
            uro: The URO to evaluate
            
        Returns:
            Initial trust level (0.0 or 100.0)
        """
        return 100.0 if uro.is_child() else 0.0
    
    @staticmethod
    def initialize_synapse_trust(
        synapse: SynapseVectorURO,
        endpoint1: BaseURO,
        endpoint2: BaseURO
    ) -> None:
        """
        Initialize trust for a new synapse based on the Genesis Rule.
        
        Args:
            synapse: The new synapse to initialize
            endpoint1: First endpoint URO
            endpoint2: Second endpoint URO
        """
        trust1 = GenesisTrustEnforcer.get_initial_trust(endpoint1)
        trust2 = GenesisTrustEnforcer.get_initial_trust(endpoint2)
        
        # If both endpoints are trusted (children of trusted parents),
        # start the synapse at a moderate trust level
        if trust1 >= 100.0 and trust2 >= 100.0:
            initial_trust = 75.0  # High but not maximum
        elif trust1 >= 100.0 or trust2 >= 100.0:
            initial_trust = 50.0  # Moderate if one endpoint is trusted
        else:
            initial_trust = 0.0   # Zero trust for genesis UROs
        
        # Set the overall trust
        synapse.overall_trust = initial_trust
        
        # Add a default "general" topic with the initial trust
        synapse.add_topic_trust("general", initial_trust)
        
        synapse.seal()
    
    @staticmethod
    def verify_parent_trust(child: BaseURO, parent: BaseURO) -> bool:
        """
        Verify that a child URO legitimately descends from a parent.
        
        Args:
            child: The child URO
            parent: The claimed parent URO
            
        Returns:
            True if the parent_inahash matches the parent's INAHASH
        """
        if not child.is_child():
            return False
        
        return child.parent_inahash == parent.inahash
