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


# =====================================================================
# MODULE START : uro.time_uro
# ---------------------------------------------------------------------
# FILE         : uro/time_uro.py
# PURPOSE      : Time and Date UROs anchored to the InSPa epoch.
# STANDARD     : URO-STD-0001 S7
# =====================================================================
"""Time and Date UROs anchored to the InSPa epoch."""

from __future__ import annotations

import datetime as _dt

from uro.constants import URO_EPOCH
from uro.core.uro import URO
from uro.core.urid import URID

__all__ = ["TimeURO", "DateURO", "now_date_uro"]


class TimeURO(URO):
    """A URO representing a duration/instant as float seconds."""

    def __init__(self, seconds: float) -> None:
        """Create a Time URO."""
        _identity = URID.new()
        super().__init__(_identity, _identity, float(seconds))
    @property
    def seconds(self) -> float:
        """The time value in seconds."""
        return float(self.payload)

    def __repr__(self) -> str:
        return f"TimeURO({self.seconds}s)"


class DateURO(TimeURO):
    """A Time URO counting signed seconds from the InSPa epoch."""

    def __init__(self, seconds_from_epoch: float) -> None:
        """Create a Date URO from an epoch-relative second count."""
        super().__init__(seconds_from_epoch)

    @classmethod
    def from_datetime(cls, when: _dt.datetime) -> "DateURO":
        """Create a Date URO from an aware datetime."""
        delta = when - URO_EPOCH
        return cls(delta.total_seconds())

    def to_datetime(self) -> _dt.datetime:
        """Convert back to an aware datetime."""
        return URO_EPOCH + _dt.timedelta(seconds=self.seconds)

    def __repr__(self) -> str:
        return f"DateURO({self.to_datetime().isoformat()})"


def now_date_uro() -> DateURO:
    """Return a Date URO for the current instant."""
    return DateURO.from_datetime(_dt.datetime.now(_dt.timezone.utc))
# =====================================================================
# MODULE END   : uro.time_uro
# =====================================================================
