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
# MODULE START : uro.inspaneda
# ---------------------------------------------------------------------
# FILE         : uro/inspaneda.py
# PURPOSE      : InSPaneda / InSPativo payment UROs. Facilitates payment
#                and price discovery between objects using cryptocurrency
#                micropayments.
#
#                From the standard:
#                  - 1 InSPativo = 1000 InSPaneda.
#                  - InSPativo holds 2 decimals; InSPaneda holds 4.
#                  - All InSPa transactions are debited 10% (protocol fee).
#                  - Payment facilitation: verify balance, then transact.
#                  - Price discovery: total cost of a path, weighted by
#                    requirements (cost, latency, reliability, speed).
#
#                Amounts are stored as integer micro-units to avoid float
#                error. Base unit = InSPaneda scaled by 10^4 (4 decimals).
# STANDARD     : URO-STD-0001 S-InSPaneda (Payment URO)
# =====================================================================
"""InSPaneda / InSPativo payment and price-discovery UROs."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional

from uro.core.uro import URO
from uro.core.urid import URID
from uro.exceptions import PaymentError

__all__ = ["Currency", "Account", "Ledger", "PathQuote", "weighted_score",
           "best_path", "to_micro", "from_micro", "MICRO",
           "INSPANEDA_PER_INSPATIVO", "FEE_PERCENT"]

MICRO = 10 ** 4                       # InSPaneda has 4 decimal places.
INSPANEDA_PER_INSPATIVO = 1000        # 1 InSPativo = 1000 InSPaneda.
FEE_PERCENT = 10                      # 10% protocol fee.


class Currency(Enum):
    """The two InSPa cryptocurrencies."""
    INSPANEDA = auto()
    INSPATIVO = auto()


def to_micro(amount: float) -> int:
    """Convert an InSPaneda float to integer micro-units.

    Args:
        amount: Amount in InSPaneda.

    Returns:
        int: Amount in micro-units (InSPaneda * 10^4).
    """
    return int(round(amount * MICRO))


def from_micro(micro: int) -> float:
    """Convert integer micro-units back to an InSPaneda float.

    Args:
        micro: Amount in micro-units.

    Returns:
        float: Amount in InSPaneda.
    """
    return micro / MICRO


class Account(URO):
    """A URO holding a balance for an owner.

    Attributes:
        owner: The owner identifier.
        currency: The denomination of the account.
        balance_micro: Balance in micro-units.
    """

    def __init__(self, owner: str,
                 currency: Currency = Currency.INSPANEDA) -> None:
        """Create an account URO.

        Args:
            owner: The owner identifier.
            currency: The account denomination.
        """
        _identity = URID.new()
        super().__init__(_identity, _identity, {"kind": "PAY.ACCT"})
        self.owner = owner
        self.currency = currency
        self.balance_micro: int = 0

    def credit(self, amount_micro: int) -> None:
        """Add micro-units to the balance.

        Args:
            amount_micro: Non-negative amount to add.

        Raises:
            PaymentError: If the amount is negative.
        """
        if amount_micro < 0:
            raise PaymentError("credit amount must be non-negative")
        self.balance_micro += amount_micro

    def debit(self, amount_micro: int) -> None:
        """Remove micro-units from the balance.

        Args:
            amount_micro: Non-negative amount to remove.

        Raises:
            PaymentError: If insufficient funds or negative amount.
        """
        if amount_micro < 0:
            raise PaymentError("debit amount must be non-negative")
        if amount_micro > self.balance_micro:
            raise PaymentError(
                f"insufficient funds: have {self.balance_micro}, "
                f"need {amount_micro}")
        self.balance_micro -= amount_micro

    @property
    def balance(self) -> float:
        """Balance expressed in the account currency."""
        if self.currency is Currency.INSPATIVO:
            return from_micro(self.balance_micro) / INSPANEDA_PER_INSPATIVO
        return from_micro(self.balance_micro)


class Ledger(URO):
    """The payment ledger: accounts, transfers, and the protocol fee.

    Attributes:
        accounts: Mapping of owner -> Account.
        treasury: The InSPa treasury account collecting fees.
        transactions: A log of completed transfers.
    """

    def __init__(self) -> None:
        """Create a ledger with a treasury account."""
        _identity = URID.new()
        super().__init__(_identity, _identity, {"kind": "PAY.LEDGER"})
        self.accounts: Dict[str, Account] = {}
        self.treasury = Account("InSPa Treasury")
        self.transactions: List[dict] = []
        self.add_child(self.treasury)

    def create_account(self, owner: str,
                       currency: Currency = Currency.INSPANEDA) -> Account:
        """Create and register an account.

        Args:
            owner: The owner identifier.
            currency: The account denomination.

        Returns:
            Account: The new account.

        Raises:
            PaymentError: If the owner already has an account.
        """
        if owner in self.accounts:
            raise PaymentError(f"account already exists for {owner}")
        acct = Account(owner, currency)
        self.accounts[owner] = acct
        self.add_child(acct)
        return acct

    def account(self, owner: str) -> Account:
        """Return an account by owner.

        Args:
            owner: The owner identifier.

        Returns:
            Account: The account.

        Raises:
            PaymentError: If the owner has no account.
        """
        acct = self.accounts.get(owner)
        if acct is None:
            raise PaymentError(f"no account for {owner}")
        return acct

    def faucet(self, owner: str, amount_micro: int) -> None:
        """Mint micro-units into an owner's account (for tests/bootstrap).

        Args:
            owner: The owner identifier.
            amount_micro: Amount to mint.
        """
        self.account(owner).credit(amount_micro)

    def transfer(self, from_owner: str, to_owner: str,
                 amount_micro: int) -> dict:
        """Transfer funds, applying the 10% protocol fee to the treasury.

        The sender is debited the full amount; the recipient is credited
        amount - fee; the treasury is credited the fee.

        Args:
            from_owner: Sender owner identifier.
            to_owner: Recipient owner identifier.
            amount_micro: Amount to transfer (micro-units).

        Returns:
            dict: A record of the transfer.

        Raises:
            PaymentError: On insufficient funds or bad amount.
        """
        if amount_micro <= 0:
            raise PaymentError("transfer amount must be positive")
        src = self.account(from_owner)
        dst = self.account(to_owner)
        fee = (amount_micro * FEE_PERCENT) // 100
        net = amount_micro - fee
        src.debit(amount_micro)
        dst.credit(net)
        self.treasury.credit(fee)
        record = {"from": from_owner, "to": to_owner,
                  "amount": amount_micro, "fee": fee, "net": net}
        self.transactions.append(record)
        return record


@dataclass
class PathQuote:
    """A priced path option used in price discovery.

    Attributes:
        name: A label for the option.
        cost_micro: Total cost in micro-units.
        latency: Relative latency (lower is better).
        reliability: Reliability in [0,1] (higher is better).
        speed: Relative throughput (higher is better).
    """
    name: str
    cost_micro: int
    latency: float = 1.0
    reliability: float = 1.0
    speed: float = 1.0


def weighted_score(quotes: List[PathQuote],
                   weights: Dict[str, float]) -> Dict[str, float]:
    """Score each quote against weighted requirements.

    Higher score is better. Cost and latency are inverted (lower is
    better) and normalized across the provided options.

    Args:
        quotes: The candidate path quotes.
        weights: Weights keyed by "cost", "latency", "reliability", "speed".

    Returns:
        Dict[str, float]: Mapping of quote name to score.

    Raises:
        PaymentError: If no quotes are supplied.
    """
    if not quotes:
        raise PaymentError("no quotes supplied")
    min_cost = min(q.cost_micro for q in quotes) or 1
    min_lat = min(q.latency for q in quotes) or 1.0
    max_speed = max(q.speed for q in quotes) or 1.0
    scores: Dict[str, float] = {}
    for q in quotes:
        score = 0.0
        score += weights.get("cost", 0.0) * (min_cost / (q.cost_micro or 1))
        score += weights.get("latency", 0.0) * (min_lat / (q.latency or 1.0))
        score += weights.get("reliability", 0.0) * q.reliability
        score += weights.get("speed", 0.0) * (q.speed / max_speed)
        scores[q.name] = score
    return scores


def best_path(quotes: List[PathQuote],
              weights: Dict[str, float]) -> PathQuote:
    """Select the best-priced path that serves the weighted requirements.

    Args:
        quotes: The candidate path quotes.
        weights: Weights keyed by "cost", "latency", "reliability", "speed".

    Returns:
        PathQuote: The highest-scoring quote.
    """
    scores = weighted_score(quotes, weights)
    best_name = max(scores, key=lambda k: scores[k])
    for q in quotes:
        if q.name == best_name:
            return q
    raise PaymentError("unable to select best path")
# =====================================================================
# MODULE END   : uro.inspaneda
# =====================================================================
