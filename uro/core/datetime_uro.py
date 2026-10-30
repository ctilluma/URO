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
# MODULE START : uro.core.datetime_uro
# ---------------------------------------------------------------------
# FILE         : uro/core/datetime_uro.py
# PURPOSE      : Time and Date UROs anchored to the InSPa epoch
#                14-MAY-1973 00:12:24 UTC, with RFC 6.4 conditions and
#                RFC 6.5 expiration semantics.
# STANDARD     : URO-STD-0001 S6
# =====================================================================
"Time and Date UROs anchored to the InSPa epoch (RFC 6)."

from __future__ import annotations

import datetime as _dt
import time as _time

from uro.constants import URO_EPOCH

__all__ = ["TimeURO", "DateURO"]


class TimeURO:
    "PURPOSE: Time as a URO wrapping a float seconds value (RFC 6.1)."

    def __init__(self, seconds: float) -> None:
        self.seconds = float(seconds)

    @classmethod
    def now(cls) -> "TimeURO":
        "PURPOSE: Current wall-clock time as a TimeURO."
        return cls(_time.time())

    def to_date_uro(self) -> "DateURO":
        "PURPOSE: Convert absolute seconds to epoch-relative DateURO (RFC 6.2)."
        return DateURO(self.seconds - URO_EPOCH.timestamp())

    def greater(self, other):
        "PURPOSE: RFC 6.4 condition: greater."
        return self.seconds > other.seconds

    def less(self, other):
        "PURPOSE: RFC 6.4 condition: less."
        return self.seconds < other.seconds

    def equal(self, other):
        "PURPOSE: RFC 6.4 condition: equal."
        return self.seconds == other.seconds

    def between(self, lo, hi):
        "PURPOSE: RFC 6.4 condition: between."
        return lo.seconds <= self.seconds <= hi.seconds

    def before(self, other):
        "PURPOSE: RFC 6.4 condition: before."
        return self.less(other)

    def after(self, other):
        "PURPOSE: RFC 6.4 condition: after."
        return self.greater(other)


class DateURO:
    "PURPOSE: Date as seconds before/after 14-MAY-1973 00:12:24 UTC (RFC 6.2)."

    def __init__(self, offset_seconds: float, expires_at: float = None,
                 renew: bool = False) -> None:
        self.offset_seconds = float(offset_seconds)
        self.expires_at = expires_at
        self.renew = bool(renew)

    @classmethod
    def from_datetime(cls, value: _dt.datetime) -> "DateURO":
        "PURPOSE: Build a DateURO from an aware or naive-UTC datetime."
        if value.tzinfo is None:
            value = value.replace(tzinfo=_dt.timezone.utc)
        return cls(value.timestamp() - URO_EPOCH.timestamp())

    def to_datetime(self) -> _dt.datetime:
        "PURPOSE: Render the offset back as an aware UTC datetime."
        return _dt.datetime.fromtimestamp(
            URO_EPOCH.timestamp() + self.offset_seconds, tz=_dt.timezone.utc)

    def expiration_action(self, now_seconds: float = None) -> str:
        "PURPOSE: RFC 6.5: renew when flagged, else delete (temp objects)."
        if self.expires_at is None:
            return "none"
        now = _time.time() if now_seconds is None else now_seconds
        if now < self.expires_at:
            return "none"
        return "renew" if self.renew else "delete"
# =====================================================================
# MODULE END   : uro.core.datetime_uro
# =====================================================================
