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
MODULE: NTE Level URO (Per-Axis State)
INTENT: A URO representing the level of a single NTE axis. Each level is its
        own URO with lineage, custody, and INAHASH.
STANDARD: URO-STD-0001 S10.1
"""
from __future__ import annotations

import time
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from uro.core.urid import URID
from uro.security.hashing import inahash
from uro.nte.axes import NTEAxis

__all__ = ["NTELevelURO"]


class NTELevelURO(BaseModel):
    """
    A URO representing the level of a single NTE axis.
    
    This is a first-class URO with its own identity, lineage, and custody.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # ── IDENTITY ──────────────────────────────────────
    urid1: URID = Field(..., description="Parent URO (e.g., the dock or synapse)")
    urid2: URID = Field(..., description="This NTE level's identity")
    
    # ── AXIS ──────────────────────────────────────────
    axis: NTEAxis = Field(..., description="Which NTE axis this level represents")
    
    # ── STATE ─────────────────────────────────────────
    level: float = Field(50.0, ge=0.0, le=100.0, description="Current level (0-100)")
    baseline: float = Field(50.0, ge=0.0, le=100.0, description="Resting baseline")
    
    # ── INTEGRITY ─────────────────────────────────────
    inahash: str = Field(default="", description="INAHASH seal")
    parent_inahash: Optional[str] = Field(None, description="Parent URO's INAHASH")
    
    # ── TIMESTAMP ─────────────────────────────────────
    timestamp: float = Field(default_factory=time.time, description="Last update time")
    
    def compute_inahash(self) -> str:
        """Compute the INAHASH seal."""
        data = self.model_dump(exclude={"inahash"})
        msg = str(data).encode()
        return inahash(msg).hex()
    
    def seal(self) -> None:
        """Seal this URO."""
        self.inahash = self.compute_inahash()
    
    def set_level(self, new_level: float) -> None:
        """Set the level and update timestamp."""
        self.level = max(0.0, min(100.0, new_level))
        self.timestamp = time.time()
    
    def apply_delta(self, delta: float) -> None:
        """Apply a delta to the level."""
        self.set_level(self.level + delta)
