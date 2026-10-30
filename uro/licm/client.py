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

import os
import time
from typing import Any, Dict, Optional

from .exceptions import LicmTransportError

try:
    from uro.transport.inter_dock_client import send_to_dock_async
except Exception:
    send_to_dock_async = None

AURA_ENV = os.getenv("AURA_ENV", "dev")


def env_dock_name(dock: str, env: Optional[str] = None) -> str:
    env = env or AURA_ENV
    dock = str(dock)
    suffix = f"_{env}"
    return dock if dock.endswith(suffix) else f"{dock}{suffix}"


async def licm_call(
    dock: str,
    path: str,
    payload: Any = None,
    method: str = "GET",
    timeout: float = 5.0,
    headers: Optional[Dict[str, str]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Canonical LICM inter-dock call.
    Uses send_to_dock_async TCP-first with HTTP fallback (S9.10).
    Measures real latency (S14.7). Env-suffixed dock names mandatory.
    """
    if send_to_dock_async is None:
        raise LicmTransportError(
            "canonical send_to_dock_async is unavailable; wire uro.transport.inter_dock_client"
        )

    dock_name = env_dock_name(dock)
    path = path if path.startswith("/") else f"/{path}"

    started = time.perf_counter()
    try:
        result = await send_to_dock_async(
            dock_name=dock_name,
            endpoint=path,
            payload=payload,
            method=method,
            timeout=timeout,
            headers=headers,
            **kwargs,
        )
    except Exception as exc:
        latency = time.perf_counter() - started
        raise LicmTransportError(
            f"LICM transport failure dock={dock_name} path={path} method={method} "
            f"latency={latency:.6f}s error={exc}"
        ) from exc

    latency = time.perf_counter() - started
    status_code = None
    if isinstance(result, dict):
        status_code = result.get("status_code")

    ok = status_code is None or (200 <= int(status_code) < 300)
    return {
        "ok": ok,
        "dock": dock_name,
        "path": path,
        "method": method,
        "latency_s": latency,
        "status_code": status_code,
        "result": result,
    }
