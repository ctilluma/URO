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
# MODULE START : uro.economy.currency
# ---------------------------------------------------------------------
# FILE         : uro/economy/currency.py
# PURPOSE      : Currency definitions with decimal precision enforcement:
#                InSPativo (2 dp), InSPaneda (4 dp), 1:1000 ratio
#                (RFC 110).
# STANDARD     : URO-STD-0001 S35
# =====================================================================
"Currency definitions and conversions (RFC 110)."

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from enum import Enum

__all__ = ["Currency", "convert", "INSPTAIVO_TO_INSPANEDA_RATIO"]

INSPTAIVO_TO_INSPANEDA_RATIO = 1000


class Currency(str, Enum):
    "PURPOSE: The two canonical currencies (RFC 110)."
    INSPTAIVO = "insptaivo"
    INSPANEDA = "inspaneda"


def _round_to_dp(value: float, dp: int) -> Decimal:
    "PURPOSE: Round to the specified decimal places using ROUND_HALF_UP."
    quant = Decimal("1." + "0" * dp) if dp > 0 else Decimal("1")
    return Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP)


def convert(value: float, from_currency: Currency, to_currency: Currency) -> Decimal:
    "PURPOSE: Convert between InSPativo and InSPaneda with decimal precision."
    if from_currency == to_currency:
        dp = 2 if from_currency == Currency.INSPTAIVO else 4
        return _round_to_dp(value, dp)
    if from_currency == Currency.INSPTAIVO and to_currency == Currency.INSPANEDA:
        raw = Decimal(str(value)) * INSPTAIVO_TO_INSPANEDA_RATIO
        return _round_to_dp(float(raw), 4)
    raw = Decimal(str(value)) / INSPTAIVO_TO_INSPANEDA_RATIO
    return _round_to_dp(float(raw), 2)
# =====================================================================
# MODULE END   : uro.economy.currency
# =====================================================================
