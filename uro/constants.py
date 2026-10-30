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
# MODULE START : uro.constants
# ---------------------------------------------------------------------
# FILE         : uro/constants.py
# PURPOSE      : Universal constants, the InSPa epoch, bit/byte widths,
#                and the canonical special URID/URO sentinel values.
# STANDARD     : URO-STD-0001 S3, S4, S7
# =====================================================================
"""Global constants for the URO reference implementation."""

from __future__ import annotations

import datetime as _dt

# Bit / byte geometry.
UUID_BITS: int = 128
UUID_BYTES: int = UUID_BITS // 8
URID_BITS: int = 256
URID_BYTES: int = URID_BITS // 8
URO_BITS: int = 512
URO_BYTES: int = URO_BITS // 8
LINK_BITS: int = 512
LINK_BYTES: int = LINK_BITS // 8

# Header geometry.
HEADER_FIELD_BITS: int = 64
HEADER_LENGTH_FIELDS: int = 4
HEADER_LEN_BYTES: int = (HEADER_FIELD_BITS // 8) * HEADER_LENGTH_FIELDS
HEADER_CHECKSUM_BYTES: int = 32
HEADER_TOTAL_BYTES: int = HEADER_LEN_BYTES + HEADER_CHECKSUM_BYTES

# The InSPa epoch: 14-MAY-1973 00:12:24 (UTC).
URO_EPOCH: _dt.datetime = _dt.datetime(
    1973, 5, 14, 0, 12, 24, tzinfo=_dt.timezone.utc
)

# Canonical URID integer sentinels.
URID_INT_ZERO: int = 0
URID_INT_ONES: int = (1 << URID_BITS) - 1
UUID_INT_ZERO: int = 0
UUID_INT_ONES: int = (1 << UUID_BITS) - 1

# Cryptographic widths.
SHA512_BYTES: int = 64
KEY_1024_BITS: int = 1024
KEY_1024_BYTES: int = KEY_1024_BITS // 8
HASH_1024_BYTES: int = 128
HASH_BITS: int = 1024

# Routing URO widths (RFC 1.2).
SOURCE_URO_BITS: int = 512
DEST_URO_BITS: int = 512
REQ_URO_BITS: int = 512
RESP_URO_BITS: int = 512
AAA_URO_BITS: int = 512
TRUST_URO_BITS: int = 512
NTE_RECEPTOR_BITS: int = 512
NTE_STATE_BITS: int = 1536  # 24 axes * 64-bit float

# Economics.
INSPANEDA_PER_INSPATIVO: int = 1000
TRANSACTION_FEE_PERCENT: int = 10
# =====================================================================
# MODULE END   : uro.constants
# =====================================================================
