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


"""Tests for PKI UROs and signatures."""
from uro import URO, PublicKeyURO, sign_uro, verify_signature


def test_public_key_lifecycle():
    pk = PublicKeyURO(b"pubkey")
    assert pk.is_valid()
    pk.revoke()
    assert not pk.is_valid()


def test_signature_roundtrip():
    obj, signer, owner = URO.new(), URO.new(), URO.new()
    priv = b"private-key"
    sig = sign_uro(obj, signer, owner, priv)
    assert verify_signature(sig, priv)


def test_signature_tamper_detection():
    obj, signer, owner = URO.new(), URO.new(), URO.new()
    priv = b"private-key"
    sig = sign_uro(obj, signer, owner, priv)
    assert not verify_signature(sig, b"wrong-key")
