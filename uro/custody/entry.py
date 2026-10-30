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
MODULE: Custody Entry URO
INTENT: A single entry in the custody chain. Records who touched the URO,
        when, and under what NTE state.
STANDARD: URO-STD-0001 S11
"""
from __future__ import annotations

import time
from typing import Dict, Optional
from pydantic import BaseModel, Field, ConfigDict

from uro.core.urid import URID
from uro.security.hashing import inahash

__all__ = ["CustodyEntryURO"]


class CustodyEntryURO(BaseModel):
    """
    A single entry in the custody chain.
    
    Records who touched the URO, when, and under what NTE state.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # ── IDENTITY ──────────────────────────────────────
    urid1: URID = Field(default_factory=URID, description="The URO being custodied")
    urid2: URID = Field(default_factory=URID, description="This custody entry's identity")
    
    # ── CUSTODIAN ─────────────────────────────────────
    custodian_urid: URID = Field(default_factory=URID, description="URID of the dock/actor that touched the URO")
    custodian_name: str = Field(default="", description="Human-readable name of the custodian")
    
    # ── TIMESTAMP ─────────────────────────────────────
    timestamp: float = Field(default_factory=time.time, description="When the URO was touched")
    
    # ── OPAR PHASE ────────────────────────────────────
    opar_phase: str = Field(default="Act", description="OPAR phase during custody")
    
    # ── NTE STATE ─────────────────────────────────────
    nte_state_ref: Optional[URID] = Field(None, description="Reference to NTE State URO at time of custody")
    nte_snapshot: Dict[str, float] = Field(
        default_factory=dict,
        description="Snapshot of NTE levels at time of custody (for fast audit)"
    )
    
    # ── INTEGRITY ─────────────────────────────────────
    inahash: str = Field(default="", description="INAHASH seal")
    previous_entry_inahash: Optional[str] = Field(None, description="INAHASH of previous custody entry")
    
    def compute_inahash(self) -> str:
        """Compute the INAHASH seal."""
        data = self.model_dump(exclude={"inahash"})
        msg = str(data).encode()
        return inahash(msg).hex()
    
    def seal(self) -> None:
        """Seal this entry."""
        self.inahash = self.compute_inahash()
