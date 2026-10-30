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
MODULE: Economic Goods (everything sellable is a URO)
INTENT: Wrap swarm assets as sellable UROs with lineage, custody, and trust.
STANDARD: URO-STD-0001 S33

GOOD TYPES:
  * SynapseTemplate:  a proven relationship pattern (per-topic trust config)
  * TrustBundle:      a packaged set of high-trust synapses
  * EmotionalHistory: an NTE trajectory (valuable for training/audit)
  * AuditTrail:       a custody chain (compliance product)
  * CapabilityGap:    an unmet need with a bounty (demand side)
"""
from __future__ import annotations

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ConfigDict

from uro.core.urid import URID
from uro.security.hashing import inahash

__all__ = ["GoodType", "EconomicGoodURO", "CapabilityGapURO"]


class GoodType:
    SYNAPSE_TEMPLATE = "synapse_template"
    TRUST_BUNDLE = "trust_bundle"
    EMOTIONAL_HISTORY = "emotional_history"
    AUDIT_TRAIL = "audit_trail"


class EconomicGoodURO(BaseModel):
    """A sellable asset, itself a URO with lineage and integrity."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    urid1: URID = Field(...)
    urid2: URID = Field(...)

    good_type: str = Field(...)
    title: str = ""
    description: str = ""
    quadrant: str = "Base"

    # The underlying asset (synapse config, NTE history, custody chain, etc.)
    asset: Dict[str, Any] = Field(default_factory=dict)

    # Provenance: who created it and the source UROs it derives from
    creator: str = ""
    source_urids: List[str] = Field(default_factory=list)

    # Economic state
    listed: bool = False
    price: float = 0.0
    royalty_rate: float = 0.05   # fraction paid to creator on each reuse

    inahash: str = Field(default="")

    def seal(self):
        data = self.model_dump(exclude={"inahash"})
        self.inahash = inahash(str(data).encode()).hex()

    @classmethod
    def new(cls, good_type, title, asset, creator="", quadrant="Base",
            description="", source_urids=None) -> "EconomicGoodURO":
        u = URID.new()
        g = cls(urid1=u, urid2=URID.new(), good_type=good_type, title=title,
                description=description, quadrant=quadrant, asset=asset,
                creator=creator, source_urids=source_urids or [])
        g.seal()
        return g


class CapabilityGapURO(BaseModel):
    """An unmet capability need with a bounty (the demand side)."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    urid1: URID = Field(...)
    urid2: URID = Field(...)

    gap_description: str = ""
    quadrant: str = "Gap Remediation"
    bounty: float = 0.0
    requester: str = ""
    filled_by: Optional[str] = None
    filled: bool = False

    inahash: str = Field(default="")

    def seal(self):
        data = self.model_dump(exclude={"inahash"})
        self.inahash = inahash(str(data).encode()).hex()

    @classmethod
    def new(cls, gap_description, bounty, requester) -> "CapabilityGapURO":
        u = URID.new()
        g = cls(urid1=u, urid2=URID.new(), gap_description=gap_description,
                bounty=bounty, requester=requester)
        g.seal()
        return g
