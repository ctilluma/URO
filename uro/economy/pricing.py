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
MODULE: Value-Based Pricing
INTENT: Price economic goods from trust, myelination, usage, and quadrant.
STANDARD: URO-STD-0001 S34
"""
from __future__ import annotations

__all__ = ["QUADRANT_BASE_PRICE", "price_good"]

QUADRANT_BASE_PRICE = {
    "Base": 1.0,
    "Gap Remediation": 5.0,
    "Best Practice": 10.0,
    "World First": 100.0,
}


def price_good(good, trust: float = 50.0, myelination: int = 0,
               usage: int = 0) -> float:
    """
    Compute a value-based price for a good.

    price = quadrant_base
            * trust_factor        (higher trust = more valuable)
            * myelination_factor  (hot/proven paths = more valuable)
            * usage_factor        (proven by use = more valuable)
    """
    base = QUADRANT_BASE_PRICE.get(good.quadrant, 1.0)
    trust_factor = 0.5 + (trust / 100.0)          # 0.5 .. 1.5
    myelin_factor = 1.0 + (myelination * 0.5)     # 1.0 .. 3.0
    usage_factor = 1.0 + min(usage, 1000) / 500.0  # 1.0 .. 3.0
    price = base * trust_factor * myelin_factor * usage_factor
    good.price = round(price, 4)
    return good.price
