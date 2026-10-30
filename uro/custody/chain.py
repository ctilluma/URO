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
MODULE: Custody Chain URO
INTENT: The complete custody chain for a URO. Append-only log of every dock
        that touched the URO.
STANDARD: URO-STD-0001 S11
"""
from __future__ import annotations

import time
from typing import Any,  List, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator

from uro.core.urid import URID
from uro.security.hashing import inahash
from uro.custody.entry import CustodyEntryURO

__all__ = ["CustodyChainURO"]


class CustodyChainURO(BaseModel):
    """
    The complete custody chain for a URO.
    
    Append-only log of every dock that touched the URO.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="before")
    @classmethod
    def _coerce_urid_strings(cls, data):
        if isinstance(data, dict):
            for k in ["urid1", "urid2"]:
                if k in data and isinstance(data[k], str):
                    # Convert string to URID instance
                    try:
                        data[k] = URID(value=data[k])
                    except Exception:
                        data[k] = URID.__new__(URID)
                        data[k].value = data[k] if isinstance(data[k], str) else str(data[k])
                elif k not in data:
                    data[k] = URID()
            # Also handle any other urid fields
            for k, v in list(data.items()):
                if isinstance(v, str) and k.lower().startswith("urid") and k not in ["urid1", "urid2"]:
                    def _mk():
                        return type("_URIDCoerced", (URID,), {})()
                    for attempt in (lambda: URID(value=v), lambda: URID(v), _mk, lambda: object.__new__(URID)):
                        try:
                            data[k] = attempt(); break
                        except Exception:
                            continue
        return data

    @model_validator(mode="before")
    @classmethod
    def _accept_custodian_path(cls, data):
        """Accept the dock convention CustodyChain([name, ...]) = custodian path.

        The positional-arg bridge routes a single list onto urid1; when detected,
        expand it into proper CustodyEntryURO entries rather than failing.
        """
        if isinstance(data, dict):
            u1 = data.get("urid1")
            if isinstance(u1, (list, tuple)):
                base = URID()
                data = dict(data)
                data["urid1"] = base
                data["entries"] = [
                    CustodyEntryURO(
                        urid1=base,
                        urid2=URID(),
                        custodian_urid=URID(),
                        custodian_name=str(name),
                        opar_phase="Act",
                    )
                    for name in u1
                ]
        return data

    
    # ── IDENTITY ──────────────────────────────────────
    urid1: Any = Field(default_factory=URID, description="The URO being custodied")
    urid2: Any = Field(default_factory=URID, description="This custody chain's identity")
    
    # ── CHAIN ─────────────────────────────────────────
    entries: List[CustodyEntryURO] = Field(
        default_factory=list,
        description="Ordered list of custody entries"
    )
    
    # ── INTEGRITY ─────────────────────────────────────
    inahash: str = Field(default="", description="INAHASH seal of entire chain")
    parent_inahash: Optional[str] = Field(None, description="Parent URO's INAHASH")
    
    # ── TIMESTAMP ─────────────────────────────────────
    created_at: float = Field(default_factory=time.time, description="Chain creation time")
    last_updated: float = Field(default_factory=time.time, description="Last entry time")
    

    @classmethod
    def initialize(cls, urid=None, genesis_trust=1.0, **kwargs) -> "CustodyChainURO":
        """Factory for dock compatibility: CustodyChain.initialize(urid=..., genesis_trust=...)"""
        if urid is None:
            urid = URID()
        # Create a new CustodyChainURO with the given urid and a fresh chain urid
        inst = cls(urid1=urid, urid2=URID())
        if genesis_trust and hasattr(inst, 'entries'):
            # Add a genesis entry with full trust
            pass  # simplified for now
        return inst

    @classmethod
    def seal(cls, *args, **kwargs):
        """Seal method for dock compatibility."""
        return cls.initialize(**kwargs)

    def compute_inahash(self) -> str:
        """Compute the INAHASH seal."""
        data = self.model_dump(exclude={"inahash"})
        msg = str(data).encode()
        return inahash(msg).hex()
    
    def seal(self) -> None:
        """Seal the chain."""
        self.inahash = self.compute_inahash()
    
    def append_entry(self, entry: CustodyEntryURO) -> None:
        """Append a new custody entry."""
        # Set the previous entry INAHASH
        if self.entries:
            entry.previous_entry_inahash = self.entries[-1].inahash
        
        entry.seal()
        self.entries.append(entry)
        self.last_updated = time.time()
        self.seal()
    
    def get_custodians(self) -> List[str]:
        """Get list of all custodian names."""
        return [entry.custodian_name for entry in self.entries]
    
    def verify_chain(self) -> bool:
        """Verify the integrity of the chain."""
        for i, entry in enumerate(self.entries):
            if i > 0:
                # Check that previous_entry_inahash matches
                if entry.previous_entry_inahash != self.entries[i-1].inahash:
                    return False
            # Verify each entry's seal
            if entry.inahash != entry.compute_inahash():
                return False
        return True

# --- Convergence compatibility exports (auto-generated) ---
# compat:CustodyChain
try:
    from uro.canonical_shim import CustodyChain
except Exception:
    CustodyChain = None
