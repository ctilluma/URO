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

from typing import Any

from fastapi import FastAPI

from .provenance import derive_from_registry, live, unmeasured
from .server import build_licm_router

try:
    from uro.transport.universal_listener import install_tcp_listener
except Exception:

    def install_tcp_listener(app: Any, dock_name: str = "dock", port: int = 9100, host: str = "0.0.0.0") -> Any:
        return app


def create_example_dock(dock_name: str = "example_dev") -> FastAPI:
    app = FastAPI(title=f"{dock_name} LICM example")

    manifest = {
        "dock_id": dock_name,
        "menu_label": "Example Dock",
        "icon": "cube",
        "color_accent": "#22c55e",
        "pitch": "Reference LICM dock wiring.",
        "views": [{"id": "status", "label": "Status", "source": "/licm/status"}],
        "endpoints": [{"path": "/licm/status", "method": "GET", "tier": "read"}],
        "ws_channel": f"{dock_name}.licm.events",
        "compliance": {"S2": True, "S4": True, "S7": True, "S9": True},
    }

    def status_provider():
        return {
            "heartbeat": live(True),
            "dock_id": derive_from_registry(dock_name, derivation="example_dock.config"),
            "queue_depth": unmeasured("example dock has no queue sensor"),
        }

    def nte_provider():
        return {"glutamate": 55.0, "gaba": 45.0}

    async def ping_action(args):
        return {"pong": args}

    providers = {
        "status": status_provider,
        "nte": nte_provider,
        "actions": {
            "ping": ping_action,
        },
    }

    app.include_router(build_licm_router(dock_name, manifest, providers))
    install_tcp_listener(app, dock_name=dock_name)
    return app
