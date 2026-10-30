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


"""Tests for InSPaneda payment and price discovery."""
import pytest

from uro import (Ledger, Currency, PathQuote, best_path, to_micro,
                 from_micro, MICRO)
from uro.exceptions import PaymentError


def test_micro_conversion():
    assert to_micro(1.0) == MICRO
    assert from_micro(MICRO) == 1.0


def test_account_credit_debit():
    ledger = Ledger()
    acct = ledger.create_account("alice")
    ledger.faucet("alice", to_micro(100.0))
    assert acct.balance == 100.0
    acct.debit(to_micro(40.0))
    assert acct.balance == 60.0


def test_insufficient_funds_raises():
    ledger = Ledger()
    ledger.create_account("alice")
    with pytest.raises(PaymentError):
        ledger.account("alice").debit(to_micro(1.0))


def test_transfer_applies_ten_percent_fee():
    ledger = Ledger()
    ledger.create_account("alice")
    ledger.create_account("bob")
    ledger.faucet("alice", to_micro(100.0))
    rec = ledger.transfer("alice", "bob", to_micro(100.0))
    assert rec["fee"] == to_micro(10.0)
    assert rec["net"] == to_micro(90.0)
    assert ledger.account("alice").balance == 0.0
    assert ledger.account("bob").balance == 90.0
    assert ledger.treasury.balance == 10.0


def test_transfer_requires_positive():
    ledger = Ledger()
    ledger.create_account("a"); ledger.create_account("b")
    with pytest.raises(PaymentError):
        ledger.transfer("a", "b", 0)


def test_inspativo_conversion():
    ledger = Ledger()
    acct = ledger.create_account("carol", Currency.INSPATIVO)
    # 1 InSPativo = 1000 InSPaneda = 1000 * MICRO micro-units
    acct.credit(1000 * MICRO)
    assert acct.balance == 1.0


def test_price_discovery_cheapest_wins_on_cost():
    quotes = [
        PathQuote("expensive", cost_micro=to_micro(10.0)),
        PathQuote("cheap", cost_micro=to_micro(1.0)),
    ]
    best = best_path(quotes, {"cost": 1.0})
    assert best.name == "cheap"


def test_price_discovery_weighted_reliability():
    quotes = [
        PathQuote("cheap_flaky", cost_micro=to_micro(1.0), reliability=0.2),
        PathQuote("priced_reliable", cost_micro=to_micro(2.0), reliability=1.0),
    ]
    best = best_path(quotes, {"cost": 0.1, "reliability": 1.0})
    assert best.name == "priced_reliable"
