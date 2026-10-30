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
# MODULE START : uro.learning.aloneness
# ---------------------------------------------------------------------
# FILE         : uro/learning/aloneness.py
# PURPOSE      : Aloneness as propagator: an object with little input
#                searches out capabilities, altruism or self-improvement
#                (RFC 98).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"Aloneness as propagator for action (RFC 98)."

from __future__ import annotations

from typing import Any, Dict

__all__ = ["AlonenessPropagator"]


class AlonenessPropagator:
    "PURPOSE: Little input propagates seeking of capabilities (RFC 98)."

    def __init__(self, input_threshold: int = 1) -> None:
        self.input_threshold = input_threshold
        self._recent = 0

    def observe_input(self, count: int = 1) -> None:
        "PURPOSE: Count incoming stimuli this window."
        self._recent += count

    def reset_window(self) -> None:
        "PURPOSE: Begin a new observation window."
        self._recent = 0

    def should_seek(self) -> bool:
        "PURPOSE: True when input falls below the aloneness threshold."
        return self._recent < self.input_threshold

    def seek_action(self, mode: str = "self_improvement") -> Dict[str, Any]:
        "PURPOSE: Emit the propagator action object (RFC 98)."
        return {"aloneness_override": True, "goal": mode}
# =====================================================================
# MODULE END   : uro.learning.aloneness
# =====================================================================
