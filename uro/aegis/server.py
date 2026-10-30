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
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from uro.licm import licm_envelope, make_urid_pair, Provenance
from uro.licm.acl import authorize as acl_authorize

class QuarantineRequest(BaseModel):
    dock_name: str
    reason: str
    severity: str = "critical"

class RestoreRequest(BaseModel):
    dock_name: str

class AegisState:
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}

    def quarantine(self, dock_name: str, reason: str, severity: str):
        self.registry[dock_name] = {"reason": reason, "severity": severity, "status": "isolated"}

    def restore(self, dock_name: str):
        self.registry.pop(dock_name, None)

def build_aegis_router(state: Optional[AegisState] = None) -> APIRouter:
    state = state or AegisState()
    router = APIRouter()

    def _auth(principal, role, tier="control"):
        if not acl_authorize(principal, role, tier):
            raise HTTPException(status_code=403, detail="acl_denied")

    @router.post("/aegis/quarantine")
    async def post_quarantine(
        req: QuarantineRequest,
        x_uro_principal: Optional[str] = Header(None),
        x_uro_role: Optional[str] = Header(None),
    ):
        _auth(x_uro_principal, x_uro_role, "control")
        state.quarantine(req.dock_name, req.reason, req.severity)
        
        payload = {"action": "quarantine", "dock_name": req.dock_name, "severity": req.severity}
        return licm_envelope(
            make_urid_pair("aegis", "quarantine"),
            payload,
            {},
            Provenance.LIVE,
        )

    @router.post("/aegis/restore")
    async def post_restore(
        req: RestoreRequest,
        x_uro_principal: Optional[str] = Header(None),
        x_uro_role: Optional[str] = Header(None),
    ):
        _auth(x_uro_principal, x_uro_role, "control")
        state.restore(req.dock_name)
        payload = {"action": "restore", "dock_name": req.dock_name}
        return licm_envelope(
            make_urid_pair("aegis", "restore"),
            payload,
            {},
            Provenance.LIVE,
        )

    @router.get("/aegis/status")
    async def get_status(
        x_uro_principal: Optional[str] = Header(None),
        x_uro_role: Optional[str] = Header(None),
    ):
        _auth(x_uro_principal, x_uro_role, "read")
        payload = {"quarantined_docks": state.registry}
        return licm_envelope(
            make_urid_pair("aegis", "status"),
            payload,
            {},
            Provenance.LIVE,
        )

    return router
