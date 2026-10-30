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
MODULE: Integration Helpers
INTENT: Helper functions to integrate the canonical URO system with existing
        infrastructure (RegistryMaster, UROSpace, CoordinatorBus).
STANDARD: URO-STD-0001 S14
"""
from __future__ import annotations

from typing import Optional, Dict, Any
from uro.core.urid import URID
from uro.core.uro import URO
from uro.base import BaseURO
from uro.synapse.vector import SynapseVectorURO
from uro.custody.chain import CustodyChainURO
from uro.custody.entry import CustodyEntryURO
from uro.nte.state import NTEStateURO
from uro.exchange.receipt import ReceiptURO, ReceiptMode
from uro.genesis_trust import GenesisTrustEnforcer

__all__ = [
    "create_uro_with_enrichments",
    "create_synapse_between",
    "record_custody_event",
    "create_receipt"
]




def compute_synapse_load(nte1, nte2, native_baseline: float = 50.0) -> dict:
    """
    Compute the synapse load as the COMBINATION of both endpoints' states.

    Each endpoint contributes its effective state = (native crossed with current).
    The synapse load = the shared combination of both effective states.

    Args:
        nte1: First endpoint NTEStateURO
        nte2: Second endpoint NTEStateURO
        native_baseline: The native (baseline) level for each axis

    Returns:
        Dict[NTEAxis, float] of the combined synapse load
    """
    from uro.nte.axes import NTEAxis
    load = {}
    for axis in NTEAxis:
        cur1 = nte1.get_level(axis) if nte1 else native_baseline
        cur2 = nte2.get_level(axis) if nte2 else native_baseline
        eff1 = (native_baseline + cur1) / 2.0  # native crossed with current
        eff2 = (native_baseline + cur2) / 2.0
        load[axis] = (eff1 + eff2) / 2.0       # shared between the two
    return load


def create_uro_with_enrichments(
    urid1: URID,
    urid2: URID,
    payload: Any = None,
    parent_inahash: Optional[str] = None,
    quadrant: str = "Base"
) -> Dict[str, Any]:
    """
    Create a complete URO with all enrichment UROs (NTE State, Custody Chain).
    
    This is the recommended way to create UROs - it ensures all enrichments
    are created at genesis.
    
    Args:
        urid1: Source URID
        urid2: Instance URID
        payload: URO payload
        parent_inahash: Parent URO's INAHASH (if this is a child)
        quadrant: URO quadrant classification
        
    Returns:
        Dict with base URO and all enrichment UROs
    """
    # Create base URO
    base_uro = BaseURO(
        urid1=urid1,
        urid2=urid2,
        payload=payload or {},
        parent_inahash=parent_inahash,
        quadrant=quadrant
    )
    
    # Create NTE State URO
    nte_state = NTEStateURO(
        urid1=urid1,
        urid2=URID.new(),
        parent_inahash=base_uro.compute_inahash()
    )
    nte_state.seal()
    
    # Create Custody Chain URO
    custody_chain = CustodyChainURO(
        urid1=urid1,
        urid2=URID.new(),
        parent_inahash=base_uro.compute_inahash()
    )
    
    # Add genesis custody entry
    genesis_entry = CustodyEntryURO(
        urid1=urid1,
        urid2=URID.new(),
        custodian_urid=urid1,
        custodian_name="genesis",
        opar_phase=base_uro.opar_phase,
        nte_snapshot=nte_state.levels
    )
    genesis_entry.seal()
    custody_chain.append_entry(genesis_entry)
    
    # Link enrichments to base URO
    base_uro.nte_state_ref = nte_state.urid2
    base_uro.custody_chain_ref = custody_chain.urid2
    
    # Seal the base URO
    base_uro.seal()
    
    return {
        "base": base_uro,
        "nte_state": nte_state,
        "custody_chain": custody_chain
    }


def create_synapse_between(
    endpoint1: BaseURO,
    endpoint2: BaseURO,
    topic: str = "general",
    endpoint1_nte=None,
    endpoint2_nte=None
) -> SynapseVectorURO:
    """
    Create a synapse between two UROs with Genesis Trust enforcement.
    
    Args:
        endpoint1: First endpoint URO
        endpoint2: Second endpoint URO
        topic: Initial topic for trust tracking
        
    Returns:
        New SynapseVectorURO
    """
    # Create synapse URID
    synapse_urid = URID.new()
    
    # Create NTE state for the synapse
    nte_state = NTEStateURO(
        urid1=synapse_urid,
        urid2=URID.new()
    )
    nte_state.seal()
    
    # Create synapse
    synapse = SynapseVectorURO(
        urid1=endpoint1.urid1,
        urid2=endpoint2.urid1,
        synapse_urid=synapse_urid,
        nte_state=nte_state
    )
    
    # Apply the COMBINED synapse load from both endpoints' states
    if endpoint1_nte is not None or endpoint2_nte is not None:
        load = compute_synapse_load(endpoint1_nte, endpoint2_nte)
        for axis, value in load.items():
            synapse.nte_state.set_level(axis, value)

    # Initialize trust using Genesis Rule
    GenesisTrustEnforcer.initialize_synapse_trust(synapse, endpoint1, endpoint2)
    
    # Add initial topic if not already added
    if topic not in synapse.topic_trusts:
        synapse.add_topic_trust(topic, synapse.overall_trust)
    
    synapse.seal()
    return synapse


def record_custody_event(
    custody_chain: CustodyChainURO,
    custodian_urid: URID,
    custodian_name: str,
    opar_phase: str,
    nte_snapshot: Dict[str, float]
) -> CustodyEntryURO:
    """
    Record a custody event in the chain.
    
    Args:
        custody_chain: The custody chain to append to
        custodian_urid: URID of the custodian
        custodian_name: Name of the custodian
        opar_phase: Current OPAR phase
        nte_snapshot: NTE state at time of custody
        
    Returns:
        The new custody entry
    """
    entry = CustodyEntryURO(
        urid1=custody_chain.urid1,
        urid2=URID.new(),
        custodian_urid=custodian_urid,
        custodian_name=custodian_name,
        opar_phase=opar_phase,
        nte_snapshot=nte_snapshot,
        previous_entry_inahash=custody_chain.entries[-1].inahash if custody_chain.entries else None
    )
    entry.seal()
    custody_chain.append_entry(entry)
    return entry


def create_receipt(
    request_uro: BaseURO,
    mode: str,
    payload_uros: list = None,
    **kwargs
) -> ReceiptURO:
    """
    Create a Receipt URO (tri-modal envelope).
    
    Args:
        request_uro: The original request URO
        mode: Receipt mode (FULFILLED/DEFERRED/INCAPABLE)
        payload_uros: List of UROs to include in the receipt
        **kwargs: Additional metadata (complexity_class, reason, etc.)
        
    Returns:
        New ReceiptURO
    """
    receipt = ReceiptURO(
        urid1=request_uro.urid1,
        urid2=URID.new(),
        mode=mode,
        payload_uros=payload_uros or [],
        parent_inahash=request_uro.inahash,
        **kwargs
    )
    receipt.seal()
    return receipt
