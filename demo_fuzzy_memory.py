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


from types import SimpleNamespace as E
import time
from uro.cognition import (should_promote_fuzzy, should_decay_fuzzy,
                           rank_memmaries_for_retrieval if False else rank_memories_for_retrieval)
from uro.nte.state import NTEStateURO
from uro.nte.axes import NTEAxis
from uro.core.urid import URID

now = time.time()
entries = [
    E(key="frequent_low_trust", access_count=50, last_accessed=now-60,
      tags=["low"], metadata={"source_trust": 20}, vector_embedding=[.1,.2,.3], urid1_source="low"),
    E(key="rare_high_trust", access_count=2, last_accessed=now-3600,
      tags=["critical"], metadata={"source_trust": 90}, vector_embedding=[.1,.2,.3], urid1_source="high"),
    E(key="moderate_recent", access_count=10, last_accessed=now-300,
      tags=["high"], metadata={"source_trust": 60}, vector_embedding=[.1,.2,.3], urid1_source="med"),
]

nte = NTEStateURO(urid1=URID.new(), urid2=URID.new())

print("HARDCODED vs FUZZY promotion:")
for e in entries:
    hard = e.access_count > 5
    soft, why = should_promote_fuzzy(e, nte)
    print(f"  {e.key:20s} hardcoded={hard}  fuzzy={soft}  ({why})")

nte.set_level(NTEAxis.CANNABINOID, 85)  # high pruning pressure
print("\nUnder high cannabinoid (pruning):")
for e in entries:
    hard = (now - e.last_accessed) > 300
    soft, why = should_decay_fuzzy(e, nte, tier_load=0.9)
    print(f"  {e.key:20s} hardcoded={hard}  fuzzy_prune={soft}  ({why})")

nte.set_level(NTEAxis.CANNABINOID, 15)
ranked = rank_memories_for_retrieval(entries, query_embedding=[.1,.2,.3],
                                     trust_map={"low":20,"high":90,"med":60}, nte=nte)
print("\nTrust-weighted retrieval ranking:")
for e, s in ranked:
    print(f"  {e.key:20s} strength={s:.2f}")
print("\nNote: frequent_low_trust is down-weighted despite high access count.")
