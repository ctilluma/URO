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


"""Tests for the canonical taxonomy."""
from uro import build_taxonomy, WELL_KNOWN_TYPES


def test_taxonomy_includes_meta_poles():
    space = build_taxonomy()
    assert len(space) >= len(WELL_KNOWN_TYPES) + 2


def test_well_known_types_present():
    assert "PKI.PUBK" in WELL_KNOWN_TYPES
    assert "CONN.DBSE" in WELL_KNOWN_TYPES
    assert "PAY.INSPANEDA" in WELL_KNOWN_TYPES
    assert "AUPI.TRANSLATOR" in WELL_KNOWN_TYPES
    assert "META.NOTHING" in WELL_KNOWN_TYPES
