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
from fastapi import FastAPI, HTTPException
from uro.aegis import AegisMonitor, calculate_repulsion_vector, build_aegis_router
from uro.aegis.server import AegisState

class TestAegisCore(unittest.TestCase):
    def test_monitor_detects_critical_anomaly(self):
        monitor = AegisMonitor(epinephrine_threshold=85.0, trust_threshold=40.0)
        nte = {"EPINEPHRINE": 90.0, "OXYTOCIN": 50.0}
        report = monitor.evaluate("rogue_dock", nte, trust_score=30.0)
        self.assertIsNotNone(report)
        self.assertEqual(report.severity, "critical")
        self.assertTrue(any("EPINEPHRINE" in r for r in report.reasons))

    def test_monitor_no_anomaly(self):
        monitor = AegisMonitor()
        nte = {"EPINEPHRINE": 50.0}
        report = monitor.evaluate("healthy_dock", nte, trust_score=80.0)
        self.assertIsNone(report)

    def test_repulsion_vector(self):
        original = {"EPINEPHRINE": 50.0, "OXYTOCIN": 80.0, "DOPAMINE": 60.0}
        repulsed = calculate_repulsion_vector(original)
        self.assertEqual(repulsed["EPINEPHRINE"], 100.0)
        self.assertEqual(repulsed["OXYTOCIN"], 0.0)
        self.assertEqual(repulsed["DOPAMINE"], 60.0)

class TestAegisServer(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.state = AegisState()
        self.app = FastAPI()
        self.app.include_router(build_aegis_router(self.state))
        self.admin = {"x-uro-principal": "admin", "x-uro-role": "varuos_admin"}
        self.operator = {"x-uro-principal": "op", "x-uro-role": "operator"}

    async def test_quarantine_acl_and_state(self):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url="http://test") as client:
            resp = await client.post("/aegis/quarantine", json={"dock_name": "bad", "reason": "test", "severity": "critical"}, headers=self.operator)
            self.assertEqual(resp.status_code, 403)

            resp = await client.post("/aegis/quarantine", json={"dock_name": "bad", "reason": "test", "severity": "critical"}, headers=self.admin)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("bad", self.state.registry)

    async def test_restore_and_status(self):
        self.state.quarantine("bad", "test", "critical")
        
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url="http://test") as client:
            resp = await client.get("/aegis/status", headers=self.admin)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("bad", resp.json()["payload"]["quarantined_docks"])

            resp = await client.post("/aegis/restore", json={"dock_name": "bad"}, headers=self.admin)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("bad", self.state.registry)

if __name__ == "__main__":
    unittest.main(verbosity=2)
