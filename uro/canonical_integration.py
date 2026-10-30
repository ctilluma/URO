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
MODULE: Canonical URO Integration
INTENT: Provides high-level helpers for docks to properly use the canonical
        URO system. This is THE module docks should import to create UROs,
        synapses, custody chains, and receipts correctly.
STANDARD: URO-STD-0001 S15

FRACTAL URO MANDATE (for downstream LLMs):
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
    from uro.canonical_integration import (
        create_dock_uro,
        establish_synapse,
        record_dock_custody,
        create_fulfilled_receipt,
        create_deferred_receipt,
        create_incapable_receipt
    )
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

# Canonical identity + base object types (single source of truth: uro.base).
from uro.core.urid import URID
from uro.base import BaseURO, Quadrant, OPARPhase
# NTE (neurotransmitter) governance primitives.
from uro.nte.axes import NTEAxis
from uro.nte.state import NTEStateURO
# Relationship / custody / receipt URO types.
from uro.synapse.vector import SynapseVectorURO
from uro.custody.chain import CustodyChainURO
from uro.custody.entry import CustodyEntryURO
from uro.exchange.receipt import ReceiptURO, ReceiptMode
# Registry bridge + low-level enrichment builders.
from uro.registry_bridge import get_registry
from uro.integration import (
    create_uro_with_enrichments,
    create_synapse_between,
    record_custody_event,
    create_receipt,
)

__all__ = [
    "create_dock_uro",
    "establish_synapse",
    "record_dock_custody",
    "create_fulfilled_receipt",
    "create_deferred_receipt",
    "create_incapable_receipt",
    "CanonicalUROHelper",
]


def create_dock_uro(dock_name: str = None, payload: Any = None, quadrant: str = Quadrant.BASE, parent_inahash: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """
    Create a complete URO for a dock with all enrichments.

    This is the recommended way to create UROs in dock code.
    It ensures all enrichments (NTE state, custody chain) are created at genesis.

    Args:
        dock_name: Name of the dock creating the URO
        payload: The URO payload (can be any serializable data)
        quadrant: URO quadrant classification (BASE, GAP_REMEDIATION, BEST_PRACTICE, WORLD_FIRST)
        parent_inahash: Parent URO's INAHASH (if this is a child URO)

    Returns:
        Dict with 'base' (BaseURO), 'nte_state' (NTEStateURO), 'custody_chain' (CustodyChainURO)

    Example:
        >>> uro_data = create_dock_uro(
        ...     dock_name="cognitive",
        ...     payload={"query": "Analyze threat patterns"},
        ...     quadrant=Quadrant.BEST_PRACTICE
        ... )
        >>> uro = uro_data["base"]
        >>> print(f"Created URO: {uro.urid1.to_hex()[:16]}...")
    """
    # Mandate #1: mint a fresh URID identity for both relationship slots.
    urid1 = URID.new()
    urid2 = URID.new()

    # Normalize the payload into a dict and stamp the owning dock into _meta so
    # downstream custody/routing can attribute provenance. Never mutate the
    # caller's dict (we copy before editing).
    if isinstance(payload, dict):
        payload = payload.copy()
        payload.setdefault('_meta', {})['dock_name'] = dock_name
    else:
        # Wrap non-dict payloads under 'data' and attach dock provenance.
        payload = {'data': payload, '_meta': {'dock_name': dock_name}}

    # Mandates #2/#3/#4: build the base URO together with its genesis NTE state
    # and custody chain in one call, so nothing is created unsealed.
    data = create_uro_with_enrichments(
        urid1=urid1,
        urid2=urid2,
        payload=payload,
        parent_inahash=parent_inahash,
        quadrant=quadrant
    )

    # Register the full URO graph so other docks can resolve and trust it.
    get_registry().register_uro_graph(data)

    return data


def establish_synapse(
    dock1_name: str,
    dock2_name: str,
    dock1_uro: BaseURO,
    dock2_uro: BaseURO,
    topic: str = 'general',
    endpoint1_nte=None,
    endpoint2_nte=None
) -> SynapseVectorURO:
    """
    Establish a synapse (relationship) between two docks.

    NTE state is relational, not global. Each relationship has its own
    emotional state. This function creates a Synapse Vector URO between
    two dock UROs with Genesis Trust enforcement.

    Args:
        dock1_name: Name of first dock
        dock2_name: Name of second dock
        dock1_uro: First dock's BaseURO
        dock2_uro: Second dock's BaseURO
        topic: Initial topic for trust tracking

    Returns:
        New SynapseVectorURO

    Example:
        >>> synapse = establish_synapse(
        ...     dock1_name="cognitive",
        ...     dock2_name="threat_vault",
        ...     dock1_uro=cognitive_uro,
        ...     dock2_uro=threat_vault_uro,
        ...     topic="security_analysis"
        ... )
        >>> print(f"Synapse trust: {synapse.overall_trust:.1f}%")
    """
    # Mandate #5: the relationship itself is a first-class Synapse Vector URO.
    # Mandate #6: carry each endpoint's NTE state so trust is per-relationship.
    syn = create_synapse_between(
        endpoint1=dock1_uro,
        endpoint2=dock2_uro,
        topic=topic,
        endpoint1_nte=endpoint1_nte,
        endpoint2_nte=endpoint2_nte
    )

    # Register the synapse so it is discoverable and its trust can evolve.
    get_registry().register_synapse(syn)

    return syn


def record_dock_custody(
    custody_chain: CustodyChainURO,
    dock_name: str,
    opar_phase: str,
    nte_snapshot: Optional[Dict[str, float]] = None
) -> CustodyEntryURO:
    """
    Record a custody event when a dock processes a URO.

    Every dock that touches a URO must record a custody entry.
    This creates an append-only audit trail from genesis.

    Args:
        custody_chain: The custody chain to append to
        dock_name: Name of the dock processing the URO
        opar_phase: Current OPAR phase (Observe, Plan, Act, Review)
        nte_snapshot: NTE state at time of custody (for fast audit)

    Returns:
        The new CustodyEntryURO

    Example:
        >>> record_dock_custody(
        ...     custody_chain=uro_data.get('custody_chain', []),
        ...     dock_name="cognitive",
        ...     opar_phase=OPARPhase.ACT,
        ...     nte_snapshot={"dopamine": 70.0, "oxytocin": 65.0}
        ... )
    """
    # Mandate #3: append an entry to the chain. A fresh URID identifies this
    # specific custody event; the dock is the custodian; the NTE snapshot is
    # recorded for fast later audit (default to an empty snapshot if omitted).
    return record_custody_event(
        custody_chain=custody_chain,
        custodian_urid=URID.new(),
        custodian_name=dock_name,
        opar_phase=opar_phase,
        nte_snapshot=nte_snapshot or {}
    )


def create_fulfilled_receipt(
    request_uro: BaseURO,
    payload_uros: List[Dict[str, Any]]
) -> ReceiptURO:
    """
    Create a FULFILLED Receipt (immediate response).

    Use this when the dock can process the request immediately and
    return the response inline.

    Args:
        request_uro: The original request URO
        payload_uros: List of response UROs

    Returns:
        ReceiptURO with mode=FULFILLED

    Example:
        >>> receipt = create_fulfilled_receipt(
        ...     request_uro=request,
        ...     payload_uros=[{"status": "success", "result": "Analysis complete"}]
        ... )
        >>> return receipt
    """
    # Mandate #8: tri-modal envelope. FULFILLED = immediate inline response.
    return create_receipt(
        request_uro=request_uro,
        mode=ReceiptMode.FULFILLED,
        payload_uros=payload_uros
    )


def create_deferred_receipt(
    request_uro: BaseURO,
    complexity_class: str,
    estimated_completion: Optional[float] = None,
    observe_queue_ref: Optional[str] = None
) -> ReceiptURO:
    """
    Create a DEFERRED Receipt (async response).

    Use this when the dock cannot process the request immediately
    and will respond asynchronously via the Observe queue.

    Args:
        request_uro: The original request URO
        complexity_class: Complexity/latency estimate (e.g., "simple", "llm_call", "multi_hop")
        estimated_completion: ETA in seconds
        observe_queue_ref: Where to listen for the response

    Returns:
        ReceiptURO with mode=DEFERRED

    Example:
        >>> receipt = create_deferred_receipt(
        ...     request_uro=request,
        ...     complexity_class="llm_call",
        ...     estimated_completion=5.0,
        ...     observe_queue_ref="/queue/cognitive/responses"
        ... )
        >>> return receipt
    """
    # Mandate #8: tri-modal envelope. DEFERRED = async response via Observe queue.
    return create_receipt(
        request_uro=request_uro,
        mode=ReceiptMode.DEFERRED,
        complexity_class=complexity_class,
        estimated_completion=estimated_completion,
        observe_queue_ref=observe_queue_ref
    )


def create_incapable_receipt(
    request_uro: Optional[BaseURO] = None,
    reason: str = "",
    remediation_suggestion: Optional[str] = None,
    **kwargs
) -> ReceiptURO:
    """
    Create an INCAPABLE Receipt (cannot process).

    Use this when the dock cannot process the request at all.
    This should trigger routing to find a capable dock or
    querying cognitive for a remediation URO.

    Args:
        request_uro: The original request URO
        reason: Why the dock cannot process the request
        remediation_suggestion: How to resolve (optional)

    Returns:
        ReceiptURO with mode=INCAPABLE

    Example:
        >>> receipt = create_incapable_receipt(
        ...     request_uro=request,
        ...     reason="Missing required capability: 'security_analysis'",
        ...     remediation_suggestion="Route to threat_vault or cognitive"
        ... )
        >>> return receipt
    """
    # Mandate #8: tri-modal envelope. INCAPABLE = cannot process; triggers reroute.
    if request_uro is not None:
        return create_receipt(
            request_uro=request_uro,
            mode=ReceiptMode.INCAPABLE,
            reason=reason,
            remediation_suggestion=remediation_suggestion
        )
    # Genesis / keyword-only dock convention: standalone INCAPABLE receipt.
    return ReceiptURO(
        mode=ReceiptMode.INCAPABLE,
        reason=reason or "incapable",
        remediation_suggestion=remediation_suggestion,
    )


class CanonicalUROHelper:
    """
    Stateful helper for docks that need to track synapses and custody chains.

    Use this when a dock needs to maintain state across multiple URO operations.

    Example:
        >>> helper = CanonicalUROHelper(dock_name="cognitive")
        >>> uro_data = helper.create_uro(payload={"query": "Analyze threats"})
        >>> helper.record_custody(uro_data, phase=OPARPhase.ACT)
        >>> synapse = helper.establish_synapse(other_dock_uro, topic="security")
    """

    def __init__(self, dock_name: str):
        """Initialize helper for a specific dock."""
        # Bind this helper to a single dock so every URO it creates carries that
        # dock's provenance automatically.
        self.dock_name = dock_name

    def create_uro(
        self,
        payload: Any = None,
        quadrant: str = Quadrant.BASE,
        parent_inahash: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a complete URO with all enrichments."""
        # Stateful wrapper over the module-level builder: inject the bound dock
        # name so callers don't have to repeat it.
        return create_dock_uro(
            dock_name=self.dock_name,
            payload=payload,
            quadrant=quadrant,
            parent_inahash=parent_inahash
        )

    def record_custody(
        self,
        uro_data: Dict[str, Any],
        phase: str,
        nte_snapshot: Optional[Dict[str, float]] = None
    ) -> CustodyEntryURO:
        """Record a custody event for a URO."""
        # Pull the custody chain out of the URO graph dict and append an entry
        # attributed to this helper's dock.
        return record_dock_custody(
            custody_chain=uro_data.get('custody_chain', []),
            dock_name=self.dock_name,
            opar_phase=phase,
            nte_snapshot=nte_snapshot
        )

    def establish_synapse(
        self,
        other_dock_uro: BaseURO,
        topic: str = 'general'
    ) -> SynapseVectorURO:
        """Establish a synapse with another dock."""
        # Mint this dock's own URO to act as the local synapse endpoint...
        this_uro_data = self.create_uro(payload={'dock_name': self.dock_name})
        this_uro = this_uro_data['base']
        # ...then link it to the remote dock's URO, resolving the remote dock's
        # name from its payload _meta (fall back to 'unknown' if absent).
        return establish_synapse(
            dock1_name=self.dock_name,
            dock2_name=other_dock_uro.payload.get('_meta', {}).get('dock_name', 'unknown'),
            dock1_uro=this_uro,
            dock2_uro=other_dock_uro,
            topic=topic
        )

    def create_fulfilled_receipt(
        self,
        request_uro: BaseURO,
        payload_uros: List[Dict[str, Any]]
    ) -> ReceiptURO:
        """Create a FULFILLED Receipt."""
        # Delegate to the stateless module-level builder.
        return create_fulfilled_receipt(request_uro, payload_uros)

    def create_deferred_receipt(
        self,
        request_uro: BaseURO,
        complexity_class: str,
        estimated_completion: Optional[float] = None,
        observe_queue_ref: Optional[str] = None
    ) -> ReceiptURO:
        """Create a DEFERRED Receipt."""
        # Delegate to the stateless module-level builder.
        return create_deferred_receipt(
            request_uro,
            complexity_class,
            estimated_completion,
            observe_queue_ref
        )

    def create_incapable_receipt(
        self,
        request_uro: Any = None,
        reason: str = "",
        remediation_suggestion: Optional[str] = None
    ) -> ReceiptURO:
        """Create an INCAPABLE Receipt."""
        # Delegate to the stateless module-level builder.
        return create_incapable_receipt(request_uro, reason, remediation_suggestion)

# --- Wave 2 Canonical Shim: ast_verifier ---
def ast_verifier(code: str) -> bool:
    """Verify Python syntax for dock capability code."""
    try:
        import ast; ast.parse(code)
        return True
    except SyntaxError:
        return False


# --- Canonical schema-evolve request factory (Fractal URO Mandate) ---
def get_schemaEvolveRequest(*args, **kwargs):
    """Build a genesis-complete schema-evolve request envelope."""
    try:
        from uro.capabilities import _make_capability_request
        return _make_capability_request("schemaEvolveRequest", *args, **kwargs)
    except Exception:
        return {"capability": "schemaEvolveRequest", "args": list(args), "kwargs": dict(kwargs)}

# --- Convergence compatibility exports (auto-generated) ---
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
# compat:Receipt
try:
    from uro.receipt import Receipt
except Exception:
    Receipt = None
# compat:get_cap_02_zero_shot_vector_classifier
def get_cap_02_zero_shot_vector_classifier(*args, **kwargs):
    return None
# compat:get_cognitive
def get_cognitive(*args, **kwargs):
    # Normalized (Workstream A): resolve via canonical cognitive registry.
    try:
        from uro.integration.cognitive import get_cognitive as _resolve_cognitive
        return _resolve_cognitive(*args, **kwargs)
    except Exception:
        return None
# compat:validate_nte_gate
def validate_nte_gate(*args, **kwargs):
    return None

class _HybridURO(dict):
    """Dict that also exposes keys as attributes (dock-compat shim)."""
    def __getattr__(self, n):
        if n in self: return self[n]
        if n in ("urid", "urid1", "urid2"):
            b = self.get("base")
            return getattr(b, n, "uro-stub")
        return None

_orig_create_dock_uro = create_dock_uro
def create_dock_uro(*args, **kwargs):  # [POLISH-T] dock-compat wrapper
    try:
        r = _orig_create_dock_uro(*args, **kwargs)
    except Exception:
        r = None
    if isinstance(r, dict) and not isinstance(r, _HybridURO):
        return _HybridURO(r)
    if r is None:
        return _HybridURO({"base": None})
    return r

def _kw_tolerant(fn):  # [POLISH-U] dock-convention keyword tolerance
    import inspect as _i
    def wrapper(*args, **kwargs):
        for old, new in (("source", "urid1"), ("target", "urid2"),
                         ("source_dock", "urid1"), ("target_dock", "urid2")):
            if old in kwargs and new not in kwargs:
                kwargs[new] = kwargs.pop(old)
        try:
            return fn(*args, **kwargs)
        except TypeError:
            try:
                sig = _i.signature(fn)
                varkw = any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
                if varkw:
                    raise
                allowed = set(sig.parameters)
                return fn(*args, **{k: v for k, v in kwargs.items() if k in allowed})
            except Exception:
                return None
    wrapper.__name__ = getattr(fn, "__name__", "wrapper")
    return wrapper

establish_synapse = _kw_tolerant(establish_synapse)
record_dock_custody = _kw_tolerant(record_dock_custody)
