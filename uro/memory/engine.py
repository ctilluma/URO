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
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .decay import apply_cognitive_decay, hours_since

class MemoryTier(str, Enum):
    WORKING = "SF_REGISTER"   # Fastest, immediate (S8.1)
    SHORT = "F_RAM"           # Short-term (S8.1)
    LONG = "M_SSD"            # Long-term (S8.1)
    ARCHIVE = "S_HD"          # Archive (S8.1)

@dataclass
class MemoryItem:
    urid_pair: Dict[str, str]
    payload: Any
    confidence: float = 1.0
    tier: MemoryTier = MemoryTier.SHORT
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    use_count: int = 0
    attachment: float = 0.0  # S8.4: more attachment = more chance to consolidate
    saved_long: bool = False  # RFC 66: a long-term copy of this item exists

    @property
    def key(self) -> str:
        return f"{self.urid_pair.get('urid1', '')}:{self.urid_pair.get('urid2', '')}"

class MemoryEngine:
    """
    URO S8 Memory Architecture.
    Manages tier transitions, cognitive decay, and consolidation.
    """
    def __init__(self, decay_threshold: float = 0.1, consolidation_threshold: int = 5):
        self.decay_threshold = decay_threshold
        self.consolidation_threshold = consolidation_threshold
        self._store: Dict[str, MemoryItem] = {}
        self._morning_questions: List[str] = []

    def store(self, item: MemoryItem) -> None:
        self._store[item.key] = item

    def retrieve(self, urid_pair: Dict[str, str]) -> Optional[MemoryItem]:
        key = f"{urid_pair.get('urid1', '')}:{urid_pair.get('urid2', '')}"
        item = self._store.get(key)
        if item:
            item.use_count += 1
            item.last_accessed = time.time()
            # S8.4: Boost in prepared activity may request more working/short memory
            if item.tier == MemoryTier.LONG:
                item.tier = MemoryTier.SHORT
            elif item.tier == MemoryTier.SHORT:
                item.tier = MemoryTier.WORKING
        return item

    def decay_all(self) -> List[str]:
        """
        S8.5: Apply cognitive decay to all items.
        Prune items below decay_threshold (0.1 confidence).
        Returns list of pruned keys.
        """
        pruned = []
        for key, item in list(self._store.items()):
            age_hours = hours_since(item.created_at)
            item.confidence = apply_cognitive_decay(item.confidence, age_hours)
            
            if item.confidence < self.decay_threshold:
                del self._store[key]
                pruned.append(key)
        return pruned

    def consolidate(self, epinephrine: float = 0.0) -> int:
        """
        S8.3 / S8.4: Move items from SHORT to LONG based on use_count and attachment.
        Returns number of items consolidated.
        """
        consolidated = 0
        for item in self._store.values():
            if item.tier == MemoryTier.SHORT:
                # S8.3: use counter combined with attachment decides promotion
                threshold = self.consolidation_threshold - 2 if epinephrine > 70.0 else self.consolidation_threshold
                if item.use_count >= threshold or item.attachment > 0.8:
                    item.tier = MemoryTier.LONG
                    item.saved_long = True
                    consolidated += 1
        return consolidated

    # === START: RFC 66 Connection Use Counter Pass ===
    def connection_pass(self, item: MemoryItem, acl_permit: bool = True,
                        potentiator: float = 0.5) -> str:
        "PURPOSE: RFC 66 four-outcome per-pass decision from use counter, ACL, potentiators, last access."
        if not acl_permit:
            return "DROP_SHORT"
        recent = hours_since(item.last_accessed) < 24.0
        high_use = item.use_count >= self.consolidation_threshold
        attached = item.attachment > 0.8 or potentiator > 0.8
        if high_use or attached:
            return "SAVE_LONG_KEEP_SHORT" if recent else "SAVE_LONG_DROP_SHORT"
        if recent:
            return "KEEP_SHORT_ONLY"
        return "DROP_SHORT"

    def apply_pass(self, item: MemoryItem, outcome: str) -> None:
        "PURPOSE: Execute one RFC 66 outcome against the store."
        if outcome == "SAVE_LONG_KEEP_SHORT":
            item.saved_long = True
            item.tier = MemoryTier.SHORT
        elif outcome == "SAVE_LONG_DROP_SHORT":
            item.saved_long = True
            item.tier = MemoryTier.LONG
        elif outcome == "KEEP_SHORT_ONLY":
            item.tier = MemoryTier.SHORT
        elif outcome == "DROP_SHORT":
            if item.saved_long:
                item.tier = MemoryTier.LONG
            else:
                self._store.pop(item.key, None)
    # === END: RFC 66 Connection Use Counter Pass ===

    # === START: RFC 65.2 Introspection Clear ===
    def introspect(self) -> Dict[str, int]:
        "PURPOSE: RFC 65.2 clear work to short and short to long at introspection."
        moved = {"working_to_short": 0, "short_to_long": 0}
        for item in self._store.values():
            if item.tier == MemoryTier.WORKING:
                item.tier = MemoryTier.SHORT
                moved["working_to_short"] += 1
            elif item.tier == MemoryTier.SHORT:
                item.tier = MemoryTier.LONG
                item.saved_long = True
                moved["short_to_long"] += 1
        return moved
    # === END: RFC 65.2 Introspection Clear ===

    # === START: RFC 68 Sleep Mode and Morning Questions ===
    def sleep_mode(self, authorized_inputs: Optional[List[str]] = None,
                   melatonin_rise: float = 20.0) -> Dict[str, Any]:
        "PURPOSE: RFC 68.1 reduced ACL set, pruning cycles, melatonin rise."
        pruned = self.decay_all()
        consolidated = self.consolidate()
        return {
            "authorized_inputs": list(authorized_inputs or []),
            "reduced_acl": True,
            "pruned": pruned,
            "consolidated": consolidated,
            "melatonin_rise": melatonin_rise,
        }

    def queue_morning_question(self, question: str) -> None:
        "PURPOSE: RFC 68.2 queue morning questions comparing past and now."
        self._morning_questions.append(question)

    def drain_morning_questions(self) -> List[str]:
        "PURPOSE: Return and clear the morning question queue."
        out = list(self._morning_questions)
        self._morning_questions.clear()
        return out
    # === END: RFC 68 Sleep Mode and Morning Questions ===

    # === START: RFC 69 Downtime Reflection ===
    def downtime_reflection(self, failed_pathing_counts: Optional[Dict[str, int]] = None,
                            learn_threshold: int = 3) -> Dict[str, List[str]]:
        "PURPOSE: RFC 69 four reflection objectives over short-term connections."
        failed = failed_pathing_counts or {}
        return {
            "learn_object": [i.key for i in self._store.values()
                             if i.tier == MemoryTier.SHORT and i.use_count == 1],
            "handle_differently": [i.key for i in self._store.values()
                                   if i.tier == MemoryTier.SHORT and i.confidence < 0.5],
            "resolve_better": [i.key for i in self._store.values()
                               if i.tier == MemoryTier.WORKING],
            "learn_frequency": [k for k, n in failed.items() if n >= learn_threshold],
        }
    # === END: RFC 69 Downtime Reflection ===

    # === START: RFC 67.3 Cache Frequency ===
    def cache_time(self, item: MemoryItem) -> float:
        "PURPOSE: RFC 67.3 cache time for no-path objects equals search frequency."
        return float(item.use_count)
    # === END: RFC 67.3 Cache Frequency ===

    def get_tier_counts(self) -> Dict[str, int]:
        counts = {tier.value: 0 for tier in MemoryTier}
        for item in self._store.values():
            counts[item.tier.value] += 1
        return counts
