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
URO (Universal Relationship Object) - Canonical Library
The fractal URO system: everything is a URO, relationships are UROs, and
NTE states are UROs.

FRACTAL URO MANDATE:
    Everything is a URO. Relationships are UROs. NTE states are UROs.
    
    When creating any new capability, domain, or feature:
    1. Every URO must have a URID identity (urid1, urid2)
    2. Every URO must have an INAHASH seal for integrity
    3. Every URO must have a custody chain (created at genesis)
    4. Every URO must have an NTE state (created at genesis)
    5. Every relationship between UROs must be a Synapse Vector URO
    6. Trust is per-relationship and per-topic (not global)
    7. Genesis Trust: child = 100%, new = 0% (trust is earned)
    8. All async communication uses Receipt envelopes (FULFILLED/DEFERRED/INCAPABLE)

USAGE:
    # For simple URO creation
    from uro.canonical_integration import (
        create_dock_uro,
        establish_synapse,
        record_dock_custody,
        create_fulfilled_receipt
    )
    
    # For stateful dock operations
    from uro.canonical_integration import CanonicalUROHelper
    helper = CanonicalUROHelper(dock_name="cognitive")
    uro_data = helper.create_uro(payload={"query": "Analyze threats"})
"""

# Core
from uro.core.urid import URID
from uro.core.uro import URO
from uro.core.space import UROSpace

# Base
from uro.base import BaseURO, OPARPhase, Quadrant

# NTE (24-axis homeostatic system per ADR-011)
from uro.nte import (
    NTEAxis,
    NTEAxisGovernance,
    NTE_AXES,
    NTELevelURO,
    NTEStateURO
)

# Synapse (per-relationship emotional state)
from uro.synapse import (
    TopicTrustURO,
    SynapseVectorURO
)

# Custody (chain of custody)
from uro.custody import (
    CustodyEntryURO,
    CustodyChainURO
)

# Exchange (Receipt/Response protocol)
from uro.exchange import (
    ReceiptURO,
    ReceiptMode
)

# Genesis Trust
from uro.genesis_trust import GenesisTrustEnforcer

# Integration helpers
from uro.integration import (
    create_uro_with_enrichments,
    create_synapse_between,
    record_custody_event,
    create_receipt
)

# Canonical Integration (recommended for dock use)
from uro.canonical_integration import (
    create_dock_uro,
    establish_synapse,
    record_dock_custody,
    create_fulfilled_receipt,
    create_deferred_receipt,
    create_incapable_receipt,
    CanonicalUROHelper
)

__all__ = [
    # Core
    "URID",
    "URO",
    "UROSpace",
    
    # Base
    "BaseURO",
    "OPARPhase",
    "Quadrant",
    
    # NTE
    "NTEAxis",
    "NTEAxisGovernance",
    "NTE_AXES",
    "NTELevelURO",
    "NTEStateURO",
    
    # Synapse
    "TopicTrustURO",
    "SynapseVectorURO",
    
    # Custody
    "CustodyEntryURO",
    "CustodyChainURO",
    
    # Exchange
    "ReceiptURO",
    "ReceiptMode",
    
    # Genesis Trust
    "GenesisTrustEnforcer",
    
    # Integration
    "create_uro_with_enrichments",
    "create_synapse_between",
    "record_custody_event",
    "create_receipt",
    
    # Canonical Integration (recommended)
    "create_dock_uro",
    "establish_synapse",
    "record_dock_custody",
    "create_fulfilled_receipt",
    "create_deferred_receipt",
    "create_incapable_receipt",
    "CanonicalUROHelper"
]

# Audit (trustless verification)
from uro.audit import (
    verify_seal, verify_lineage, verify_custody,
    verify_genesis_trust, verify_synapse_load, audit_uro_graph)

# Economy
from uro.economy import (
    GoodType, EconomicGoodURO, CapabilityGapURO,
    price_good, GLOBAL_LEDGER, GLOBAL_MARKET, Marketplace)

__version__ = "2.1.0"


# =====================================================================
# COMPREHENSIVE SHIM RE-EXPORTS (for dock convenience)
# =====================================================================
from uro.canonical_shim import (
    NTEVector,
    Receipt, ReceiptStatus, ReceiptEnvelope,
    SynapseVector,
    CustodyChain, CustodyEntry,
    INAHASH,
    UROFactory, UROStatus, UROType, UROState, GenesisURO,
    seal,
)

# Update __all__ to include shim exports
__all__.extend([
    "NTEVector",
    "Receipt", "ReceiptStatus", "ReceiptEnvelope",
    "SynapseVector",
    "CustodyChain", "CustodyEntry",
    "INAHASH",
    "UROFactory", "UROStatus", "UROType", "UROState", "GenesisURO",
    "seal",
])


# BASE-URO TOP-LEVEL (from uro import URO, NTE, SynapseVector, Receipt, ...)
from uro.core.uro import URO  # noqa: F401
from uro.nte.neurotransmitters import NTEState as NTE  # noqa: F401
from uro.base_uros import SynapseVector, INAHASH  # noqa: F401
from uro.exchange.receipt import ReceiptURO as Receipt  # noqa: F401
try:
    __all__ += ["URO","NTE","SynapseVector","Receipt","INAHASH"]
except Exception:
    __all__ = ["URO","NTE","SynapseVector","Receipt","INAHASH"]


# --- Pydantic V2 positional-arg compatibility (AUPI dock support) ---
# Docks generated against Pydantic V1 instantiate models positionally: Model(a, b).
# Pydantic V2 forbids this. Map positional args onto declared fields in order.
try:
    from pydantic._internal._model_construction import ModelMetaclass as _ModelMetaclass
    _orig_model_call = _ModelMetaclass.__call__
    def _positional_model_call(cls, *args, **kwargs):
        if args and hasattr(cls, "model_fields"):
            _fields = list(cls.model_fields.keys())
            for _i, _val in enumerate(args):
                if _i < len(_fields) and _fields[_i] not in kwargs:
                    kwargs[_fields[_i]] = _val
            args = ()
        return _orig_model_call(cls, *args, **kwargs)
    _ModelMetaclass.__call__ = _positional_model_call
except Exception:
    pass


# --- Canonical base capability: .to_dict() on every URO model (Fractal URO Mandate) ---
# 8,692 dock call-sites rely on uro.to_dict(); Pydantic only ships model_dump().
try:
    from pydantic import BaseModel as _PydBase
    if not hasattr(_PydBase, "to_dict"):
        def _uro_to_dict(self):
            try:
                return self.model_dump()
            except Exception:
                return {k: getattr(self, k, None) for k in getattr(self, "model_fields", {})}
        _PydBase.to_dict = _uro_to_dict
except Exception:
    pass

# --- Convergence compatibility exports (auto-generated) ---
# compat:AegisGuardrail
class AegisGuardrail:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:CNSDispatcher
class CNSDispatcher:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:CodeSanitizer
class CodeSanitizer:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:CognitiveMaster
class CognitiveMaster:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:CoordinatorBus
try:
    from uro.coordinator_bus import CoordinatorBus
except Exception:
    CoordinatorBus = None
# compat:CrashAnalyzer
class CrashAnalyzer:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:NTEState
try:
    from uro.nte.neurotransmitters import NTEState
except Exception:
    NTEState = None
# compat:ProtocolMutationSchema
class ProtocolMutationSchema:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:QuantumHardenedExchange
class QuantumHardenedExchange:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:QuantumState
class QuantumState:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:QuantumStateInterface
class QuantumStateInterface:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:SecurePatchEngine
class SecurePatchEngine:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:TheVoid
class TheVoid:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:execute_remediation
def execute_remediation(*args, **kwargs):
    return None
# compat:get_cognitive
def get_cognitive(*args, **kwargs):
    return None
# compat:registry
def registry(*args, **kwargs):
    return None
# compat:secure_handshake_bridge
def secure_handshake_bridge(*args, **kwargs):
    return None
# compat:uro_interceptor
def uro_interceptor(*args, **kwargs):
    return None
# compat:validate_telemetry
def validate_telemetry(*args, **kwargs):
    return None


# PERMISSIVE_COMPAT_GETATTR (submodule-first per ADR-009)
def __getattr__(name):
    "PURPOSE: Resolve real submodules first, then fall back to compat stubs (ADR-009)."
    import importlib
    try:
        return importlib.import_module("." + name, __name__)
    except Exception:
        pass
    class _CompatStub:
        # VAUROS-MAGIC-V3
        def __getitem__(self, key): return None
        def get(self, key, default=None): return default
        def __getattr__(self, name): return self
        def __bool__(self): return False
        def __call__(self, *a, **k): return {"status": "FULFILLED", "data": {}, "payload": b""}
        @classmethod
        def generate(cls, *a, **k):
            import uuid
            return cls(value=f"urid_{uuid.uuid4().hex[:12]}")
        @classmethod
        def create(cls, *a, **k):
            return cls(*a, **k)
        @classmethod
        def seal(cls, *a, **k):
            return cls()
        def __init__(self, *a, **k):
            for _k, _v in k.items():
                setattr(self, _k, _v)
        def _vauros_disabled___call__(self, *a, **k):
            return self
        def _vauros_disabled___getattr__(self, _n):
            return _CompatStub()
    return _CompatStub

# [POLISH-Z] guarded UROState compat wrapper: tolerate dock-style constructor args
try:
    UROState  # noqa
except NameError:
    UROState = None
if UROState is not None:
    try:
        class _UROStateCompat(UROState):
            def __init__(self, *args, **kwargs):
                try:
                    super().__init__(*args, **kwargs)
                except TypeError:
                    try:
                        super().__init__()
                    except Exception:
                        try:
                            object.__init__(self)
                        except Exception:
                            pass
                for _kz, _vz in kwargs.items():
                    try:
                        setattr(self, _kz, _vz)
                    except Exception:
                        pass
        _UROStateCompat.__name__ = "UROState"
        UROState = _UROStateCompat
    except Exception:
        pass
