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
import time
from uro.memory import MemoryEngine, MemoryItem, MemoryTier, apply_cognitive_decay

class TestMemoryDecay(unittest.TestCase):
    def test_cognitive_decay_formula(self):
        # S8.5: decayed_conf = original_conf * (0.95 ^ age_in_hours)
        self.assertAlmostEqual(apply_cognitive_decay(1.0, 0.0), 1.0)
        self.assertAlmostEqual(apply_cognitive_decay(1.0, 1.0), 0.95)
        self.assertAlmostEqual(apply_cognitive_decay(1.0, 2.0), 0.9025)
        self.assertAlmostEqual(apply_cognitive_decay(0.5, 1.0), 0.475)

class TestMemoryEngine(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.engine = MemoryEngine(decay_threshold=0.1, consolidation_threshold=3)
        self.urid = {"urid1": "urn:test:dock", "urid2": "obj1"}

    def test_store_and_retrieve(self):
        item = MemoryItem(urid_pair=self.urid, payload="test_data", confidence=1.0)
        self.engine.store(item)
        
        retrieved = self.engine.retrieve(self.urid)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.payload, "test_data")
        self.assertEqual(retrieved.use_count, 1)

    def test_consolidation_short_to_long(self):
        item = MemoryItem(urid_pair=self.urid, payload="data", tier=MemoryTier.SHORT)
        self.engine.store(item)
        
        # Retrieve 3 times to hit consolidation_threshold
        for _ in range(3):
            self.engine.retrieve(self.urid)
            
        consolidated = self.engine.consolidate()
        self.assertEqual(consolidated, 1)
        
        key = f"{self.urid['urid1']}:{self.urid['urid2']}"
        self.assertEqual(self.engine._store[key].tier, MemoryTier.LONG)

    def test_cognitive_decay_pruning(self):
        # Create an item with low initial confidence
        item = MemoryItem(urid_pair=self.urid, payload="fading", confidence=0.11)
        # Fake the created_at time to be 2 hours ago
        item.created_at = time.time() - (2 * 3600)
        self.engine.store(item)
        
        pruned = self.engine.decay_all()
        self.assertIn(f"{self.urid['urid1']}:{self.urid['urid2']}", pruned)
        self.assertIsNone(self.engine.retrieve(self.urid))

    def test_tier_counts(self):
        self.engine.store(MemoryItem(urid_pair={"urid1": "a", "urid2": "1"}, payload="a", tier=MemoryTier.SHORT))
        self.engine.store(MemoryItem(urid_pair={"urid1": "b", "urid2": "2"}, payload="b", tier=MemoryTier.LONG))
        self.engine.store(MemoryItem(urid_pair={"urid1": "c", "urid2": "3"}, payload="c", tier=MemoryTier.LONG))
        
        counts = self.engine.get_tier_counts()
        self.assertEqual(counts[MemoryTier.SHORT.value], 1)
        self.assertEqual(counts[MemoryTier.LONG.value], 2)

if __name__ == "__main__":
    unittest.main(verbosity=2)
