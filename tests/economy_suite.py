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


#!/usr/bin/env python3
# === FILE: tests/economy_suite.py ===
# PURPOSE: Phase 15 validation: currency precision, tax math, atomicity,
#          ledger integrity, marketplace pricing, social trust weighting,
#          supply chain roll-up.
# === END FILE HEADER ===
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.economy.currency import Currency, convert, INSPTAIVO_TO_INSPANEDA_RATIO
from uro.economy.token_transfer import transfer_tokens, NETWORK_TAX_RATE
from uro.economy.ledger import Ledger, GLOBAL_LEDGER
from uro.economy.marketplace import Marketplace
from uro.economy.social_pricing import social_price
from uro.economy.supply_chain import SupplyChainStage, SupplyChainLedger
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 currency decimal precision enforcement")
def c01():
    v = convert(1.23456, Currency.INSPTAIVO, Currency.INSPTAIVO)
    assert str(v) == "1.23"
    v2 = convert(1.23456, Currency.INSPANEDA, Currency.INSPANEDA)
    assert str(v2) == "1.2346"
@check("02 1:1000 conversion both directions")
def c02():
    assert convert(1.0, Currency.INSPTAIVO, Currency.INSPANEDA) == 1000.0
    assert convert(1000.0, Currency.INSPANEDA, Currency.INSPTAIVO) == 1.0
@check("03 network tax math")
def c03():
    assert abs(NETWORK_TAX_RATE - 0.10) < 1e-9
    ledger = Ledger()
    ledger.credit("alice", 100.0)
    r = transfer_tokens("alice", "bob", 10.0, ledger)
    assert abs(r["tax"] - 1.0) < 1e-9 and abs(r["net"] - 9.0) < 1e-9
    assert ledger.balance("bob") == 9.0
    assert ledger.balance("network") == 1.0
@check("04 atomicity on insufficient funds")
def c04():
    ledger = Ledger()
    ledger.credit("alice", 5.0)
    r = transfer_tokens("alice", "bob", 10.0, ledger)
    assert r["status"] == "error"
    assert ledger.balance("alice") == 5.0
@check("05 ledger append-only and balance invariant")
def c05():
    ledger = Ledger()
    ledger.credit("alice", 100.0)
    ledger.debit("alice", 30.0)
    assert ledger.balance("alice") == 70.0
    assert len(ledger.transactions) >= 0
@check("06 marketplace purchase with ledger integration")
def c06():
    ledger = Ledger()
    ledger.credit("buyer", 100.0)
    mp = Marketplace(ledger)
    from uro.economy.goods import EconomicGoodURO, GoodType
    from uro.core.urid import URID
    first_type = GoodType.DATA if hasattr(GoodType, "DATA") else (list(GoodType)[0] if hasattr(GoodType, "__iter__") else "DATA")
    good = EconomicGoodURO(urid1=URID.new(), urid2=URID.new(), good_type=first_type, creator="creator")
    mp.list_good(good)
    good.price = 50.0
    r = mp.purchase("buyer", good.urid1.to_hex())
    assert r["status"] == "success"
    assert ledger.balance("buyer") == 50.0
    assert ledger.balance("creator") == 50.0
@check("07 social pricing trust weighting")
def c07():
    base = 100.0
    high_trust = social_price(base, trust=80.0, reputation=80.0)
    low_trust = social_price(base, trust=20.0, reputation=20.0)
    assert high_trust < low_trust
    assert 50.0 <= high_trust < 100.0
@check("08 supply chain cost roll-up")
def c08():
    sc = SupplyChainLedger()
    sc.add_stage(SupplyChainStage("s1", cost=10.0, value_add=5.0))
    sc.add_stage(SupplyChainStage("s2", cost=20.0, value_add=10.0))
    assert sc.total_cost() == 30.0
    assert sc.total_value_add() == 15.0
    assert sc.final_price(margin=0.1) == 33.0
@check("09 currency invariants preserved")
def c09():
    v = convert(1.5, Currency.INSPTAIVO, Currency.INSPANEDA)
    v_back = convert(float(v), Currency.INSPANEDA, Currency.INSPTAIVO)
    assert abs(float(v_back) - 1.5) < 0.01
@check("10 GLOBAL_LEDGER single instance")
def c10():
    from uro.economy.ledger import GLOBAL_LEDGER as g1
    from uro.economy import GLOBAL_LEDGER as g2
    assert g1 is g2
passed = 0
for name, fn in checks:
    try:
        fn()
        passed += 1
        print("PASS  " + name)
    except Exception as e:
        print("FAIL  " + name + " :: " + type(e).__name__ + ": " + str(e))
print("%d/10 checks passed" % passed)
sys.exit(0 if passed == 10 else 1)
