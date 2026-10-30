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


"""Tests for URID identity and conversions."""
import pytest

from uro import URID
from uro.constants import URID_BYTES, URID_INT_ONES
from uro.exceptions import URIDError


def test_new_urid_unique():
    a, b = URID.new(), URID.new()
    assert a != b


def test_int_roundtrip():
    u = URID.new()
    assert URID.from_int(u.to_int()) == u


def test_bytes_roundtrip_and_width():
    u = URID.new()
    b = u.to_bytes()
    assert len(b) == URID_BYTES
    assert URID.from_bytes(b) == u


def test_hex_roundtrip():
    u = URID.new()
    assert URID.from_hex(u.to_hex()) == u


def test_zero_and_ones_sentinels():
    assert URID.zero().is_zero()
    assert not URID.zero().is_ones()
    assert URID.ones().is_ones()
    assert URID.ones().to_int() == URID_INT_ONES


def test_xor():
    a, b = URID.new(), URID.new()
    x = a ^ b
    assert (a.to_int() ^ b.to_int()) == x.to_int()


def test_hashable_and_eq():
    u = URID.new()
    s = {u, URID.from_int(u.to_int())}
    assert len(s) == 1


def test_from_int_range_guard():
    with pytest.raises(URIDError):
        URID.from_int(1 << 300)


def test_from_bytes_length_guard():
    with pytest.raises(URIDError):
        URID.from_bytes(b"\x00" * 5)


def test_uuid_halves():
    u = URID.new()
    assert u.uuid1.int == (u.to_int() >> 128)
    assert u.uuid2.int == (u.to_int() & ((1 << 128) - 1))
