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
MODULE: Per-Topic Trust URO
INTENT: Trust is per-relationship AND per-topic. Two UROs may have high trust
        on religion but low trust on politics. Each topic is its own URO.
STANDARD: URO-STD-0001 S10.3
"""
from __future__ import annotations

import time
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from uro.core.urid import URID
from uro.security.hashing import inahash
from uro.nte.axes import NTEAxis

__all__ = ["TopicTrustURO"]


class TopicTrustURO(BaseModel):
    """
    Trust on a specific topic within a synapse.
    
    Example: Aegis↔Chaos synapse has high trust on "security_analysis" topic
    but low trust on "resource_allocation" topic.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # ── IDENTITY ──────────────────────────────────────
    urid1: URID = Field(..., description="Parent Synapse Vector URO")
    urid2: URID = Field(..., description="This topic trust's identity")
    
    # ── TOPIC ─────────────────────────────────────────
    topic: str = Field(..., description="Topic name (e.g., 'security', 'politics', 'code_quality')")
    
    # ── TRUST STATE ───────────────────────────────────
    trust_level: float = Field(0.0, ge=0.0, le=100.0, description="Trust level on this topic (0-100)")
    confidence: float = Field(50.0, ge=0.0, le=100.0, description="Confidence in this trust assessment")
    openness: float = Field(50.0, ge=0.0, le=100.0, description="Willingness to update trust on this topic")
    
    # ── NTE MODULATION ────────────────────────────────
    # Trust is modulated by NTE: high acetylcholine = more open to learning
    # High cannabinoid = more willing to let go of prior assumptions
    nte_modulation: dict = Field(
        default_factory=lambda: {
            NTEAxis.ACETYLCHOLINE.value: 0.5,  # Plasticity weight
            NTEAxis.CANNABINOID.value: 0.3,     # Forgetting weight
            NTEAxis.OXYTOCIN.value: 0.7         # Trust weight
        },
        description="How NTE axes modulate trust updates on this topic"
    )
    
    # ── INTEGRITY ─────────────────────────────────────
    inahash: str = Field(default="", description="INAHASH seal")
    parent_inahash: Optional[str] = Field(None, description="Parent Synapse Vector's INAHASH")
    
    # ── TIMESTAMP ─────────────────────────────────────
    timestamp: float = Field(default_factory=time.time, description="Last update time")
    
    def compute_inahash(self) -> str:
        """Compute the INAHASH seal."""
        data = self.model_dump(exclude={"inahash"})
        msg = str(data).encode()
        return inahash(msg).hex()
    
    def seal(self) -> None:
        """Seal this URO."""
        self.inahash = self.compute_inahash()
    
    def update_trust(self, delta: float, nte_context: dict) -> None:
        """
        Update trust based on outcome and NTE context.
        
        Args:
            delta: Raw trust delta (positive = good outcome, negative = bad)
            nte_context: Current NTE state (modulates how much to update)
        """
        # Modulate delta by NTE openness
        ach_weight = nte_context.get(NTEAxis.ACETYLCHOLINE.value, 50.0) / 100.0
        cb_weight = nte_context.get(NTEAxis.CANNABINOID.value, 50.0) / 100.0
        oxt_weight = nte_context.get(NTEAxis.OXYTOCIN.value, 50.0) / 100.0
        
        # High acetylcholine = more open to updating
        # High cannabinoid = more willing to let go (decay old trust)
        # High oxytocin = more willing to build trust
        modulation = (
            ach_weight * self.nte_modulation[NTEAxis.ACETYLCHOLINE.value] +
            cb_weight * self.nte_modulation[NTEAxis.CANNABINOID.value] +
            oxt_weight * self.nte_modulation[NTEAxis.OXYTOCIN.value]
        )
        
        modulated_delta = delta * modulation * self.openness / 100.0
        self.trust_level = max(0.0, min(100.0, self.trust_level + modulated_delta))
        self.timestamp = time.time()
