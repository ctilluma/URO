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


"""Tests for symmetric encryption."""
import pytest

from uro import (encrypt, decrypt, double_encrypt, double_decrypt,
                 derive_key_from_password)
from uro.security.encryption import xor_bytes, split_1024_key
from uro.exceptions import EncryptionError


def test_xor_roundtrip():
    a = b"\x0f" * 16
    b = b"\xf0" * 16
    assert xor_bytes(xor_bytes(a, b), b) == a


def test_xor_length_guard():
    with pytest.raises(EncryptionError):
        xor_bytes(b"\x00", b"\x00\x00")


def test_derive_key_width():
    key = derive_key_from_password(b"pw", b"\x00" * 64)
    assert len(key) == 64


def test_split_1024_key():
    k = bytes(range(128))
    k1, k2 = split_1024_key(k)
    assert len(k1) == 64 and len(k2) == 64
    assert k1 + k2 == k


def test_split_key_length_guard():
    with pytest.raises(EncryptionError):
        split_1024_key(b"\x00" * 64)


def test_single_layer_roundtrip():
    key = b"k" * 64
    ct = encrypt(key, b"secret")
    assert ct != b"secret"
    assert decrypt(key, ct) == b"secret"


def test_double_layer_roundtrip():
    key = b"k" * 128
    ct = double_encrypt(key, b"the connection carries the value")
    assert double_decrypt(key, ct) == b"the connection carries the value"
