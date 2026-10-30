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


"""Tests for Time and Date UROs."""
import datetime as dt

from uro import DateURO, TimeURO, now_date_uro
from uro.constants import URO_EPOCH


def test_epoch_is_1973():
    assert URO_EPOCH.year == 1973
    assert URO_EPOCH.month == 5
    assert URO_EPOCH.day == 14


def test_time_uro_seconds():
    t = TimeURO(3.5)
    assert t.seconds == 3.5


def test_date_roundtrip():
    when = dt.datetime(2020, 1, 1, tzinfo=dt.timezone.utc)
    d = DateURO.from_datetime(when)
    assert d.to_datetime() == when


def test_now_is_after_epoch():
    assert now_date_uro().seconds > 0


def test_before_epoch_is_negative():
    when = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    assert DateURO.from_datetime(when).seconds < 0
