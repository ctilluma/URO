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


"""Tests for neurotransmitter equivalences."""
from uro import NTE, NTEState, Receptor, Synapse


def test_nte_state_set_get():
    s = NTEState()
    s.set(NTE.DOPAMINE, 0.7)
    assert s.get(NTE.DOPAMINE) == 0.7


def test_receptor_ratio_range():
    r = Receptor(receptor_count=10, potentiators=8, antagonists=2)
    assert 0.0 <= r.activity_ratio() <= 1.0


def test_receptor_empty_is_zero():
    r = Receptor(receptor_count=10)
    assert r.activity_ratio() == 0.0


def test_synapse_fire_returns_bool():
    r = Receptor(receptor_count=10, potentiators=10, antagonists=0)
    s = Synapse(r)
    assert isinstance(s.fire(), bool)


def test_gaba_inhibition_suppresses():
    state = NTEState()
    state.set(NTE.GABA, 1.0)
    r = Receptor(receptor_count=10, potentiators=10)
    s = Synapse(r, state)
    fires = sum(s.fire() for _ in range(50))
    assert fires == 0
