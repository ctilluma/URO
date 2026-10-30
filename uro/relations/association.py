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
# MODULE START : uro.relations.association
# ---------------------------------------------------------------------
# FILE         : uro/relations/association.py
# PURPOSE      : Associations - first-class relationship UROs connecting
#                two UROs. The connection carries trust, bond, type, NTE.
# STANDARD     : URO-STD-0001 S5.1, S5.3
# =====================================================================
"""Association UROs - first-class relationships between UROs."""

from __future__ import annotations

import time as _time
from enum import Enum, auto
from typing import Optional

from uro.core.uro import URO
from uro.core.urid import URID

__all__ = ["ConnectionType", "Association"]


class ConnectionType(Enum):
    """The canonical relationship types between two UROs."""
    OUTPUT = auto()
    INPUT = auto()
    LINK = auto()
    CHILD = auto()
    PATH = auto()


class Association(URO):
    """A relationship URO connecting URO a to URO b."""

    def __init__(self, a: URO, b: URO,
                 connection_type: ConnectionType = ConnectionType.LINK) -> None:
        """Create an association between two UROs."""
        _identity = URID.new()
        super().__init__(_identity, _identity, {"kind": "ASSOCIATION"})
        self.a = a
        self.b = b
        self.connection_type = connection_type
        self.trust: float = 0.5
        self.bond: float = 1.0
        self.created_at: float = _time.monotonic()
        self.last_used: float = self.created_at
        self.nte: Optional[object] = None
        a.associate(self)
        b.associate(self)

    def use(self) -> None:
        """Mark the association as used, strengthening the bond."""
        now = _time.monotonic()
        age = now - self.created_at
        growth = 0.1 * (1.0 + min(age / 3600.0, 1.0))
        self.bond += growth
        self.last_used = now

    def decay(self, seconds: float) -> None:
        """Apply natural bond decay over time."""
        age = _time.monotonic() - self.created_at
        rate = 0.01 / (1.0 + min(age / 3600.0, 10.0))
        self.bond = max(0.0, self.bond - rate * seconds)

    def reward(self, amount: float = 0.1) -> None:
        """Increase trust as a reward."""
        self.trust = min(1.0, self.trust + amount)

    def punish(self, amount: float = 0.1) -> None:
        """Decrease trust as punishment."""
        self.trust = max(0.0, self.trust - amount)

    def is_active(self) -> bool:
        """Return True if the bond is still above zero."""
        return self.bond > 0.0

    def __repr__(self) -> str:
        return (f"Association<{self.connection_type.name}>"
                f"(trust={self.trust:.2f}, bond={self.bond:.2f})")
# =====================================================================
# MODULE END   : uro.relations.association
# =====================================================================
