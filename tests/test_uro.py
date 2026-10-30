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


"""Tests for the core URO object and its special cases."""
import pytest

from uro import URO, URID
from uro.constants import LINK_BYTES
from uro.exceptions import UROStructureError


def test_new_is_self_reference():
    u = URO.new()
    assert u.is_self_reference
    assert u.urid1 == u.urid2


def test_nothing():
    n = URO.nothing()
    assert n.is_structure
    assert n.is_self_reference


def test_everything():
    e = URO.everything()
    assert e.is_group
    assert e.is_self_reference


def test_structure_template():
    base = URID.new()
    t = URO(base, URID.zero())
    assert t.is_structure
    assert not t.is_group


def test_group_reference():
    base = URID.new()
    g = URO(base, URID.ones())
    assert g.is_group
    assert not g.is_structure


def test_link_width_and_determinism():
    u = URO.new()
    assert len(u.link()) == LINK_BYTES
    assert u.link() == u.link()


def test_add_and_get_child():
    parent, child = URO.new(), URO.new()
    parent.add_child(child)
    assert parent.get_child(child.urid2) is child
    assert child.parent is parent


def test_duplicate_child_raises():
    parent, child = URO.new(), URO.new()
    parent.add_child(child)
    with pytest.raises(UROStructureError):
        parent.add_child(child)


def test_equality_and_hash():
    u = URO.new()
    v = URO(u.urid1, u.urid2)
    assert u == v
    assert hash(u) == hash(v)
