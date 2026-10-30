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


"""Tests for the OPAR lifecycle."""
from uro import URO, OPARCycle, OPARPhase


def test_full_cycle_history():
    c = OPARCycle(URO.new())
    c.run(1)
    assert c.history == [OPARPhase.OBSERVE, OPARPhase.PLAN,
                         OPARPhase.ACT, OPARPhase.REVIEW]


def test_enqueue_is_observed():
    c = OPARCycle(URO.new())
    c.enqueue({"event": "hello"})
    summaries = c.run(1)
    assert summaries[0]["processed"] >= 1


def test_multiple_iterations():
    c = OPARCycle(URO.new())
    summaries = c.run(3)
    assert len(summaries) == 3


def test_self_check_included():
    c = OPARCycle(URO.new())
    obs = c.observe()
    assert any("self" in o for o in obs if isinstance(o, dict))
