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


"""Tests for ACL combinators."""
from uro import ACL, ACLEntry, ACLCombinator


def test_default_deny():
    acl = ACL()
    assert acl.evaluate("alice", "read") is False


def test_and_requires_all_allow():
    acl = ACL(ACLCombinator.AND)
    acl.add(ACLEntry("alice", "read", True))
    acl.add(ACLEntry("alice", "read", True))
    assert acl.evaluate("alice", "read") is True
    acl.add(ACLEntry("alice", "read", False))
    assert acl.evaluate("alice", "read") is False


def test_or_allows_any():
    acl = ACL(ACLCombinator.OR)
    acl.add(ACLEntry("alice", "read", False))
    acl.add(ACLEntry("alice", "read", True))
    assert acl.evaluate("alice", "read") is True


def test_nand():
    acl = ACL(ACLCombinator.NAND)
    acl.add(ACLEntry("alice", "read", True))
    acl.add(ACLEntry("alice", "read", True))
    assert acl.evaluate("alice", "read") is False


def test_nor():
    acl = ACL(ACLCombinator.NOR)
    acl.add(ACLEntry("alice", "read", False))
    assert acl.evaluate("alice", "read") is True
