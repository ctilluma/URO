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
# MODULE START : uro.interchange
# ---------------------------------------------------------------------
# FILE         : uro/interchange.py
# PURPOSE      : URO Code Interchange - binary and JSON serialization and
#                the canonical URO header.
# STANDARD     : URO-STD-0001 S4
# =====================================================================
"""Serialization/deserialization of UROs and the URO header."""

from __future__ import annotations

import base64 as _b64
import json as _json
import struct as _struct
from typing import Tuple

from uro.constants import HEADER_LEN_BYTES, HEADER_TOTAL_BYTES
from uro.core.urid import URID
from uro.core.uro import URO
from uro.exceptions import InterchangeError
from uro.security.hashing import blake2b_256

__all__ = ["build_header", "parse_header", "encode_uro", "decode_uro",
           "uro_to_json", "uro_from_json"]


def build_header(src_len: int, dst_len: int, payload_len: int,
                 future: int = 0) -> bytes:
    "PURPOSE: Delegate to the canonical RFC 7 header builder (single source)."
    from uro.core.header import build_header as _core
    return _core(src_len, dst_len, payload_len, future)


def parse_header(header: bytes) -> Tuple[int, int, int, int]:
    "PURPOSE: Delegate verification to the canonical RFC 7 header parser."
    from uro.core.header import parse_header as _core
    try:
        d = _core(header)
    except Exception as exc:
        raise InterchangeError(str(exc)) from exc
    return (d["src_len"], d["dst_len"], d["pay_len"], d["future"])


def encode_uro(uro: URO) -> bytes:
    """Serialize a URO to a canonical binary form."""
    payload_bytes = _json.dumps({"payload": uro.payload}).encode("utf-8")
    header = build_header(32, 32, len(payload_bytes))
    return header + uro.urid1.to_bytes() + uro.urid2.to_bytes() + payload_bytes


def decode_uro(data: bytes) -> URO:
    """Deserialize a URO from encode_uro output."""
    if len(data) < HEADER_TOTAL_BYTES + 64:
        raise InterchangeError("data too short")
    header = data[:HEADER_TOTAL_BYTES]
    _, _, payload_len = parse_header(header)[:3]
    offset = HEADER_TOTAL_BYTES
    urid1 = URID.from_bytes(data[offset:offset + 32]); offset += 32
    urid2 = URID.from_bytes(data[offset:offset + 32]); offset += 32
    payload_bytes = data[offset:offset + payload_len]
    payload = _json.loads(payload_bytes.decode("utf-8")).get("payload")
    return URO(urid1, urid2, payload)


def uro_to_json(uro: URO) -> str:
    """Serialize a URO to a JSON string."""
    doc = {
        "urid1": uro.urid1.to_hex(),
        "urid2": uro.urid2.to_hex(),
        "link": _b64.b64encode(uro.link()).decode("ascii"),
        "payload": uro.payload,
        "flags": {"structure": uro.is_structure, "group": uro.is_group,
                  "self": uro.is_self_reference},
    }
    return _json.dumps(doc, indent=2)


def uro_from_json(text: str) -> URO:
    """Deserialize a URO from uro_to_json output."""
    doc = _json.loads(text)
    return URO(URID.from_hex(doc["urid1"]), URID.from_hex(doc["urid2"]),
               doc.get("payload"))
# =====================================================================
# MODULE END   : uro.interchange
# =====================================================================
