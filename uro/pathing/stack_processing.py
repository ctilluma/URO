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
# MODULE START : uro.pathing.stack_processing
# ---------------------------------------------------------------------
# FILE         : uro/pathing/stack_processing.py
# PURPOSE      : Stack-based order of processing (RFC 77): top processing,
#                pop-as-far-as forwarding, bottom insertion of new results.
# STANDARD     : URO-STD-0001 S9
# =====================================================================
"Stack-based order of processing (RFC 77)."

from __future__ import annotations

from typing import Any, Callable, List

__all__ = ["ProcessingStack"]


class ProcessingStack:
    "PURPOSE: Stack semantics per RFC 77.1-77.3."

    def __init__(self) -> None:
        self.items: List[Any] = []

    def push(self, item: Any) -> None:
        "PURPOSE: Add an item to the top of the stack."
        self.items.append(item)

    def add_result_item(self, item: Any) -> None:
        "PURPOSE: RFC 77.3: a third item with new result goes to the bottom."
        if len(self.items) >= 2:
            self.items.insert(0, item)
        else:
            self.items.append(item)

    def process_top(self, handler: Callable[[Any], Any]) -> Any:
        "PURPOSE: RFC 77.1: process when the object can get to top of stack."
        if not self.items:
            return None
        return handler(self.items[-1])

    def pop_as_far_as(self, can_reach: Callable[[Any], bool]) -> List[Any]:
        "PURPOSE: RFC 77.2: pop from top while reachable; return popped for forwarding."
        popped: List[Any] = []
        while self.items and can_reach(self.items[-1]):
            popped.append(self.items.pop())
        return popped
# =====================================================================
# MODULE END   : uro.pathing.stack_processing
# =====================================================================
