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
# MODULE START : uro.economy.social_pricing
# ---------------------------------------------------------------------
# FILE         : uro/economy/social_pricing.py
# PURPOSE      : Social pricing: trust-weighted price adjustments and
#                reputation-based discounts (RFC 111).
# STANDARD     : URO-STD-0001 S35
# =====================================================================
"Social pricing with trust weighting (RFC 111)."

from __future__ import annotations

__all__ = ["social_price", "TRUST_DISCOUNT_FACTOR"]

TRUST_DISCOUNT_FACTOR = 0.01


def social_price(base_price: float, trust: float, reputation: float = 50.0) -> float:
    "PURPOSE: Apply trust and reputation discounts to base price."
    trust_discount = trust * TRUST_DISCOUNT_FACTOR
    rep_discount = reputation * TRUST_DISCOUNT_FACTOR * 0.5
    total_discount = min(0.5, trust_discount + rep_discount)
    return base_price * (1.0 - total_discount)
# =====================================================================
# MODULE END   : uro.economy.social_pricing
# =====================================================================
