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


"""Tests for path resolution."""
from uro import URO, Association, resolve_path


def test_self_path():
    a = URO.new()
    p = resolve_path(a, a)
    assert p is not None and len(p) == 1


def test_chain_path():
    a, b, c = URO.new(), URO.new(), URO.new()
    Association(a, b)
    Association(b, c)
    p = resolve_path(a, c)
    assert p is not None
    assert p.hops[0] is a and p.hops[-1] is c
    assert len(p) == 3


def test_no_path_returns_none():
    a, z = URO.new(), URO.new()
    assert resolve_path(a, z) is None
