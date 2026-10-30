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
# MODULE START : uro.priority
# ---------------------------------------------------------------------
# FILE         : uro/priority.py
# PURPOSE      : Priority processing: crit/high/normal/low queue precedence
#                and unprocessed-data retention times (RFC 87).
# STANDARD     : URO-STD-0001 S-URO Interchange
# =====================================================================
"Priority processing: retention and queue precedence (RFC 87)."

from __future__ import annotations

from typing import Any, Dict, List

__all__ = ["PRIORITY_LEVELS", "RETENTION_SECONDS", "PriorityQueue"]

PRIORITY_LEVELS = ("crit", "high", "normal", "low")

# RFC 87: priority determines how long unprocessed data is stored.
RETENTION_SECONDS: Dict[str, float] = {
    "crit": 86400.0,
    "high": 21600.0,
    "normal": 3600.0,
    "low": 300.0,
}


class PriorityQueue:
    "PURPOSE: Queue precedence crit > high > normal > low (RFC 87)."

    def __init__(self) -> None:
        self._queues: Dict[str, List[Any]] = {lvl: [] for lvl in PRIORITY_LEVELS}

    def push(self, level: str, item: Any) -> None:
        "PURPOSE: Enqueue an item at its priority level."
        if level not in self._queues:
            raise KeyError("unknown priority level: " + str(level))
        self._queues[level].append(item)

    def pop(self) -> Any:
        "PURPOSE: Dequeue by precedence order."
        for level in PRIORITY_LEVELS:
            if self._queues[level]:
                return self._queues[level].pop(0)
        return None

    def retention(self, level: str) -> float:
        "PURPOSE: How long unprocessed data is stored per level (RFC 87)."
        return RETENTION_SECONDS[level]
# =====================================================================
# MODULE END   : uro.priority
# =====================================================================
