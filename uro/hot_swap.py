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
# MODULE START : uro.hot_swap
# ---------------------------------------------------------------------
# FILE         : uro/hot_swap.py
# PURPOSE      : URO code interchange: supplant code while maintaining
#                identity (RFC 85). URID1 preserved, URID2 may change,
#                associations and connections carried over.
# STANDARD     : URO-STD-0001 S-URO Interchange
# =====================================================================
"Hot-swap process preserving identity (RFC 85)."

from __future__ import annotations

from typing import Any, Callable, List

from uro.core.uro import URO

__all__ = ["HotSwapRecord", "hot_swap"]


class HotSwapRecord:
    "PURPOSE: Typed result of one hot-swap operation (RFC 85)."

    def __init__(self, urid1, old_urid2, new_urid2, carried: List[Any]) -> None:
        self.urid1 = urid1
        self.old_urid2 = old_urid2
        self.new_urid2 = new_urid2
        self.carried_associations = carried


def hot_swap(old: URO, new_code_factory: Callable[[], URO],
             verify: Callable[[URO], bool] = None) -> HotSwapRecord:
    "PURPOSE: Generate+verify, compile+test, identify old, swap preserving URID1."
    candidate = new_code_factory()
    if verify is not None and not verify(candidate):
        raise ValueError("candidate failed verification")
    candidate.urid1 = old.urid1
    carried = list(getattr(old, "associations", []))
    for assoc in carried:
        candidate.associate(assoc)
    return HotSwapRecord(old.urid1, old.urid2, candidate.urid2, carried)
# =====================================================================
# MODULE END   : uro.hot_swap
# =====================================================================
