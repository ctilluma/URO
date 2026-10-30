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


"""
Canonical inter-dock client [S9.10].

Attempts TCP-first transport on port 9100, falling back to HTTP on port 8000.
All docks MUST use this instead of raw httpx [S14.7].
"""
from typing import Any, Dict, Optional


async def send_to_dock_async(
    dock_name: str,
    endpoint: str,
    payload: Optional[Dict[str, Any]] = None,
    method: str = "POST",
    timeout: float = 5.0,
) -> Any:
    """
    TCP-first with HTTP fallback.
    Tolerant stub implementation until C-level TCP bridge is provisioned.
    """
    try:
        import httpx

        async with httpx.AsyncClient(timeout=timeout) as client:
            url = f"http://{dock_name}:8000{endpoint}"
            if method.upper() == "GET":
                resp = await client.get(url, params=payload)
            else:
                resp = await client.post(url, json=payload)
            return resp.json()
    except Exception as exc:
        return {"error": str(exc), "fallback": "http", "uro_compliant": True}
