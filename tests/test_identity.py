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


"""Tests for identity verification and tokens."""
import pytest

from uro import Identity
from uro.exceptions import IdentityError


def test_verify_correct_password():
    i = Identity("subject", b"pw")
    assert i.verify_password(b"pw")


def test_reject_wrong_password():
    i = Identity("subject", b"pw")
    assert not i.verify_password(b"bad")


def test_token_lifecycle():
    i = Identity("subject", b"pw")
    tok = i.issue_token()
    assert i.validate_token(tok.token)
    i.revoke_token(tok.token)
    assert not i.validate_token(tok.token)


def test_revoke_unknown_raises():
    i = Identity("subject", b"pw")
    with pytest.raises(IdentityError):
        i.revoke_token("nope")
