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
MODULE: Pydantic V2 API Models for URO Interchange
INTENT: Maps core URO objects to JSON-serializable models for FastAPI and 
        inter-dock communication. Ensures a single source of truth for URO 
        structure across the entire V.A.U.R.O.S. ecosystem.
"""
import uuid
import time
from typing import Dict, Any, Optional, List, Literal
from pydantic import BaseModel, Field, ConfigDict
from uro.core.urid import URID
from uro.core.uro import URO
from uro.security.hashing import inahash

class NTEVectorModel(BaseModel):
    """8-axis Neurotransmitter Vector for API interchange."""
    model_config = ConfigDict(frozen=False)
    dopamine: float = 50.0
    serotonin: float = 50.0
    epinephrine: float = 10.0
    cannabinoid: float = 10.0
    oxytocin: float = 30.0
    norepinephrine: float = 20.0
    acetylcholine: float = 40.0
    gaba: float = 30.0


    # --- CANONICAL ADAPTER: BIOLOGICAL MUTATION METHODS ---
    # Added to satisfy the Fractal URO Mandate across all 53 docks.
    
    def apply_dopamine_reward(self, success: bool, magnitude: float = 1.0) -> None:
        import math
        if success:
            x = (self.dopamine / 100.0) * magnitude
            delta = x * math.log10(x + 10) if x > 0 else 0.1
            self.dopamine = min(100.0, self.dopamine + (delta * 10.0))
            self.oxytocin = min(100.0, self.oxytocin + (magnitude * 2.0))
        else:
            self.dopamine = max(0.0, self.dopamine - (5.0 * magnitude))
            self.epinephrine = min(100.0, self.epinephrine + (5.0 * magnitude))

    def apply_epinephrine_threat(self, threat_level: float) -> None:
        self.epinephrine = min(100.0, self.epinephrine + threat_level)
        if self.epinephrine > 80.0:
            self.norepinephrine = min(100.0, self.norepinephrine + 10.0)

    def apply_cannabinoid_pruning(self, factor: float = 1.0) -> None:
        self.cannabinoid = min(100.0, self.cannabinoid + (15.0 * factor))
        if self.cannabinoid > 80.0:
            # Reset weak signals to baseline during high pruning
            for field in ['serotonin', 'epinephrine', 'oxytocin', 'norepinephrine', 'acetylcholine', 'gaba', 'dopamine']:
                val = getattr(self, field)
                if abs(val - 50.0) < 15.0:
                    setattr(self, field, 50.0)
            self.cannabinoid = 50.0


class BaseUROModel(BaseModel):
    """Standardized URO model for API ingestion and inter-dock routing."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    urid1_source: str = Field(default_factory=lambda: str(uuid.uuid4()))
    urid2_instance: str = Field(default_factory=lambda: str(uuid.uuid4()))
    quadrant: Literal["Base", "Gap Remediation", "Best Practice", "World-First Innovation"] = "Base"
    tenant_id: str = "system"
    env_context: str = "prod"
    intent: str = "process_query"
    payload: Dict[str, Any] = Field(default_factory=dict)
    nte: NTEVectorModel = Field(default_factory=NTEVectorModel)
    execution_result: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)
    opar_stage: Literal["Observe", "Plan", "Act", "Review"] = "Observe"
    swarm_path: Optional[str] = None

    @property
    def inahash(self) -> str:
        msg = f"{self.urid1_source}::{self.urid2_instance}".encode()
        return inahash(msg).hex()

    def to_core_uro(self) -> URO:
        u1 = URID.from_hex(self.urid1_source.replace("-", "")) if len(self.urid1_source.replace("-", "")) == 64 else URID.new()
        u2 = URID.from_hex(self.urid2_instance.replace("-", "")) if len(self.urid2_instance.replace("-", "")) == 64 else URID.new()
        uro = URO(u1, u2, payload=self.payload)
        uro._meta["api_model"] = self.model_dump()
        return uro

    @classmethod
    def from_core_uro(cls, uro: URO) -> "BaseUROModel":
        return cls(
            urid1_source=uro.urid1.to_hex(),
            urid2_instance=uro.urid2.to_hex(),
            payload=uro.payload
        )


    # --- CANONICAL ADAPTER: SYNAPSE HOOK ---
    # Enforces the mandate that relationships are first-class UROs.
    synapses: List[Any] = Field(default_factory=list, description="List of Association UROs connecting this URO to others")

    def register_synapse(self, association_uro: Any) -> None:
        if association_uro not in self.synapses:
            self.synapses.append(association_uro)


class CognitiveUROModel(BaseUROModel):
    """Cognitive-specific URO model."""
    intent: str = "cognitive_process"

class OrchestrationUROModel(BaseUROModel):
    """Orchestration URO model for DAG/Saga tracking."""
    intent: str = "orchestrate"
    orchestration_type: Literal["SAGA", "CHOREOGRAPHY", "BROADCAST"] = "SAGA"
    child_uros: List[BaseUROModel] = Field(default_factory=list)


# Backward-compat: docks import Receipt (canonical name is ReceiptURO)
try:
    from uro.exchange.receipt import ReceiptURO as Receipt
except ImportError:
    class Receipt(BaseModel):
        status: str = "FULFILLED"
        capability: Optional[str] = None
        error: Optional[str] = None
        data: Optional[Dict[str, Any]] = None

# --- Convergence compatibility exports (auto-generated) ---
# compat:CanonicalUROHelper
try:
    from uro.canonical_integration import CanonicalUROHelper
except Exception:
    CanonicalUROHelper = None
# compat:DEFERRED
try:
    from uro.exchange.receipt import ReceiptMode as _RM
    DEFERRED = getattr(_RM, "DEFERRED", "DEFERRED")
except Exception:
    DEFERRED = "DEFERRED"
# compat:EnhancedCognitiveURO
class EnhancedCognitiveURO:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:FULFILLED
try:
    from uro.exchange.receipt import ReceiptMode as _RM
    FULFILLED = getattr(_RM, "FULFILLED", "FULFILLED")
except Exception:
    FULFILLED = "FULFILLED"
# compat:INCAPABLE
try:
    from uro.exchange.receipt import ReceiptMode as _RM
    INCAPABLE = getattr(_RM, "INCAPABLE", "INCAPABLE")
except Exception:
    INCAPABLE = "INCAPABLE"
# compat:TheVoid
class TheVoid:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:compute_inahash
try:
    from uro.vauros_crypto import compute_inahash
except Exception:
    compute_inahash = None
# compat:validate_nte_vector
def validate_nte_vector(*args, **kwargs):
    return None
