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
# MODULE START : uro.relations.pathing
# ---------------------------------------------------------------------
# FILE         : uro/relations/pathing.py
# PURPOSE      : Pathing - resolving the most appropriate route between
#                UROs. A Path is a URO of ordered hops.
# STANDARD     : URO-STD-0001 S5.2
# =====================================================================
"""Path UROs and path resolution."""

from __future__ import annotations

from typing import List, Optional

from uro.core.uro import URO
from uro.core.urid import URID

__all__ = ["PathURO", "resolve_path"]


class PathURO(URO):
    """A URO representing an ordered route between UROs."""

    def __init__(self, hops: Optional[List[URO]] = None,
                 priority: int = 0, cost: float = 0.0) -> None:
        """Create a Path URO."""
        _identity = URID.new()
        super().__init__(_identity, _identity, {"kind": "PATH"})
        self.hops: List[URO] = list(hops or [])
        self.priority = priority
        self.cost = cost

    def add_hop(self, uro: URO) -> "PathURO":
        """Append a hop to the path."""
        self.hops.append(uro)
        return self

    def __len__(self) -> int:
        return len(self.hops)

    def __repr__(self) -> str:
        return (f"PathURO(hops={len(self.hops)}, priority={self.priority}, "
                f"cost={self.cost})")


def resolve_path(source: URO, destination: URO,
                 max_depth: int = 16) -> Optional[PathURO]:
    """Resolve a path from source to destination via associations (BFS)."""
    if source is destination:
        return PathURO([source])
    from collections import deque
    queue = deque([(source, [source])])
    seen = {id(source)}
    while queue:
        node, path = queue.popleft()
        if len(path) > max_depth:
            continue
        for assoc in getattr(node, "associations", []):
            for endpoint in ("a", "b"):
                other = getattr(assoc, endpoint, None)
                if other is None or other is node or id(other) in seen:
                    continue
                new_path = path + [other]
                if other is destination:
                    return PathURO(new_path)
                seen.add(id(other))
                queue.append((other, new_path))
    return None
# =====================================================================
# MODULE END   : uro.relations.pathing
# =====================================================================
