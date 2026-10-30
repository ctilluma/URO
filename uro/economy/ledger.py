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
MODULE: FinOps Ledger (micropayments + royalties)
INTENT: Record every transaction and per-use royalty immutably.
STANDARD: URO-STD-0001 S35
"""
from __future__ import annotations

import time
from typing import Dict, List, Any

__all__ = ["Ledger", "GLOBAL_LEDGER"]


class Ledger:
    def __init__(self):
        self.transactions: List[Dict[str, Any]] = []
        self.balances: Dict[str, float] = {}

    def credit(self, account: str, amount: float):
        self.balances[account] = self.balances.get(account, 0.0) + amount

    def debit(self, account: str, amount: float) -> bool:
        if self.balances.get(account, 0.0) < amount:
            return False
        self.balances[account] -= amount
        return True

    def record_purchase(self, buyer, seller, good_urid, amount):
        self.transactions.append({
            "type": "purchase", "buyer": buyer, "seller": seller,
            "good": good_urid, "amount": amount, "time": time.time()})
        self.debit(buyer, amount)
        self.credit(seller, amount)

    def record_royalty(self, payer, creator, good_urid, amount):
        self.transactions.append({
            "type": "royalty", "payer": payer, "creator": creator,
            "good": good_urid, "amount": amount, "time": time.time()})
        self.debit(payer, amount)
        self.credit(creator, amount)

    def balance(self, account: str) -> float:
        return self.balances.get(account, 0.0)


GLOBAL_LEDGER = Ledger()
