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
MODULE: Marketplace
INTENT: List/discover/purchase/reuse economic goods; pay royalties; post and
        fill CapabilityGaps with escrowed bounties.
STANDARD: URO-STD-0001 S36

MONEY CONSERVATION:
  * The ledger's record_* methods are the ONLY place balances move.
  * Bounties are escrowed from the requester at post_gap time and released
    from escrow at fill_gap time. No money is ever minted or burned.
"""
from __future__ import annotations

from typing import Dict, List, Any

from uro.economy.goods import EconomicGoodURO, CapabilityGapURO, GoodType
from uro.economy.pricing import price_good
from uro.economy.ledger import GLOBAL_LEDGER

__all__ = ["Marketplace", "GLOBAL_MARKET", "ESCROW"]

ESCROW = "escrow"


class Marketplace:
    def __init__(self, ledger=None):
        self.goods: Dict[str, EconomicGoodURO] = {}
        self.gaps: Dict[str, CapabilityGapURO] = {}
        self.ledger = ledger or GLOBAL_LEDGER

    # --- listing / discovery ---
    def list_good(self, good, trust=50.0, myelination=0, usage=0):
        price_good(good, trust, myelination, usage)
        good.listed = True
        self.goods[good.urid1.to_hex()] = good
        return good

    def discover(self, good_type=None, quadrant=None, min_price=0.0):
        out = [g for g in self.goods.values()
               if g.listed
               and (not good_type or g.good_type == good_type)
               and (not quadrant or g.quadrant == quadrant)
               and g.price >= min_price]
        return sorted(out, key=lambda g: -g.price)

    # --- purchase + reuse (ledger.record_* is the only money mover) ---
    def purchase(self, buyer: str, good_urid: str) -> Dict[str, Any]:
        good = self.goods.get(good_urid)
        if not good or not good.listed:
            return {"status": "error", "error": "Good not listed"}
        if self.ledger.balance(buyer) < good.price:
            return {"status": "error", "error": "Insufficient funds"}
        self.ledger.record_purchase(buyer, good.creator, good_urid, good.price)
        return {"status": "success", "good": good_urid,
                "price": good.price, "owner": buyer}

    def reuse(self, user: str, good_urid: str) -> Dict[str, Any]:
        good = self.goods.get(good_urid)
        if not good:
            return {"status": "error", "error": "Good not found"}
        royalty = round(good.price * good.royalty_rate, 4)
        if royalty > 0:
            if self.ledger.balance(user) < royalty:
                return {"status": "error", "error": "Insufficient funds for royalty"}
            self.ledger.record_royalty(user, good.creator, good_urid, royalty)
        return {"status": "success", "royalty": royalty}

    # --- capability gaps with escrowed bounties ---
    def post_gap(self, gap: CapabilityGapURO):
        if not self.ledger.debit(gap.requester, gap.bounty):
            return None  # requester cannot fund the bounty
        self.ledger.credit(ESCROW, gap.bounty)
        self.gaps[gap.urid1.to_hex()] = gap
        return gap

    def fill_gap(self, gap_urid: str, filler: str) -> Dict[str, Any]:
        gap = self.gaps.get(gap_urid)
        if not gap or gap.filled:
            return {"status": "error", "error": "Gap unavailable"}
        gap.filled = True
        gap.filled_by = filler
        gap.seal()
        self.ledger.debit(ESCROW, gap.bounty)
        self.ledger.credit(filler, gap.bounty)
        return {"status": "success", "gap": gap_urid,
                "bounty": gap.bounty, "filled_by": filler}


GLOBAL_MARKET = Marketplace()
