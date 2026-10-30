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
# MODULE START : uro.learning.attention
# ---------------------------------------------------------------------
# FILE         : uro/learning/attention.py
# PURPOSE      : Attention and daydream: prioritize or deprioritize input
#                streams to provide overrides on input (RFC 93).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"Attention and daydream input-stream overrides (RFC 93)."

from __future__ import annotations

from typing import Dict, List

__all__ = ["AttentionManager", "INTERNAL_STREAM"]

INTERNAL_STREAM = "internal"


class AttentionManager:
    "PURPOSE: Stream prioritization with forced overrides and daydream."

    def __init__(self, streams: List[str]) -> None:
        self._priority: Dict[str, float] = {s: 0.0 for s in streams}
        self._override = None

    def prioritize(self, stream: str, delta: float = 1.0) -> None:
        "PURPOSE: Raise a stream priority (RFC 93 override)."
        self._priority[stream] = self._priority.get(stream, 0.0) + delta

    def deprioritize(self, stream: str, delta: float = 1.0) -> None:
        "PURPOSE: Lower a stream priority (RFC 93 override)."
        self._priority[stream] = self._priority.get(stream, 0.0) - delta

    def override(self, stream: str) -> None:
        "PURPOSE: Force a stream to the top regardless of priority."
        self._override = stream

    def clear_override(self) -> None:
        "PURPOSE: Remove the forced stream override."
        self._override = None

    def active_order(self) -> List[str]:
        "PURPOSE: Effective stream order honoring override then priority."
        order = sorted(self._priority, key=lambda s: -self._priority[s])
        if self._override is not None and self._override in self._priority:
            order.remove(self._override)
            order.insert(0, self._override)
        return order

    def daydream(self, enabled: bool = True) -> bool:
        "PURPOSE: Daydream routes attention to the internal stream (RFC 93)."
        if enabled:
            self._priority.setdefault(INTERNAL_STREAM, 0.0)
            self.override(INTERNAL_STREAM)
        elif self._override == INTERNAL_STREAM:
            self.clear_override()
        return bool(enabled)
# =====================================================================
# MODULE END   : uro.learning.attention
# =====================================================================
