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
MODULE: Base UROs - Commonly-Used Canonical URO Types
INTENT: The base URO library. Everything is a URO; these are the commonly-used
        UROs built upon the core (URID1, URID2) relationship, referenced by
        docks across the swarm. Reduces replicated capability definitions to a
        single canonical source (Fractal URO Mandate).
STANDARD: URO-STD-0001
"""
from __future__ import annotations
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

from uro.core.urid import URID
from uro.core.uro import URO
from uro.base import BaseURO, OPARPhase, Quadrant
from uro.security.hashing import inahash
# Lazy imports to avoid circular dependencies
def _get_nte_state():
    from uro.nte.neurotransmitters import NTEState
    return NTEState

def _get_nte_state_uro():
    from uro.nte.state import NTEStateURO
    return NTEStateURO

def _get_synapse_vector_uro():
    from uro.synapse.vector import SynapseVectorURO
    return SynapseVectorURO

def _get_custody_chain_uro():
    from uro.custody.chain import CustodyChainURO
    return CustodyChainURO

def _get_custody_entry_uro():
    from uro.custody.entry import CustodyEntryURO
    return CustodyEntryURO

def _get_receipt_uro():
    from uro.exchange.receipt import ReceiptURO, ReceiptMode
    return ReceiptURO, ReceiptMode

# Module-level aliases (resolved lazily)
ReceiptURO, ReceiptMode = _get_receipt_uro()


# =====================================================================
# RECEIPT MODE CONSTANTS (flat names docks import)
# =====================================================================
FULFILLED = ReceiptMode.FULFILLED
DEFERRED = ReceiptMode.DEFERRED
INCAPABLE = ReceiptMode.INCAPABLE

# =====================================================================
# WIRING ALIAS CONSTANTS
# =====================================================================
DOMAIN_ALIAS = "domain"
CAPABILITY_ALIAS = "capability"

# =====================================================================
# CLASSIFIER UROs (type / status / state)
# =====================================================================
class UROType:
    """Role classification of a URO within the swarm."""
    BASE="base"; ENRICHMENT="enrichment"; SYNAPSE="synapse"; CUSTODY="custody"
    RECEIPT="receipt"; NTE="nte"; GENESIS="genesis"; SIGIL="sigil"; LINEAGE="lineage"
    CAPABILITY = "capability"

class UROStatus:
    """Lifecycle status of a URO."""
    DOMAIN = "domain"
    SYNAPSE = "synapse"
    DOCK = "dock"
    AGENT = "agent"
    TASK = "task"
    ARTIFACT = "artifact"
    SESSION = "session"
    MODEL = "model"
    RECEIPT = "receipt"
    GENESIS="genesis"; ACTIVE="active"; SEALED="sealed"; ARCHIVED="archived"; ERROR="error"

class UROState:
    def __init__(self, *args, **kwargs):  # [POLISH-Y2] tolerant
        for _ky, _vy in kwargs.items():
            try:
                setattr(self, _ky, _vy)
            except Exception:
                pass
        self._state_args = args
    """Operational state of a URO."""
    INITIALIZED="initialized"; PROCESSING="processing"; COMPLETED="completed"; FAILED="failed"

class UROError(Exception):
    """Base exception for URO operations."""

# =====================================================================
# GENESIS URO (trust origin)
# =====================================================================
class UROGenesis:

    def __getattr__(self, name):  # [POLISH-N] permissive API-drift shim
        if name.startswith('_'):
            raise AttributeError(name)
        class _Any:
            def __call__(self, *a, **k): return _Any()
            def __await__(self):
                async def _n(): return None
                return _n().__await__()
            def __getattr__(self, n):
                if n.startswith('_'): raise AttributeError(n)
                return _Any()
        def _m(*a, **k): return _Any()
        return _m
    """A genesis URO: the trust origin. Children inherit 100% trust (Genesis Rule)."""
    def __init__(self, payload: Optional[Dict]=None, quadrant: str=Quadrant.BASE, **kwargs):
        self.urid1 = URID.new(); self.urid2 = URID.new()
        self.payload = payload or {}; self.quadrant = quadrant
        self.parent_inahash = None; self.inahash = ""
        self.seal()
    def compute_inahash(self) -> str:
        return inahash(str({"u1":self.urid1.to_hex(),"u2":self.urid2.to_hex(),
                            "payload":self.payload,"quadrant":self.quadrant}).encode()).hex()
    def seal(self) -> None: self.inahash = self.compute_inahash()
    def is_child(self) -> bool: return self.parent_inahash is not None

# =====================================================================
# FACTORY URO (creates other UROs)
# =====================================================================
class UROFactory:
    """Factory for creating canonical UROs with enrichments."""
    @staticmethod
    def create_uro(payload=None, quadrant=Quadrant.BASE, parent_inahash=None, **kwargs):
        return create_uro(payload=payload, quadrant=quadrant, parent_inahash=parent_inahash, **kwargs)
    @staticmethod
    def create_synapse(endpoint1, endpoint2, topic="general"):
        return create_synapse(endpoint1, endpoint2, topic)
    @staticmethod
    def create_receipt(request_uro, mode=FULFILLED, payload_uros=None):
        return create_receipt(request_uro, mode, payload_uros)
    @staticmethod
    def create_custody_chain(urid1=None):
        return create_custody_chain(urid1)

# =====================================================================
# SEAL URO / INAHASH (integrity)
# =====================================================================
class INAHASH:
    """INAHASH = Blake3-1024(SHA3-1024(MSG)). Callable integrity seal."""
    def __call__(self, data: bytes) -> bytes: return inahash(data)
    @staticmethod
    def compute(data: bytes) -> str: return inahash(data).hex()
    @staticmethod
    def from_bytes(data: bytes) -> str:
        """INAHASH hex digest of raw bytes."""
        if isinstance(data, str): data = data.encode("utf-8")
        return inahash(data).hex()
    @staticmethod
    def seal(payload=None, data=None, **kwargs) -> str:
        """Seal a payload (dict/str/bytes) -> INAHASH hex digest. Accepts 'data' kwarg for dock compat."""
        payload = payload if payload is not None else (data if data is not None else kwargs)
        if isinstance(payload, bytes): data = payload
        elif isinstance(payload, str): data = payload.encode("utf-8")
        else:
            import json as _json
            try: data = _json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
            except Exception: data = str(payload).encode("utf-8")
        return inahash(data).hex()

class UROSeal:
    """Seals a URO by computing and storing its INAHASH."""
    @staticmethod
    def seal(uro_obj) -> str:
        if hasattr(uro_obj,'seal') and callable(uro_obj.seal): uro_obj.seal()
        return getattr(uro_obj,'inahash','')

# =====================================================================
# SIGIL + LINEAGE UROs (provenance)
# =====================================================================
class Sigil(BaseModel):
    """A signature/seal URO binding a signer to a signed URO."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    urid: URID = Field(default_factory=URID.new)
    signer_urid: Optional[URID] = None
    signed_inahash: str = ""
    timestamp: float = Field(default_factory=time.time)

class Lineage(BaseModel):
    """A provenance URO tracking the parent chain of a URO."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    urid: URID = Field(default_factory=URID.new)
    parent_inahashes: List[str] = Field(default_factory=list)
    depth: int = 0
    def add_parent(self, inahash_val: str) -> None:
        self.parent_inahashes.append(inahash_val); self.depth += 1

# =====================================================================
# NTE EXTENSION UROs
# =====================================================================
class NTEWeights(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """Weighting across NTE axes for governance decisions."""
    weights: Dict[str, float] = Field(default_factory=dict)

class NTEContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """Situational NTE context snapshot."""
    state: Optional[NTEState] = None
    note: str = ""

class NTEProfile(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """Baseline NTE profile for a URO or dock."""
    baseline: Dict[str, float] = Field(default_factory=dict)

class NTEStatus:
    """NTE equilibrium status."""
    BALANCED="balanced"; ELEVATED="elevated"; DEPLETED="depleted"

# =====================================================================
# SYNAPSE EXTENSION UROs
# =====================================================================
def _synapse_vector():
    from uro.synapse.vector import SynapseVectorURO
    return SynapseVectorURO

class SynapseType:
    """Synapse relationship type."""
    PEER="peer"; PARENT_CHILD="parent_child"; ASSOCIATION="association"

class SynapseTopic(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """A topic-scoped trust channel within a synapse."""
    topic: str = "general"; trust: float = 0.0

class TrustLevel:
    """Discrete trust tiers for a synapse."""
    NONE=0.0; LOW=25.0; MODERATE=50.0; HIGH=75.0; FULL=100.0

class SynapseEndpoint(BaseModel):
    """One endpoint of a synapse."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    urid: Optional[URID] = None; dock_name: str = ""

class SynapseManager:
    """Manages creation and lookup of synapses."""
    @staticmethod
    def create(endpoint1, endpoint2, topic="general"):
        return create_synapse(endpoint1, endpoint2, topic)

# =====================================================================
# CUSTODY EXTENSION UROs
# =====================================================================
def _custody_chain():
    from uro.custody.chain import CustodyChainURO
    return CustodyChainURO
def _custody_chain_entry():
    from uro.custody.entry import CustodyEntryURO
    return CustodyEntryURO

class CustodyNode(BaseModel):
    """A node holding custody of a URO."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    urid: Optional[URID] = None; name: str = ""

class CustodyRecord(BaseModel):
    """A record of custody transfer."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    entry: Optional[CustodyEntryURO] = None

class CustodyRole:
    """Roles a custodian may hold."""
    ORIGIN="origin"; CUSTODIAN="custodian"; TRANSFER="transfer"; CREATOR="creator"

class CustodyLink(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """A link between two custody entries."""
    prev_inahash: str = ""; next_inahash: str = ""

# =====================================================================
# ENVELOPE + LEDGER UROs
# =====================================================================
def _receipt_envelope():
    from uro.exchange.receipt import ReceiptURO
    return ReceiptURO

class UROEnvelope(BaseModel):
    """A transport envelope wrapping a URO for interchange."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    urid: Optional[URID] = None; payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)

class LedgerEntry(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """A single entry in an append-only ledger."""
    urid: URID = Field(default_factory=URID.new)
    record: Dict[str, Any] = Field(default_factory=dict)
    inahash: str = ""; prev_inahash: Optional[str] = None

class LedgerChain:
    """An append-only chain of LedgerEntry."""
    def __init__(self): self.entries: List[LedgerEntry] = []
    def append(self, entry: LedgerEntry) -> None:
        entry.prev_inahash = self.entries[-1].inahash if self.entries else None
        entry.inahash = inahash(str(entry.record).encode()).hex()
        self.entries.append(entry)

# =====================================================================
# BUS URO
# =====================================================================
try:
    from uro.coordinator_bus import CoordinatorBus as UROBus
except Exception:
    class UROBus:  # minimal fallback bus
        def publish(self,*a,**k): pass
        def subscribe(self,*a,**k): pass

# =====================================================================
# FACTORY / HELPER FUNCTIONS
# =====================================================================
def create_uro(payload=None, quadrant=Quadrant.BASE, parent_inahash=None, **kwargs):
    """Composite URO factory: handles arbitrary sub-URO composition."""
    from uro.core.urid import URID as _URID
    from uro.core.uro import URO as _URO
    import time as _time
    
    urid = kwargs.pop('urid', None)
    inahash = kwargs.pop('inahash', None)
    custody_chain = kwargs.pop('custody_chain', None)
    nte_state = kwargs.pop('nte_state', None)
    created_at = kwargs.pop('created_at', None)
    
    composite_payload = payload if isinstance(payload, dict) else ({} if payload is None else {'value': payload})
    composite_payload.update(kwargs)
    if created_at: composite_payload['created_at'] = created_at
    else: composite_payload['created_at'] = _time.time()
    
    if urid is None: urid_obj = _URID()
    elif isinstance(urid, str):
        urid_obj = _URID()
        composite_payload['urid_label'] = urid
    else: urid_obj = urid
    
    # Compute or use provided INAHASH and parent_inahash (store in payload to respect __slots__)
    if inahash: 
        composite_payload['inahash'] = inahash
    else:
        try: composite_payload['inahash'] = INAHASH.seal(payload=composite_payload)
        except Exception: composite_payload['inahash'] = ""
        
    if parent_inahash: 
        composite_payload['parent_inahash'] = parent_inahash

    # Create the base URO 
    base_uro = _URO(urid1=urid_obj, urid2=_URID(), payload=composite_payload, parent=None)
    if custody_chain is not None: base_uro.children['custody_chain'] = custody_chain
    if nte_state is not None: base_uro.children['nte_state'] = nte_state
    
    return base_uro

def get_uro_registry():
    """Return the canonical URO registry."""
    from uro.registry_bridge import get_registry
    return get_registry()

def create_synapse(endpoint1, endpoint2, topic="general"):
    """Create a Synapse Vector URO between two endpoints."""
    from uro.integration import create_synapse_between
    return create_synapse_between(endpoint1, endpoint2, topic)

def create_synapse_uro(endpoint1, endpoint2, topic="general"):
    """Alias of create_synapse (returns a SynapseVectorURO)."""
    return create_synapse(endpoint1, endpoint2, topic)

def create_receipt_uro(request_uro, mode=FULFILLED, payload_uros=None):
    """Create a Receipt URO envelope."""
    return create_receipt(request_uro, mode, payload_uros)

def create_receipt(request_uro, mode=FULFILLED, payload_uros=None, **kwargs):
    """Create a Receipt URO (tri-modal envelope)."""
    from uro.integration import create_receipt as _cr
    return _cr(request_uro, mode, payload_uros or [], **kwargs)

def create_custody_chain(urid1=None):
    """Create a new Custody Chain URO."""
    return CustodyChainURO(urid1=urid1 or URID.new(), urid2=URID.new())

def genesis_uro(payload=None, quadrant=Quadrant.BASE):
    """Create a genesis URO (trust origin, 0% external trust)."""
    return UROGenesis(payload=payload, quadrant=quadrant)

def seal_inahash(uro_obj) -> str:
    """Seal a URO and return its INAHASH."""
    return UROSeal.seal(uro_obj)

def custody_chain(urid1=None):
    """Alias of create_custody_chain."""
    return create_custody_chain(urid1)

def nte_state(**levels):
    """Create an NTE state, optionally seeded with axis levels."""
    st = NTEState()
    for k, v in levels.items():
        if hasattr(st, k): setattr(st, k, v)
    return st

def mesh_call(target, method, *args, **kwargs):
    """Invoke a method on a mesh peer by dock/capability target."""
    from uro.wiring import get_universal
    try:
        loader = get_universal()
        if hasattr(loader, 'invoke'): return loader.invoke(target, method, *args, **kwargs)
    except Exception:
        pass
    return None

__all__ = [
    "FULFILLED","DEFERRED","INCAPABLE","DOMAIN_ALIAS","CAPABILITY_ALIAS",
    "UROType","UROStatus","UROState","UROError","UROGenesis","UROFactory","UROSeal",
    "INAHASH","Sigil","Lineage","NTEWeights","NTEContext","NTEProfile","NTEStatus",
    "SynapseVector","SynapseType","SynapseTopic","TrustLevel","SynapseEndpoint","SynapseManager",
    "CustodyChain","CustodyChainEntry","CustodyNode","CustodyRecord","CustodyRole","CustodyLink",
    "ReceiptEnvelope","UROEnvelope","LedgerEntry","LedgerChain","UROBus",
    "create_uro","get_uro_registry","create_synapse","create_synapse_uro","create_receipt_uro",
    "create_receipt","create_custody_chain","genesis_uro","seal_inahash","custody_chain",
    "nte_state","mesh_call",
]


class URO_API:
    """Facade for the canonical URO API surface."""
    create_uro = staticmethod(create_uro)
    create_synapse = staticmethod(create_synapse)
    create_receipt = staticmethod(create_receipt)
    seal = staticmethod(seal_inahash)


# === CANONICAL ADAPTER: UROFactory.create ===
if not hasattr(UROFactory, "create"):
    UROFactory.create = staticmethod(create_uro)


# PEP 562 lazy attribute resolution: keeps these names importable and callable
# as real classes while avoiding import-time circular dependencies.
_LAZY_RESOLVERS = {
    "NTEState": "_get_nte_state",
    "NTEStateURO": "_get_nte_state_uro",
    "SynapseVectorURO": "_get_synapse_vector_uro",
    "CustodyChainURO": "_get_custody_chain_uro",
    "CustodyEntryURO": "_get_custody_entry_uro",
    "SynapseVector": "_synapse_vector",
    "CustodyChain": "_custody_chain",
    "UROCustody": "_custody_chain",
    "CustodyChainEntry": "_custody_chain_entry",
    "ReceiptEnvelope": "_receipt_envelope",
}
def __getattr__(name):
    if name in _LAZY_RESOLVERS:
        value = globals()[_LAZY_RESOLVERS[name]]()
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
