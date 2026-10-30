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
# MODULE START : uro.core.header
# ---------------------------------------------------------------------
# FILE         : uro/core/header.py
# PURPOSE      : URO header format per RFC 7: four 64-bit length fields
#                plus a Blake2-256 integrity checksum over their
#                concatenation (S-Len + D-Len + P-Len + Fut).
# STANDARD     : URO-STD-0001 S7
# =====================================================================
"URO header construction and integrity verification (RFC 7)."

from __future__ import annotations

import hashlib
import struct

from uro.constants import (
    HEADER_FIELD_BITS,
    HEADER_LENGTH_FIELDS,
    HEADER_LEN_BYTES,
    HEADER_CHECKSUM_BYTES,
    HEADER_TOTAL_BYTES,
)
from uro.exceptions import HeaderIntegrityError, UROStructureError

__all__ = ["build_header", "parse_header", "verify_header"]

_FMT = ">" + "Q" * HEADER_LENGTH_FIELDS


def _checksum(length_block: bytes) -> bytes:
    "PURPOSE: Blake2-256 digest over the 32-byte length block (RFC 7.2)."
    return hashlib.blake2b(length_block, digest_size=HEADER_CHECKSUM_BYTES).digest()


def build_header(src_len: int, dst_len: int, pay_len: int, future: int = 0) -> bytes:
    "PURPOSE: Pack the four 64-bit length fields and append their Blake2-256."
    for name, value in (("src_len", src_len), ("dst_len", dst_len),
                        ("pay_len", pay_len), ("future", future)):
        if not 0 <= value < (1 << HEADER_FIELD_BITS):
            raise UROStructureError("header field out of 64-bit range: " + name)
    length_block = struct.pack(_FMT, src_len, dst_len, pay_len, future)
    return length_block + _checksum(length_block)


def parse_header(blob: bytes) -> dict:
    "PURPOSE: Unpack and integrity-check a header blob; raise on mismatch."
    if len(blob) != HEADER_TOTAL_BYTES:
        raise UROStructureError("header must be 64 bytes")
    length_block = blob[:HEADER_LEN_BYTES]
    digest = blob[HEADER_LEN_BYTES:]
    if _checksum(length_block) != digest:
        raise HeaderIntegrityError("Blake2-256 header checksum mismatch")
    src_len, dst_len, pay_len, future = struct.unpack(_FMT, length_block)
    return {"src_len": src_len, "dst_len": dst_len,
            "pay_len": pay_len, "future": future}


def verify_header(blob: bytes) -> bool:
    "PURPOSE: Boolean header integrity probe (non-raising)."
    try:
        parse_header(blob)
        return True
    except Exception:
        return False
# =====================================================================
# MODULE END   : uro.core.header
# =====================================================================
