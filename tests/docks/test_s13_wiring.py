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


import unittest
import httpx
import sys
import os

# Ensure docks are importable
sys.path.insert(0, os.path.abspath("docks/coordinator"))
sys.path.insert(0, os.path.abspath("docks/phoenix"))

from docks.coordinator.s13_endpoints import apply_s13_wiring as coord_wiring
from docks.phoenix.s13_endpoints import apply_s13_wiring as phoenix_wiring
from fastapi import FastAPI

class TestS13Wiring(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.coord_app = FastAPI()
        coord_wiring(self.coord_app)
        
        self.phoenix_app = FastAPI()
        phoenix_wiring(self.phoenix_app)
        
        self.admin = {"x-uro-principal": "admin", "x-uro-role": "varuos_admin"}

    async def test_coordinator_aegis_quarantine(self):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=self.coord_app), base_url="http://test") as client:
            resp = await client.post("/aegis/quarantine", json={"dock_name": "rogue", "reason": "test", "severity": "critical"}, headers=self.admin)
            self.assertEqual(resp.status_code, 200)

    async def test_phoenix_restore(self):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=self.phoenix_app), base_url="http://test") as client:
            resp = await client.post("/phoenix/restore", json={"dock_name": "rogue", "reason": "test"}, headers=self.admin)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json()["payload"]["action"], "restore")

if __name__ == "__main__":
    unittest.main(verbosity=2)
