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
# MODULE START : uro.economy.token_transfer
# ---------------------------------------------------------------------
# FILE         : uro/economy/token_transfer.py
# PURPOSE      : Atomic token transfers with 10% network tax (RFC 110,
#                27.1).
# STANDARD     : URO-STD-0001 S35
# =====================================================================
"Atomic token transfers with network tax (RFC 110, 27.1)."

from __future__ import annotations

from typing import Dict

from uro.economy.ledger import GLOBAL_LEDGER

__all__ = ["NETWORK_TAX_RATE", "transfer_tokens"]

NETWORK_TAX_RATE = 0.10


def transfer_tokens(from_account: str, to_account: str, amount: float,
                    ledger=None) -> Dict[str, any]:
    "PURPOSE: Atomic transfer with 10% tax burned; insufficient funds returns error."
    ledger = ledger or GLOBAL_LEDGER
    if ledger.balance(from_account) < amount:
        return {"status": "error", "error": "Insufficient funds"}
    tax = amount * NETWORK_TAX_RATE
    net = amount - tax
    ledger.debit(from_account, amount)
    ledger.credit(to_account, net)
    ledger.credit("network", tax)
    ledger.transactions.append({
        "type": "transfer", "from": from_account, "to": to_account,
        "gross": amount, "tax": tax, "net": net,
    })
    return {"status": "success", "gross": amount, "tax": tax, "net": net}
# =====================================================================
# MODULE END   : uro.economy.token_transfer
# =====================================================================
