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
# MODULE START : uro.boot.child_boot
# ---------------------------------------------------------------------
# FILE         : uro/boot/child_boot.py
# PURPOSE      : Child boot: parent-provided boot URO, queued responses
#                until parent ACK, child INAHASH verification (RFC 108).
# STANDARD     : URO-STD-0001 S12
# =====================================================================
"Child boot with response queues and parent ACK (RFC 108)."

from __future__ import annotations

from typing import Any, Dict, List

__all__ = ["ChildBoot"]


class ChildBoot:
    "PURPOSE: Model a child URO booting under a parent seal."

    def __init__(self, parent_seal: str, child: Any) -> None:
        self.parent_seal = parent_seal
        self.child = child
        self._queue: List[Any] = []

    def queue_response(self, response: Any) -> None:
        "PURPOSE: Child queues responses until the parent ACKs."
        self._queue.append(response)

    def drain_on_ack(self, ack: bool) -> List[Any]:
        "PURPOSE: Release the queue only on parent ACK (RFC 108)."
        if not ack:
            return []
        out = list(self._queue)
        self._queue.clear()
        return out

    def verify_child(self) -> bool:
        "PURPOSE: Verify the child seal recomputes to its stored INAHASH."
        compute = getattr(self.child, "compute_inahash", None)
        stored = getattr(self.child, "inahash", "")
        if compute is None or not stored:
            return False
        return stored == compute()

    def boot(self, ack: bool = True) -> Dict[str, Any]:
        "PURPOSE: Child boot result: verification plus released responses."
        return {"verified": self.verify_child(),
                "responses": self.drain_on_ack(ack)}
# =====================================================================
# MODULE END   : uro.boot.child_boot
# =====================================================================
