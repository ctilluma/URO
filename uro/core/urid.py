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
# MODULE START : uro.core.urid
# ---------------------------------------------------------------------
# FILE         : uro/core/urid.py
# PURPOSE      : URID - Universal Relationship IDentifier (256-bit).
#                URID = UUID1 || UUID2. Atomic addressable identity.
# STANDARD     : URO-STD-0001 S3.1
# =====================================================================
"""URID - Universal Relationship IDentifier (256-bit identity)."""

from __future__ import annotations

import uuid as _uuid

from uro.constants import (
    URID_BITS, URID_BYTES, UUID_BITS,
    URID_INT_ZERO, URID_INT_ONES, UUID_INT_ZERO, UUID_INT_ONES,
)
from uro.exceptions import URIDError

__all__ = ["URID", "new_uuid", "new_urid"]


def new_uuid() -> _uuid.UUID:
    """Generate a new random (UUIDv4) 128-bit UUID."""
    return _uuid.uuid4()


class URID:
    """A 256-bit Universal Relationship IDentifier (UUID1||UUID2)."""

    __slots__ = ("_uuid1", "_uuid2")

    def __init__(self, uuid1: _uuid.UUID = None, uuid2: _uuid.UUID = None) -> None:
        """Construct a URID from two UUID halves."""
        self._uuid1 = uuid1 if uuid1 is not None else new_uuid()
        self._uuid2 = uuid2 if uuid2 is not None else new_uuid()

    @classmethod
    def generate(cls, seed=None, **kwargs) -> "URID":
        """Alias for URID.new() for dock compatibility.

        Many docks pass a semantic label (e.g. URID.generate("capability:x")
        or URID.generate(f"receipt:{id}")). The label is accepted for
        compatibility and a fresh random URID is returned.
        """
        return cls.new()

    @classmethod
    def new(cls) -> "URID":
        """Create a fresh, random URID."""
        return cls(new_uuid(), new_uuid())

    @classmethod
    def zero(cls) -> "URID":
        """All-zero URID (nothing / structure)."""
        return cls(_uuid.UUID(int=UUID_INT_ZERO), _uuid.UUID(int=UUID_INT_ZERO))

    @classmethod
    def ones(cls) -> "URID":
        """All-ones URID (everything / group)."""
        return cls(_uuid.UUID(int=UUID_INT_ONES), _uuid.UUID(int=UUID_INT_ONES))

    @classmethod
    def from_int(cls, value: int) -> "URID":
        """Construct from a 256-bit integer (upper 128 bits = uuid1)."""
        if not (0 <= value <= URID_INT_ONES):
            raise URIDError(f"value out of 256-bit range: {value}")
        u1 = value >> UUID_BITS
        u2 = value & ((1 << UUID_BITS) - 1)
        return cls(_uuid.UUID(int=u1), _uuid.UUID(int=u2))

    @classmethod
    def from_bytes(cls, data: bytes) -> "URID":
        """Construct from a 32-byte big-endian representation."""
        if len(data) != URID_BYTES:
            raise URIDError(f"expected {URID_BYTES} bytes, got {len(data)}")
        return cls.from_int(int.from_bytes(data, "big"))

    @classmethod
    def from_hex(cls, text: str) -> "URID":
        """Construct from a 64-character hex string."""
        return cls.from_int(int(text, 16))

    def to_int(self) -> int:
        """Return the URID as a 256-bit integer."""
        return (self._uuid1.int << UUID_BITS) | self._uuid2.int

    def to_bytes(self) -> bytes:
        """Return the URID as 32 big-endian bytes."""
        return self.to_int().to_bytes(URID_BYTES, "big")

    def to_hex(self) -> str:
        """Return a zero-padded 64-character hex string."""
        return format(self.to_int(), f"0{URID_BYTES * 2}x")

    @property
    def uuid1(self) -> _uuid.UUID:
        """Origin/parent half."""
        return self._uuid1

    @property
    def uuid2(self) -> _uuid.UUID:
        """Local/component half."""
        return self._uuid2

    def is_zero(self) -> bool:
        """True if all-zero (nothing/structure)."""
        return self.to_int() == URID_INT_ZERO

    def is_ones(self) -> bool:
        """True if all-ones (everything/group)."""
        return self.to_int() == URID_INT_ONES

    def __xor__(self, other: "URID") -> "URID":
        """Bitwise XOR two URIDs."""
        return URID.from_int(self.to_int() ^ other.to_int())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, URID):
            return NotImplemented
        return self.to_int() == other.to_int()

    def __hash__(self) -> int:
        return hash(self.to_int())

    def __repr__(self) -> str:
        return f"URID({self.to_hex()})"


def new_urid() -> URID:
    """Convenience: create a fresh random URID."""
    return URID.new()
# =====================================================================
# MODULE END   : uro.core.urid
# =====================================================================


# ============================================================================
# CANONICAL URID UTILITIES
# ============================================================================
def make_urid_pair(dock_id: str, resource_id: str) -> tuple:
    """
    Generates a canonical URID pair (URID1, URID2) for a given dock and resource.
    """
    return (f"uro:{dock_id}", f"res:{resource_id}")
