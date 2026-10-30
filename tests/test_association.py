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


"""Tests for Association relationship UROs."""
from uro import URO, Association, ConnectionType


def test_association_registers_on_endpoints():
    a, b = URO.new(), URO.new()
    rel = Association(a, b)
    assert rel in a.associations
    assert rel in b.associations


def test_connection_type():
    a, b = URO.new(), URO.new()
    rel = Association(a, b, ConnectionType.CHILD)
    assert rel.connection_type is ConnectionType.CHILD


def test_use_increases_bond():
    a, b = URO.new(), URO.new()
    rel = Association(a, b)
    before = rel.bond
    rel.use()
    assert rel.bond > before


def test_reward_punish_clamped():
    a, b = URO.new(), URO.new()
    rel = Association(a, b)
    for _ in range(20):
        rel.reward(0.5)
    assert rel.trust == 1.0
    for _ in range(40):
        rel.punish(0.5)
    assert rel.trust == 0.0


def test_decay_reduces_bond():
    a, b = URO.new(), URO.new()
    rel = Association(a, b)
    before = rel.bond
    rel.decay(100.0)
    assert rel.bond < before
