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


"""Tests for multi-standard hashing."""
from uro import inahash, sha512, sha512x3, blake2b_256
from uro.security.hashing import sha128, sha3_1024, blake3_1024


def test_inahash_width():
    assert len(inahash(b"message")) == 128


def test_inahash_deterministic():
    assert inahash(b"x") == inahash(b"x")


def test_sha512x3_deterministic():
    assert sha512x3(b"pw") == sha512x3(b"pw")
    assert len(sha512x3(b"pw")) == 64


def test_blake2b_256_width():
    assert len(blake2b_256(b"data")) == 32


def test_sha128_width():
    assert len(sha128(b"data")) == 16


def test_sha3_1024_width():
    assert len(sha3_1024(b"data")) == 128


def test_blake3_1024_width():
    assert len(blake3_1024(b"data")) == 128


def test_distinct_inputs_distinct_hashes():
    assert inahash(b"a") != inahash(b"b")
