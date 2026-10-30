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
MODULE: uro.uro - Comprehensive URO API surface
INTENT: This is the primary import target for docks. When code does
        'from uro.uro import X', Python resolves to this file. It re-exports
        every commonly-used URO type from the canonical shim.
STANDARD: URO-STD-0001 (Fractal URO Mandate)

FRACTAL URO MANDATE:
    Everything is a URO. This module ensures all base URO types are accessible
    through a single import point, reducing replication across docks.

USAGE:
    from uro.uro import (
        URO, BaseURO, URID, INAHASH,
        NTEState, NTEVector, SynapseVector, CustodyChain, Receipt,
        create_dock_uro, establish_synapse, record_dock_custody,
        UROFactory, UROStatus, UROType, seal
    )
"""
from __future__ import annotations

# Re-export everything from the canonical shim
from uro.canonical_shim import *  # noqa: F401,F403
from uro.canonical_shim import (  # noqa: F401
    # Core
    URO, BaseURO, URID, OPARPhase, Quadrant,
    # NTE
    NTEState, NTEStateURO, NTEAxis, NTEAxisGovernance, NTE_AXES,
    NTEVector, NTEVectorModel,
    # Receipt
    Receipt, ReceiptURO, ReceiptMode, ReceiptStatus, ReceiptEnvelope,
    # Synapse
    SynapseVector, SynapseVectorURO,
    # Custody
    CustodyChain, CustodyChainURO, CustodyEntry, CustodyEntryURO,
    # Integration helpers
    create_dock_uro, establish_synapse, record_dock_custody,
    create_fulfilled_receipt, create_deferred_receipt, create_incapable_receipt,
    create_receipt, create_uro_with_enrichments, create_synapse_between,
    record_custody_event, CanonicalUROHelper,
    # Security
    inahash, INAHASH,
    # Trust
    GenesisTrustEnforcer, GenesisURO,
    # Bus
    CoordinatorBus,
    # Wiring
    get_universal, UniversalLoader, get_registry,
    # Factory/Status
    UROFactory, UROStatus, UROType, UROState,
    # Helpers
    seal,
)

# Legacy compatibility
from uro.api.models import BaseUROModel, NTEVectorModel  # noqa: F401
UROBase = BaseUROModel

# Ensure __all__ is comprehensive
from uro.canonical_shim import __all__ as _shim_all  # noqa: F401
__all__ = list(_shim_all) + ["UROBase", "BaseUROModel"]


# BASE-URO FULL CONTRACT (flat re-exports for dock imports)
from uro.base_uros import (  # noqa: F401
    FULFILLED, DEFERRED, INCAPABLE,
    UROType, UROStatus, UROState, UROError, UROGenesis, UROFactory, UROSeal,
    INAHASH, Sigil, Lineage, NTEWeights, NTEContext, NTEProfile, NTEStatus,
    SynapseVector, SynapseType, SynapseTopic, TrustLevel, SynapseEndpoint, SynapseManager,
    CustodyChain, CustodyChainEntry, CustodyNode, CustodyRecord, CustodyRole, CustodyLink,
    ReceiptEnvelope, UROEnvelope, LedgerEntry, LedgerChain, UROBus,
    create_uro, get_uro_registry, create_synapse, create_synapse_uro, create_receipt_uro,
    create_receipt, create_custody_chain, genesis_uro, seal_inahash, custody_chain, nte_state,
)
from uro.nte.neurotransmitters import NTEState  # noqa: F401
from uro.exchange.receipt import ReceiptURO as Receipt, ReceiptMode as ReceiptStatus  # noqa: F401
UROReceipt = Receipt
UROReceiptStatus = ReceiptStatus
GenesisURO = UROGenesis
from uro.base_uros import UROGenesis as _g  # noqa: F401
__all__ += [
    "FULFILLED","DEFERRED","INCAPABLE","UROType","UROStatus","UROState","UROError",
    "UROGenesis","UROFactory","UROSeal","INAHASH","Sigil","Lineage","NTEState",
    "SynapseVector","CustodyChain","Receipt","ReceiptStatus","ReceiptEnvelope",
    "create_uro","get_uro_registry","create_synapse_uro","create_receipt_uro",
    "genesis_uro","seal_inahash","custody_chain","nte_state","UROReceipt",
    "UROReceiptStatus","GenesisURO","UROBus","LedgerEntry","LedgerChain","UROEnvelope",
]

from uro.base_uros import UROCustody, URO_API  # noqa: F401
try:
    __all__ += ["UROCustody", "URO_API"]
except Exception:
    pass


# --- URO_API submodule alias (enables 'from uro.URO_API import ...') ---
import sys as _sys_uapi
import types as _types_uapi
_uapi_name = __name__ + '.URO_API'
if _uapi_name not in _sys_uapi.modules:
    _uapi_mod = _types_uapi.ModuleType(_uapi_name)
    for _sym in ('URO', 'UROType', 'NTEState', 'SynapseVector', 'Receipt', 'ReceiptStatus'):
        if _sym in globals():
            setattr(_uapi_mod, _sym, globals()[_sym])
    _sys_uapi.modules[_uapi_name] = _uapi_mod
    # also expose as attribute of this module for getattr-based access
    globals()['URO_API'] = _uapi_mod


# ---------------------------------------------------------------------------
# Canonical LLM request URO (added during convergence)
# ---------------------------------------------------------------------------

# Re-export LLMRequestURO from coordinator_bus
try:
    from uro.coordinator_bus import LLMRequestURO
except ImportError:
    pass  # Will be defined locally if coordinator_bus unavailable

# --- Convergence compatibility exports (auto-generated) ---
# compat:OrchestrationURO
class OrchestrationURO:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
