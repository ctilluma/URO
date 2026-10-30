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


"""Tests for Policy UROs."""
from uro import PolicyURO, ACL, ACLEntry, ACLCombinator


def test_policy_scopes():
    p = PolicyURO("device-sync")
    folders = ACL(ACLCombinator.AND).add(ACLEntry("tablet", "sync", True))
    p.add_acl("folders", folders)
    assert "folders" in p.scopes()


def test_policy_allows_matching_scope():
    p = PolicyURO("device-sync")
    p.add_acl("contacts", ACL().add(ACLEntry("phone", "read", True)))
    assert p.evaluate("contacts", "phone", "read") is True


def test_policy_denies_unknown_scope():
    p = PolicyURO("device-sync")
    assert p.evaluate("missing", "phone", "read") is False


def test_group_override_via_combinator():
    p = PolicyURO("device-sync")
    acl = ACL(ACLCombinator.OR)
    acl.add(ACLEntry("groupA", "overwrite", True))
    acl.add(ACLEntry("groupA", "overwrite", False))
    p.add_acl("contacts", acl)
    assert p.evaluate("contacts", "groupA", "overwrite") is True
