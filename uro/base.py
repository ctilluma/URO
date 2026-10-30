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
MODULE: Base URO + Canonical Enumerations
INTENT: Defines BaseURO - the enriched, sealable Universal Relationship Object
        that every dock creates and exchanges - together with the two canonical
        string enumerations that classify a URO's OPAR lifecycle phase and its
        value quadrant.
STANDARD: URO-STD-0001 S3.2 (URO), S8 (OPAR), S9.1 (INAHASH)

FRACTAL URO MANDATE:
    BaseURO is the runtime carrier of the (urid1, urid2) relationship. It is
    born with a genesis custody chain and NTE state (see uro.integration), and
    it is sealed with an INAHASH so any child URO can reference its parent by
    parent_inahash and inherit 100% Genesis Trust.

    - urid1             : source / producer identity
    - urid2             : instance / message identity
    - payload           : carried data (provenance in payload['_meta'])
    - quadrant          : value classification (Quadrant.*)
    - opar_phase        : current lifecycle phase (OPARPhase.*)
    - parent_inahash    : parent's seal (None => genesis URO, 0% trust)
    - inahash           : this URO's own seal (set by seal())
    - nte_state_ref     : URID of this URO's NTE State URO
    - custody_chain_ref : URID of this URO's Custody Chain URO
"""
from __future__ import annotations

import time
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field

from uro.core.urid import URID
from uro.security.hashing import inahash

__all__ = ["BaseURO", "OPARPhase", "Quadrant"]


# =====================================================================
# CANONICAL STRING ENUMERATIONS
# ---------------------------------------------------------------------
# These are *string* constants (not Enum members) so they can be stored
# directly in the `opar_phase` / `quadrant` str fields of every URO and
# round-trip through the pydantic API models (uro/api/models.py) unchanged.
# They follow the same convention as the sibling uro.exchange.receipt
# .ReceiptMode constant class.
# =====================================================================
class OPARPhase:
    """The four OPAR lifecycle phases (Observe -> Plan -> Act -> Review)."""

    OBSERVE = "Observe"   # Gather internal state + external inputs
    PLAN = "Plan"         # Decide how to process the observations
    ACT = "Act"           # Execute the plan, produce output
    REVIEW = "Review"
    IDLE = "Idle"     # Evaluate the outcome, learn, improve


class Quadrant:
    """Value-quadrant classification of a URO's contribution."""

    BASE = "Base"                              # Baseline / required function
    GAP_REMEDIATION = "Gap Remediation"        # Closes a known gap
    BEST_PRACTICE = "Best Practice"            # Matches industry best practice
    WORLD_FIRST = "World-First Innovation"     # Novel, world-first capability


# =====================================================================
# BASE URO
# =====================================================================
class BaseURO(BaseModel):
    """
    The enriched, sealable Universal Relationship Object.

    A BaseURO is the runtime carrier of the (urid1, urid2) relationship. Docks
    create it (canonical_integration.create_dock_uro), enrich it with a genesis
    NTE state and custody chain (integration.create_uro_with_enrichments), seal
    it with an INAHASH, and exchange it through the swarm. Child UROs reference
    their parent by parent_inahash to inherit Genesis Trust.
    """

    # Permit non-pydantic field types (URID) inside the model.
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # ── IDENTITY ──────────────────────────────────────
    urid1: URID = Field(..., description="Source / producer URID")
    urid2: URID = Field(..., description="Instance / message URID")

    # ── PAYLOAD ───────────────────────────────────────
    # Provenance is stamped into payload['_meta']['dock_name'] by
    # canonical_integration.create_dock_uro.
    payload: Dict[str, Any] = Field(default_factory=dict, description="Carried data")

    # ── CLASSIFICATION ────────────────────────────────
    quadrant: str = Field(default=Quadrant.BASE, description="Value quadrant (Quadrant.*)")
    opar_phase: str = Field(default=OPARPhase.OBSERVE, description="Current OPAR phase (OPARPhase.*)")

    # ── LINEAGE / INTEGRITY ───────────────────────────
    # parent_inahash is None for a genesis URO (0% trust) and set for a child
    # URO (100% trust to parent) - see uro.genesis_trust.GenesisTrustEnforcer.
    parent_inahash: Optional[str] = Field(default=None, description="Parent URO's INAHASH seal")
    inahash: str = Field(default="", description="This URO's INAHASH seal (set by seal())")

    # ── ENRICHMENT REFERENCES ─────────────────────────
    # Populated by integration.create_uro_with_enrichments after it builds the
    # genesis NTE state and custody chain.
    nte_state_ref: Optional[URID] = Field(default=None, description="URID of this URO's NTE State URO")
    custody_chain_ref: Optional[URID] = Field(default=None, description="URID of this URO's Custody Chain URO")

    # ── TIMESTAMP ─────────────────────────────────────
    timestamp: float = Field(default_factory=time.time, description="Creation time")

    # ── INTEGRITY METHODS ─────────────────────────────
    def compute_inahash(self) -> str:
        """
        Compute the INAHASH seal over every field except the seal itself.

        Mirrors the sibling URO pattern (ReceiptURO / CustodyEntryURO): dump
        the model excluding `inahash`, serialize, then apply the composite
        Blake3-1024(SHA3-1024(msg)) hash from uro.security.hashing.
        """
        data = self.model_dump(exclude={"inahash"})
        msg = str(data).encode()
        return inahash(msg).hex()

    def seal(self) -> None:
        """Seal this URO by storing its computed INAHASH."""
        self.inahash = self.compute_inahash()

    # ── LINEAGE HELPERS ───────────────────────────────
    def is_child(self) -> bool:
        """
        True if this URO descends from a parent (has a parent_inahash).

        Used by uro.genesis_trust.GenesisTrustEnforcer to apply the Genesis
        Rule: children start at 100% trust, genesis UROs at 0%.
        """
        return self.parent_inahash is not None