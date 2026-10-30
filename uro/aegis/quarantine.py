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


from __future__ import annotations
from typing import Any, Dict
from uro.licm.client import licm_call

class QuarantineClient:
    """
    S13.4 / S13.5: Client to enforce quarantine and trigger Phoenix restoration.
    """
    def __init__(self, coordinator_dock: str = "coordinator"):
        self.coordinator_dock = coordinator_dock
        self.phoenix_dock = "phoenix"

    async def isolate(self, dock_name: str, reason: str, severity: str = "critical") -> Dict[str, Any]:
        return await licm_call(
            self.coordinator_dock,
            "/aegis/quarantine",
            payload={"dock_name": dock_name, "reason": reason, "severity": severity},
            method="POST",
        )

    async def restore(self, dock_name: str) -> Dict[str, Any]:
        return await licm_call(
            self.coordinator_dock,
            "/aegis/restore",
            payload={"dock_name": dock_name},
            method="POST",
        )

    async def rebuild(self, dock_name: str, reason: str) -> Dict[str, Any]:
        return await licm_call(
            self.phoenix_dock,
            "/phoenix/restore",
            payload={"dock_name": dock_name, "reason": reason},
            method="POST",
        )
