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


"""Tests for URO serialization and the header."""
import pytest

from uro import (URO, build_header, parse_header, encode_uro, decode_uro,
                 uro_to_json, uro_from_json)
from uro.exceptions import InterchangeError


def test_header_roundtrip():
    h = build_header(32, 32, 10, 0)
    assert parse_header(h) == (32, 32, 10, 0)


def test_header_checksum_guard():
    h = bytearray(build_header(32, 32, 10, 0))
    h[0] ^= 0xFF
    with pytest.raises(InterchangeError):
        parse_header(bytes(h))


def test_binary_roundtrip():
    u = URO.new(payload={"hello": "world"})
    assert decode_uro(encode_uro(u)) == u


def test_json_roundtrip():
    u = URO.new(payload={"n": 1})
    v = uro_from_json(uro_to_json(u))
    assert v == u
    assert v.payload == {"n": 1}
