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
MODULE: Receipt URO (Tri-Modal Envelope)
INTENT: The Receipt URO is the acknowledgment/response envelope. It carries
        a list of UROs and declares the mode (FULFILLED/DEFERRED/INCAPABLE).
STANDARD: URO-STD-0001 S12
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

from uro.core.urid import URID
from uro.security.hashing import inahash

__all__ = ["ReceiptURO", "ReceiptMode", "ReceiptURO"]


class ReceiptMode:
    """Receipt modes."""
    FULFILLED = "FULFILLED"       # Response URO(s) inline, done
    DEFERRED = "DEFERRED"         # Async, subscribe to Observe queue
    INCAPABLE = "INCAPABLE"       # Cannot process, reason + remediation URO


class ReceiptURO(BaseModel):
    """
    The Receipt URO (tri-modal envelope).
    
    Carries a list of UROs and declares the mode.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # ── IDENTITY ──────────────────────────────────────
    urid1: URID = Field(default_factory=URID, description="The original Request URO")
    urid2: URID = Field(default_factory=URID, description="This Receipt's identity")
    
    # ── MODE ──────────────────────────────────────────
    mode: str = Field(default="FULFILLED", description="FULFILLED | DEFERRED | INCAPABLE")
    
    # ── PAYLOAD (list of UROs) ────────────────────────
    # FULFILLED: response URO(s) inline
    # DEFERRED: tracking/reference URO + complexity class
    # INCAPABLE: reason URO + remediation URO
    payload_uros: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of UROs (response, tracking, or reason/remediation)"
    )
    
    # ── METADATA ──────────────────────────────────────
    complexity_class: Optional[str] = Field(None, description="For DEFERRED: complexity/latency estimate")
    estimated_completion: Optional[float] = Field(None, description="For DEFERRED: ETA in seconds")
    observe_queue_ref: Optional[str] = Field(None, description="For DEFERRED: where to listen for response")
    
    reason: Optional[str] = Field(None, description="For INCAPABLE: why it can't process")
    remediation_suggestion: Optional[str] = Field(None, description="For INCAPABLE: how to resolve")
    
    # ── INTEGRITY ─────────────────────────────────────
    inahash: str = Field(default="", description="INAHASH seal")
    parent_inahash: Optional[str] = Field(None, description="Request URO's INAHASH")
    
    # ── TIMESTAMP ─────────────────────────────────────
    timestamp: float = Field(default_factory=time.time, description="Receipt creation time")
    
    def compute_inahash(self) -> str:
        """Compute the INAHASH seal."""
        data = self.model_dump(exclude={"inahash"})
        msg = str(data).encode()
        return inahash(msg).hex()
    
    def seal(self) -> None:
        """Seal this receipt."""
        self.inahash = self.compute_inahash()
    
    def is_fulfilled(self) -> bool:
        """Check if mode is FULFILLED."""
        return self.mode == ReceiptMode.FULFILLED
    
    def is_deferred(self) -> bool:
        """Check if mode is DEFERRED."""
        return self.mode == ReceiptMode.DEFERRED
    
    def is_incapable(self) -> bool:
        """Check if mode is INCAPABLE."""
        return self.mode == ReceiptMode.INCAPABLE


# --- Genesis convenience: docks call receipt.to_dict() ---
def _uro_to_dict(self):
    try:
        return self.model_dump()
    except Exception:
        return {k: getattr(self, k, None) for k in self.model_fields}
ReceiptURO.to_dict = _uro_to_dict
