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


# =====================================================================
# MODULE START : uro.core.space
# ---------------------------------------------------------------------
# FILE         : uro/core/space.py
# PURPOSE      : UROSpace - the shared, hierarchical, communal registry
#                of every URO and every relationship between them.
# STANDARD     : URO-STD-0001 S6
# =====================================================================
"""UROSpace - the communal registry/graph of all UROs and relationships."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

from uro.exceptions import UROStructureError
from uro.core.urid import URID
from uro.core.uro import URO

__all__ = ["UROSpace"]


class UROSpace:
    """A shared space holding UROs and the relationships between them."""

    def __init__(self, name: str = "root") -> None:
        """Create a new UROSpace."""
        self.name = name
        self._objects: Dict[Tuple[int, int], URO] = {}
        self._relationships: Dict[bytes, URO] = {}

    def register(self, uro: URO) -> URO:
        """Register an object URO."""
        key = (uro.urid1.to_int(), uro.urid2.to_int())
        if key in self._objects:
            raise UROStructureError("URO already registered in space")
        self._objects[key] = uro
        return uro

    def register_relationship(self, relationship_uro: URO) -> URO:
        """Register a relationship URO by its 512-bit link."""
        self._relationships[relationship_uro.link()] = relationship_uro
        return relationship_uro

    def get(self, urid1: URID, urid2: URID) -> Optional[URO]:
        """Look up an object URO by its two URIDs."""
        return self._objects.get((urid1.to_int(), urid2.to_int()))

    def relationship(self, link: bytes) -> Optional[URO]:
        """Look up a relationship URO by its link bytes."""
        return self._relationships.get(link)

    def objects(self) -> Iterable[URO]:
        """Yield all object UROs."""
        return self._objects.values()

    def relationships(self) -> Iterable[URO]:
        """Yield all relationship UROs."""
        return self._relationships.values()

    def neighbors(self, uro: URO) -> List[URO]:
        """Return UROs directly associated with the given URO."""
        result: List[URO] = []
        for assoc in getattr(uro, "associations", []):
            for endpoint in ("a", "b"):
                other = getattr(assoc, endpoint, None)
                if isinstance(other, URO) and other is not uro:
                    result.append(other)
        return result

    def __len__(self) -> int:
        return len(self._objects) + len(self._relationships)

    def __repr__(self) -> str:
        return (f"UROSpace({self.name!r}, objects={len(self._objects)}, "
                f"relationships={len(self._relationships)})")
# =====================================================================
# MODULE END   : uro.core.space
# =====================================================================
