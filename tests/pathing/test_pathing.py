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
from uro.uro.pathing import TrustValueProtocol, OnionRouter, BeaconManager, BeaconType, Connector, ConnectorType

class TestPathing(unittest.TestCase):
    def test_trust_value_protocol_high_confidence(self):
        tvp = TrustValueProtocol()
        responses = [{"value": "A"}] * 9 + [{"value": "B"}]
        result = tvp.evaluate_responses(responses)
        self.assertEqual(result["status"], "high_confidence")
        self.assertEqual(result["trust_points"], 2)
        self.assertEqual(result["majority_value"], "A")

    def test_trust_value_protocol_reanalyze(self):
        tvp = TrustValueProtocol()
        responses = [{"value": "A"}, {"value": "B"}, {"value": "C"}]
        result = tvp.evaluate_responses(responses)
        self.assertEqual(result["status"], "reanalyze")
        self.assertEqual(result["trust_points"], 0)

    def test_onion_router_encrypt_decrypt(self):
        router = OnionRouter()
        hops = ["hop1", "hop2", "hop3"]
        payload = {"msg": "secret"}
        
        encrypted = router.encrypt_path(hops, payload)
        self.assertEqual(encrypted["hop"], "hop1")
        
        # Decrypting hop1 reveals the plaintext metadata for hop1, including the next_hop
        layer2 = router.decrypt_layer(encrypted, "hop1")
        self.assertEqual(layer2["next_hop"], "hop2")
        self.assertEqual(layer2["current_hop"], "hop1")

    def test_beacon_manager(self):
        bm = BeaconManager()
        bm.broadcast("dock1", BeaconType.I_EXIST, {"version": "1.0"})
        bm.broadcast("dock2", BeaconType.SO_DO_I, {"version": "1.0"})
        
        all_beacons = bm.get_beacons()
        self.assertEqual(len(all_beacons), 2)
        
        exist_beacons = bm.get_beacons(BeaconType.I_EXIST)
        self.assertEqual(len(exist_beacons), 1)
        self.assertEqual(exist_beacons[0]["sender"], "dock1")

    def test_connectors(self):
        c_out = Connector.from_urid_pair("0", "dock1")
        self.assertEqual(c_out.type, ConnectorType.OUTPUT)
        
        c_in = Connector.from_urid_pair("dock1", "0")
        self.assertEqual(c_in.type, ConnectorType.INPUT)
        
        c_path = Connector.from_urid_pair("dock1", "dock2")
        self.assertEqual(c_path.type, ConnectorType.PATH)

if __name__ == "__main__":
    unittest.main(verbosity=2)
