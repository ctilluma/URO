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
MODULE: Registry Bridge (Phase A - Make the graph real)
INTENT: Registers UROs and their enrichments into a shared, queryable graph.
        This is the in-memory single source of truth for the live fractal
        graph. (Next step: mirror to the registry dock for cross-process.)
STANDARD: URO-STD-0001 S22
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from uro.core.urid import URID

__all__ = ["RegistryBridge", "get_registry"]


class RegistryBridge:
    """
    A shared, queryable index of the live URO graph.

    Stores base UROs, NTE states, custody chains, and synapses, keyed by
    URID hex, and provides resolution + neighborhood queries.
    """

    _instance: Optional["RegistryBridge"] = None

    def __new__(cls) -> "RegistryBridge":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self) -> None:
        self.uros: Dict[str, Any] = {}        # hex -> BaseURO
        self.nte: Dict[str, Any] = {}         # hex -> NTEStateURO
        self.custody: Dict[str, Any] = {}     # hex -> CustodyChainURO
        self.synapses: Dict[str, Any] = {}    # hex -> SynapseVectorURO
        self.matrices: Dict[str, Any] = {}    # hex -> FuzzyMatrixURO
        self.by_dock: Dict[str, List[str]] = {}  # dock_name -> [base hex]

    # --- Registration ---
    def register_uro_graph(self, uro_data: Dict[str, Any]) -> str:
        """Register a base URO + its enrichments. Returns the base hex URID."""
        base = uro_data["base"]
        hex1 = base.urid1.to_hex()

        self.uros[hex1] = base
        if "nte_state" in uro_data:
            self.nte[hex1] = uro_data["nte_state"]
        if "custody_chain" in uro_data:
            self.custody[hex1] = uro_data["custody_chain"]

        dock = base.payload.get("_meta", {}).get("dock_name") if isinstance(base.payload, dict) else None
        if dock:
            self.by_dock.setdefault(dock, []).append(hex1)
        return hex1

    def register_synapse(self, synapse: Any) -> str:
        """Register a Synapse Vector URO. Returns its synapse hex URID."""
        shex = synapse.synapse_urid.to_hex()
        self.synapses[shex] = synapse
        return shex

    # --- Resolution ---
    def register_matrix(self, matrix: Any) -> str:
        h = matrix.urid1.to_hex()
        self.matrices[h] = matrix
        return h

    def resolve(self, hex_urid: str) -> Optional[Any]:
        """Resolve a hex URID to whatever URO it refers to."""
        return (self.uros.get(hex_urid) or self.nte.get(hex_urid)
                or self.custody.get(hex_urid) or self.synapses.get(hex_urid)
                or self.matrices.get(hex_urid))

    def synapses_for(self, dock_name: str) -> List[Any]:
        """All synapses a dock participates in."""
        out = []
        for s in self.synapses.values():
            # synapse endpoints are stored as urid1/urid2 of the two docks
            for hex1 in self.by_dock.get(dock_name, []):
                if hex1 in (s.urid1.to_hex(), s.urid2.to_hex()):
                    out.append(s)
        return out

    def custody_for(self, hex_urid: str) -> Optional[Any]:
        return self.custody.get(hex_urid)

    def verify_chain(self, hex_urid: str) -> bool:
        chain = self.custody.get(hex_urid)
        return chain.verify_chain() if chain else False

    def stats(self) -> Dict[str, int]:
        return {
            "uros": len(self.uros),
            "nte_states": len(self.nte),
            "custody_chains": len(self.custody),
            "synapses": len(self.synapses),
            "docks": len(self.by_dock),
        }


def get_registry() -> RegistryBridge:
    """Get the shared RegistryBridge singleton."""
    return RegistryBridge()

# --- Convergence compatibility exports (auto-generated) ---
# compat:CNSDispatcher
class CNSDispatcher:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:CapabilityHandler
class CapabilityHandler:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
