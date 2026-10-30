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
from docks.bursar.api import app
from uro.uro.inspaneda import Ledger, to_micro

class TestBursarDock(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.admin = {"x-uro-principal": "admin", "x-uro-role": "varuos_admin"}
        self.operator = {"x-uro-principal": "op", "x-uro-role": "operator"}

    async def test_bursar_status_and_acl(self):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/licm/status", headers=self.admin)
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertIn("payload", data)
            self.assertEqual(data["payload"]["inspaneda_per_inspativo"]["value"], 1000)

            resp_op = await client.get("/licm/status", headers=self.operator)
            self.assertEqual(resp_op.status_code, 200)

    async def test_bursar_manifest(self):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/licm/manifest", headers=self.admin)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json()["payload"]["dock_id"], "bursar")

if __name__ == "__main__":
    unittest.main(verbosity=2)
