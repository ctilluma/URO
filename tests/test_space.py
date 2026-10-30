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


"""Tests for UROSpace registry and relationship indexing."""
import pytest

from uro import URO, UROSpace, Association, ConnectionType
from uro.exceptions import UROStructureError


def test_register_and_get():
    space = UROSpace()
    u = URO.new()
    space.register(u)
    assert space.get(u.urid1, u.urid2) is u


def test_duplicate_registration_raises():
    space = UROSpace()
    u = URO.new()
    space.register(u)
    with pytest.raises(UROStructureError):
        space.register(u)


def test_register_relationship_and_lookup():
    space = UROSpace()
    a, b = URO.new(), URO.new()
    rel = Association(a, b, ConnectionType.LINK)
    space.register(a); space.register(b)
    space.register_relationship(rel)
    assert space.relationship(rel.link()) is rel


def test_neighbors():
    space = UROSpace()
    a, b = URO.new(), URO.new()
    Association(a, b)
    assert b in space.neighbors(a)
    assert a in space.neighbors(b)


def test_len_counts_objects_and_relationships():
    space = UROSpace()
    a, b = URO.new(), URO.new()
    rel = Association(a, b)
    space.register(a); space.register(b)
    space.register_relationship(rel)
    assert len(space) == 3
