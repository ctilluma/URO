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
# MODULE START : uro.core.uro
# ---------------------------------------------------------------------
# FILE         : uro/core/uro.py
# PURPOSE      : The Universal Relationship Object. URO = (URID1, URID2).
#                The relationship between source and identifier is the
#                carrier of value.
# STANDARD     : URO-STD-0001 S3.2, S3.3, S3.4
# =====================================================================
"""The core URO class - the universal relationship object."""

from __future__ import annotations

import hashlib as _hashlib
from typing import Any, Dict, Iterable, List, Optional

from uro.constants import LINK_BYTES
from uro.exceptions import UROStructureError
from uro.core.urid import URID

__all__ = ["URO", "sha128"]


def sha128(data: bytes) -> bytes:
    """128-bit digest (SHA-256 truncated to 16 bytes)."""
    return _hashlib.sha256(data).digest()[:16]


class URO:
    """A Universal Relationship Object: (source URID, identifier URID)."""

    __slots__ = (
        "urid1", "urid2", "payload", "parent",
        "children", "associations", "paths", "_meta", "__dict__")

    def __init__(self, urid1: URID = None, urid2: URID = None,
                 payload: Any = None, parent: Optional["URO"] = None, **kwargs) -> None:
        """Construct a URO from two URIDs (auto-generated if omitted). Absorbs genesis kwargs."""
        self.urid1 = urid1 if urid1 is not None else URID()
        self.urid2 = urid2 if urid2 is not None else URID()
        self.payload = payload if payload is not None else (kwargs if kwargs else None)
        self.parent = parent
        self.children: Dict[URID, "URO"] = {}
        self.associations: List[Any] = []
        self.paths: List[Any] = []
        self._meta: Dict[str, Any] = {}

    @classmethod
    def new(cls, payload: Any = None) -> "URO":
        """Create a self-defined URO (URID1 == URID2)."""
        identity = URID.new()
        return cls(identity, identity, payload)

    @classmethod
    def nothing(cls) -> "URO":
        """The URO for the concept of nothing (0x0, 0x0)."""
        return cls(URID.zero(), URID.zero())

    @classmethod
    def everything(cls) -> "URO":
        """The URO for an unbounded group (everything)."""
        return cls(URID.ones(), URID.ones())

    @property
    def is_structure(self) -> bool:
        """True if URID2 all-zeros (structure of URID1)."""
        return self.urid2.is_zero()

    @property
    def is_group(self) -> bool:
        """True if URID2 all-ones (group of URID1s)."""
        return self.urid2.is_ones()

    @property
    def is_self_reference(self) -> bool:
        """True if URID2 == URID1 (entire URID1 objective)."""
        return self.urid1 == self.urid2

    def link(self) -> bytes:
        """Compute the 512-bit relationship link."""
        x = self.urid1.to_int() ^ self.urid2.to_int()
        left = x.to_bytes(32, "big")
        mid = bytes(a ^ b for a, b in zip(sha128(self.urid1.to_bytes()),
                                          sha128(self.urid2.to_bytes())))
        tail = sha128(left + mid)
        return (left + mid + tail)[:LINK_BYTES]

    def add_child(self, child: "URO") -> None:
        """Attach a child URO."""
        if child.urid2 in self.children:
            raise UROStructureError(f"duplicate child URID {child.urid2}")
        child.parent = self
        self.children[child.urid2] = child

    def get_child(self, urid: URID) -> Optional["URO"]:
        """Return a child URO by URID, or None."""
        return self.children.get(urid)

    def children_of(self) -> Iterable["URO"]:
        """Yield all child UROs."""
        return self.children.values()

    def associate(self, association: Any) -> None:
        """Attach an Association URO."""
        self.associations.append(association)

    def add_path(self, path: Any) -> None:
        """Attach a Path URO."""
        self.paths.append(path)

    def __repr__(self) -> str:
        kind = ("structure" if self.is_structure else
                "group" if self.is_group else
                "self" if self.is_self_reference else "object")
        return f"URO<{kind}>({self.urid1.to_hex()[:8]},{self.urid2.to_hex()[:8]})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, URO):
            return NotImplemented
        return self.urid1 == other.urid1 and self.urid2 == other.urid2

    def __hash__(self) -> int:
        return hash((self.urid1, self.urid2))
# =====================================================================
# MODULE END   : uro.core.uro
# =====================================================================
# Rock-solid base build trigger
