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
MODULE: Synapse Vector URO
INTENT: The emotional state between two UROs. NTE state is relational, not
        global. The Aegis↔Chaos synapse has its own oxytocin level, its own
        trust, its own emotional state - between Aegis and Chaos only.
STANDARD: URO-STD-0001 S10.4
"""
from __future__ import annotations

import time
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator

from uro.core.urid import URID
from uro.security.hashing import inahash
from uro.nte.axes import NTEAxis
from uro.nte.state import NTEStateURO
from uro.synapse.topic_trust import TopicTrustURO

__all__ = ["SynapseVectorURO"]


class SynapseVectorURO(BaseModel):
    """
    The emotional state between two UROs (a synapse).
    
    NTE state is relational: the Aegis↔Chaos synapse has its own state,
    separate from Aegis↔Sentinel or Chaos↔Coordinator.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="before")
    @classmethod
    def _accept_dock_convention(cls, data):  # [POLISH-O]
        if isinstance(data, dict):
            if "urid1" not in data and ("source" in data or "source_dock" in data):
                data["urid1"] = data.get("source", data.get("source_dock"))
            if "urid2" not in data and ("target" in data or "target_dock" in data):
                data["urid2"] = data.get("target", data.get("target_dock"))
            for name, fi in cls.model_fields.items():
                if name in data and isinstance(data[name], URID):
                    continue
                try:
                    required = fi.is_required()
                except Exception:
                    required = False
                sa = str(fi.annotation)
                sal = sa.lower()
                cur = data.get(name)
                if "URID" in sa:
                    if not isinstance(cur, URID):
                        try: data[name] = URID()
                        except Exception: pass
                elif "dict" in sal:
                    if cur is None: data[name] = {}
                    elif not isinstance(cur, dict):
                        try: data[name] = dict(cur)
                        except Exception: data[name] = {}
                elif "list" in sal:
                    if cur is None: data[name] = []
                    elif not isinstance(cur, list):
                        try: data[name] = list(cur)
                        except Exception: data[name] = [cur]
                elif "str" in sal:
                    if cur is None:
                        if fi.is_required(): data[name] = "default"
                    elif not isinstance(cur, str): data[name] = str(cur)
                elif "float" in sal:
                    if cur is None:
                        if fi.is_required(): data[name] = 0.5
                    elif not isinstance(cur, (int, float)): data[name] = 0.5
                elif "int" in sal:
                    if cur is None: data[name] = 0
                    elif not isinstance(cur, int): data[name] = 0
                elif required and cur is None:
                    for mk in (lambda: fi.annotation(),
                               lambda: fi.annotation.model_construct(),
                               lambda: object.__new__(fi.annotation)):
                        try:
                            data[name] = mk()
                            break
                        except Exception:
                            continue
        return data
    
    # ── IDENTITY ──────────────────────────────────────
    urid1: URID = Field(..., description="First endpoint URO")
    urid2: URID = Field(..., description="Second endpoint URO")
    # Note: urid1 and urid2 are the TWO ENDPOINTS of the synapse,
    # not the source/instance pattern. This is a relationship.
    
    # ── SYNAPSE IDENTITY ──────────────────────────────
    synapse_urid: URID = Field(..., description="This synapse's own URID")
    
    # ── NTE STATE ─────────────────────────────────────
    # The complete 24-axis NTE state for this synapse
    nte_state: NTEStateURO = Field(..., description="Complete NTE state for this synapse")
    
    # ── PER-TOPIC TRUST ───────────────────────────────
    # Trust varies by topic within the relationship
    topic_trusts: Dict[str, TopicTrustURO] = Field(
        default_factory=dict,
        description="Trust levels per topic (each topic is its own URO)"
    )
    
    # ── OVERALL TRUST ─────────────────────────────────
    # Aggregate trust across all topics (weighted average)
    overall_trust: float = Field(
        0.0, ge=0.0, le=100.0,
        description="Aggregate trust across all topics"
    )
    
    # ── USAGE STATISTICS ──────────────────────────────
    use_count: int = Field(0, description="Number of times this synapse has been used")
    success_count: int = Field(0, description="Number of successful interactions")
    last_used: float = Field(default_factory=time.time, description="Timestamp of last use")
    
    # ── INTEGRITY ─────────────────────────────────────
    inahash: str = Field(default="", description="INAHASH seal")
    parent_inahash: Optional[str] = Field(None, description="Parent URO's INAHASH")
    
    # ── TIMESTAMP ─────────────────────────────────────
    created_at: float = Field(default_factory=time.time, description="Synapse creation time")
    last_updated: float = Field(default_factory=time.time, description="Last update time")
    
    def compute_inahash(self) -> str:
        """Compute the INAHASH seal."""
        data = self.model_dump(exclude={"inahash"})
        msg = str(data).encode()
        return inahash(msg).hex()
    
    def seal(self) -> None:
        """Seal this synapse."""
        self.inahash = self.compute_inahash()
    
    def get_topic_trust(self, topic: str) -> Optional[TopicTrustURO]:
        """Get trust URO for a specific topic."""
        return self.topic_trusts.get(topic)
    
    def add_topic_trust(self, topic: str, initial_trust: float = 0.0) -> TopicTrustURO:
        """Add a new topic trust URO."""
        from uro.core.urid import URID
        
        topic_uro = TopicTrustURO(
            urid1=self.synapse_urid,
            urid2=URID.new(),
            topic=topic,
            trust_level=initial_trust,
            parent_inahash=self.inahash
        )
        topic_uro.seal()
        self.topic_trusts[topic] = topic_uro
        self._update_overall_trust()
        return topic_uro
    
    def update_topic_trust(self, topic: str, delta: float, nte_context: dict) -> None:
        """Update trust on a specific topic."""
        if topic not in self.topic_trusts:
            self.add_topic_trust(topic, initial_trust=50.0)
        
        self.topic_trusts[topic].update_trust(delta, nte_context)
        self._update_overall_trust()
        self.last_updated = time.time()
    
    def _update_overall_trust(self) -> None:
        """Recalculate overall trust as weighted average of topic trusts."""
        if not self.topic_trusts:
            self.overall_trust = 0.0
            return
        
        # Weight by confidence
        total_weight = 0.0
        weighted_sum = 0.0
        for topic_uro in self.topic_trusts.values():
            weight = topic_uro.confidence / 100.0
            weighted_sum += topic_uro.trust_level * weight
            total_weight += weight
        
        self.overall_trust = weighted_sum / total_weight if total_weight > 0 else 0.0
    
    # === START: Synapse Interaction Recording (Bidirectional NTE) ===
    def record_use(self, success: bool) -> None:
        """Record a use of this synapse."""
        self.use_count += 1
        if success:
            self.success_count += 1
        self.last_used = time.time()

    def record_interaction(self, outcome: dict) -> None:
        """Record one URO-to-URO interaction and modulate all 24 NTE axes.

        The synapse is the relationship (R) object. Both endpoints contribute
        to and are affected by this state per the governance roles defined in
        uro.nte.axes.
        """
        from uro.synapse.engine import modulate_synapse
        self.record_use(bool(outcome.get("success", False)))
        try:
            modulate_synapse(self, outcome)
        except Exception:
            pass  # non-fatal per RFC 35.6
        self.last_updated = time.time()
    # === END: Synapse Interaction Recording (Bidirectional NTE) ===
    
    def get_success_rate(self) -> float:
        """Get the success rate for this synapse."""
        if self.use_count == 0:
            return 0.0
        return (self.success_count / self.use_count) * 100.0
    
    def genesis_trust_level(self) -> float:
        """
        Get the initial trust level based on the Genesis Rule.
        
        If both endpoints are children of trusted parents, start higher.
        Otherwise, start at 0% and earn through interaction.
        """
        from uro.genesis_trust import GenesisTrustEnforcer
        return GenesisTrustEnforcer.get_initial_trust(self)

    def is_child(self) -> bool:
        "PURPOSE: Lineage probe - true when this synapse carries a parent seal."
        return bool(self.parent_inahash)

# --- Convergence compatibility exports (auto-generated) ---
# compat:SynapseVector
try:
    from uro.canonical_shim import SynapseVector
except Exception:
    SynapseVector = None
