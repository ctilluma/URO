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


"""Tests for the adaptive OPAR scheduler."""
import asyncio

import pytest

from uro import URO, AdaptiveScheduler
from uro.exceptions import SchedulerError


def test_register_and_entry():
    s = AdaptiveScheduler()
    u = URO.new()
    s.register(u)
    assert s.entry(u).uro is u


def test_duplicate_registration_raises():
    s = AdaptiveScheduler()
    u = URO.new()
    s.register(u)
    with pytest.raises(SchedulerError):
        s.register(u)


def test_run_executes_iterations():
    s = AdaptiveScheduler()
    u = URO.new()
    s.register(u, base_interval=0.001)
    result = asyncio.run(s.run(steps=3))
    assert result[id(u)] == 3


def test_adaptive_interval_shrinks_with_queue():
    s = AdaptiveScheduler()
    u = URO.new()
    s.register(u, base_interval=1.0)
    entry = s.entry(u)
    idle = s.adaptive_interval(entry)
    for i in range(10):
        s.feed(u, i)
    busy = s.adaptive_interval(entry)
    assert busy < idle


def test_one_off_not_run_by_default():
    s = AdaptiveScheduler()
    always = URO.new()
    oneoff = URO.new()
    s.register(always, base_interval=0.001, always_on=True)
    s.register(oneoff, base_interval=0.001, always_on=False)
    result = asyncio.run(s.run(steps=2))
    assert id(always) in result
    assert id(oneoff) not in result
