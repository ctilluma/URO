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


"""
Shared helper: any dock imports this to use Cognitive (reasoning) and
Memory (storage) instead of doing its own. This is the migration target.
"""
import os, sys
sys.path.insert(0, "/opt/uro")
from uro.coordinator_bus import CoordinatorBus

class BrainClient:
    def __init__(self, dock_name):
        self.bus = CoordinatorBus(dock_name)

    async def think(self, prompt, context=None):
        """Delegate reasoning to Cognitive."""
        return await self.bus.query_cognitive(prompt, context or {})

    async def remember(self, key, entity, data, ttl=None):
        """Delegate storage to Memory."""
        return await self.bus.store_memory(key=key, entity=entity, data=data, ttl=ttl)

    async def recall(self, key="", entity="", filters=None):
        """Delegate retrieval to Memory."""
        return await self.bus.retrieve_memory(key=key, entity=entity)

    async def synthesize(self, prompt, model=None):
        """Delegate LLM synthesis to LLM Bridge."""
        return await self.bus.request_llm(prompt, model=model)
