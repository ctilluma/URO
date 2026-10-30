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
MODULE: Canonical URO Shim (Comprehensive Re-exports)
INTENT: Single import point for all commonly-used URO types. Docks can import
        from uro.uro or uro.canonical_shim to get everything they need.
STANDARD: URO-STD-0001 (Fractal URO Mandate)

FRACTAL URO MANDATE:
    Everything is a URO. This shim ensures every commonly-used URO type is
    accessible through a single import, reducing replication and making the
    canonical library the single source of truth.

USAGE:
    from uro.uro import (
        URO, BaseURO, URID, INAHASH,
        NTEState, NTEVector, SynapseVector, CustodyChain, Receipt,
        create_dock_uro, establish_synapse, record_dock_custody,
        create_fulfilled_receipt, create_deferred_receipt, create_incapable_receipt
    )
"""
from __future__ import annotations

# =====================================================================
# CORE URO TYPES
# =====================================================================
from uro.core.uro import URO
from uro.base import BaseURO, OPARPhase, Quadrant
from uro.core.urid import URID

# =====================================================================
# NTE (Neurotransmitter) TYPES
# =====================================================================
from uro.nte.neurotransmitters import NTEState
from uro.nte.state import NTEStateURO
from uro.nte.axes import NTEAxis, NTEAxisGovernance, NTE_AXES
from uro.api.models import NTEVectorModel

# Alias: NTEVector is the API-layer name for NTEVectorModel
NTEVector = NTEVectorModel

# =====================================================================
# RECEIPT TYPES
# =====================================================================
from uro.exchange.receipt import ReceiptURO, ReceiptMode

# Aliases: convenience names docks expect
Receipt = ReceiptURO
ReceiptStatus = ReceiptMode
ReceiptEnvelope = ReceiptURO  # Synonym

# =====================================================================
# SYNAPSE TYPES
# =====================================================================
from uro.synapse.vector import SynapseVectorURO

# Alias: SynapseVector is the convenience name
SynapseVector = SynapseVectorURO

# =====================================================================
# CUSTODY TYPES
# =====================================================================
from uro.custody.chain import CustodyChainURO
from uro.custody.entry import CustodyEntryURO

# Aliases
CustodyChain = CustodyChainURO
CustodyEntry = CustodyEntryURO

# =====================================================================
# CANONICAL INTEGRATION HELPERS
# =====================================================================
from uro.canonical_integration import (
    create_dock_uro,
    establish_synapse,
    record_dock_custody,
    create_fulfilled_receipt,
    create_deferred_receipt,
    create_incapable_receipt,
    CanonicalUROHelper,
)

from uro.integration import (
    create_receipt,
    create_uro_with_enrichments,
    create_synapse_between,
    record_custody_event,
)

# =====================================================================
# SECURITY / HASHING
# =====================================================================
from uro.security.hashing import inahash

# INAHASH as a callable class (some docks expect INAHASH(data))
class INAHASH:
    """INAHASH = Blake3-1024(SHA3-1024(msg)). Callable wrapper."""
    @staticmethod
    def __call__(data: bytes) -> bytes:
        return inahash(data)
    
    @staticmethod
    def compute(data: bytes) -> str:
        """Compute INAHASH and return as hex string."""
        return inahash(data).hex()

# =====================================================================
# GENESIS TRUST
# =====================================================================
from uro.genesis_trust import GenesisTrustEnforcer

# Alias
GenesisURO = GenesisTrustEnforcer

# =====================================================================
# COORDINATOR BUS
# =====================================================================
from uro.coordinator_bus import CoordinatorBus

# =====================================================================
# WIRING / REGISTRY
# =====================================================================
from uro.wiring import get_universal, UniversalLoader
from uro.registry_bridge import get_registry

# =====================================================================
# FACTORY / STATUS CLASSES (for docks that expect them)
# =====================================================================
class UROFactory:
    """Factory for creating UROs with enrichments."""
    @staticmethod
    def create_dock_uro(*args, **kwargs):
        return create_dock_uro(*args, **kwargs)
    
    @staticmethod
    def establish_synapse(*args, **kwargs):
        return establish_synapse(*args, **kwargs)

class UROStatus:
    """URO lifecycle status constants."""
    GENESIS = "genesis"
    ACTIVE = "active"
    SEALED = "sealed"
    ARCHIVED = "archived"

class UROType:
    """URO type classification."""
    BASE = "base"
    ENRICHMENT = "enrichment"
    SYNAPSE = "synapse"
    CUSTODY = "custody"
    RECEIPT = "receipt"

class UROState:
    def __init__(self, *args, **kwargs):  # [POLISH-Y] tolerant
        for _k_y, _v_y in kwargs.items():
            setattr(self, _k_y, _v_y)
        self._state_args = args
    """URO operational state."""
    DOMAIN = "domain"
    CAPABILITY = "capability"
    DOCK = "dock"
    AGENT = "agent"
    TASK = "task"
    ARTIFACT = "artifact"
    SESSION = "session"
    MODEL = "model"
    INITIALIZED = "initialized"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# =====================================================================
# HELPER FUNCTIONS
# =====================================================================
def seal(uro_obj) -> None:
    """Seal a URO by calling its .seal() method."""
    if hasattr(uro_obj, 'seal') and callable(uro_obj.seal):
        uro_obj.seal()
    else:
        raise AttributeError(f"{type(uro_obj).__name__} has no seal() method")

# =====================================================================
# EXPORTS
# =====================================================================
__all__ = [
    # Core
    "URO", "BaseURO", "URID", "OPARPhase", "Quadrant",
    # NTE
    "NTEState", "NTEStateURO", "NTEAxis", "NTEAxisGovernance", "NTE_AXES",
    "NTEVector", "NTEVectorModel",
    # Receipt
    "Receipt", "ReceiptURO", "ReceiptMode", "ReceiptStatus", "ReceiptEnvelope",
    # Synapse
    "SynapseVector", "SynapseVectorURO",
    # Custody
    "CustodyChain", "CustodyChainURO", "CustodyEntry", "CustodyEntryURO",
    # Integration
    "create_dock_uro", "establish_synapse", "record_dock_custody",
    "create_fulfilled_receipt", "create_deferred_receipt", "create_incapable_receipt",
    "create_receipt", "create_uro_with_enrichments", "create_synapse_between",
    "record_custody_event", "CanonicalUROHelper",
    # Security
    "inahash", "INAHASH",
    # Trust
    "GenesisTrustEnforcer", "GenesisURO",
    # Bus
    "CoordinatorBus",
    # Wiring
    "get_universal", "UniversalLoader", "get_registry",
    # Factory/Status
    "UROFactory", "UROStatus", "UROType", "UROState",
    # Helpers
    "seal",
]
