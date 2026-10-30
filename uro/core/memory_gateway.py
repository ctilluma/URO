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
V.A.U.R.O.S. UNIVERSAL MEMORY GATEWAY (Core Library)
Accepts any incoming data, classifies its intent, deduplicates via INAHASH, 
and routes it to the appropriate memory tier (Redis, Qdrant, Postgres) 
without redundant learning loops.
"""
import os
import json
import logging
import hashlib
from typing import Dict, Any, Optional

logger = logging.getLogger("URO.MemoryGateway")

class UniversalMemoryGateway:
    """
    Core library component to handle unified memory classification and storage.
    """
    def __init__(self, bus_instance: Any = None):
        self.bus = bus_instance
        self.seen_signatures = set()

    def classify_and_route(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classifies raw input, determines target backend, and computes INAHASH deduplication.
        """
        intent = data.get("intent", "memory.store")
        payload = data.get("payload", data)
        if not isinstance(payload, dict):
            payload = {"content": payload}

        # Compute deterministic signature for deduplication
        signature_payload = json.dumps({"intent": intent, "payload": payload}, sort_keys=True)
        inahash_sig = hashlib.sha256(signature_payload.encode()).hexdigest()

        if inahash_sig in self.seen_signatures:
            return {
                "status": "deduplicated",
                "inahash": inahash_sig,
                "message": "Signature already processed. Bypassing redundant swarm broadcast."
            }

        self.seen_signatures.add(inahash_sig)
        if len(self.seen_signatures) > 1000:
            self.seen_signatures.pop() # Prevent boundless memory growth

        # Classification Logic
        target_backends = []
        if "vector" in payload or "embedding" in payload or "semantic" in intent:
            target_backends.append("qdrant")
        if "cache" in intent or "ttl" in payload or "temporary" in payload:
            target_backends.append("redis")
        if not target_backends or "store" in intent or "query" in intent or "schema" in intent:
            target_backends.append("postgres")

        return {
            "status": "classified",
            "inahash": inahash_sig,
            "intent": intent,
            "recommended_backends": target_backends,
            "payload": payload
        }

    async def commit_to_memory_uro(self, classified_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Commits classified data through the CoordinatorBus to the Memory Dock.
        """
        if classified_data.get("status") == "deduplicated":
            return classified_data

        if self.bus and hasattr(self.bus, "store_memory"):
            try:
                await self.bus.store_memory(
                    key=f"gateway_commit_{classified_data['inahash'][:12]}",
                    entity="universal_memory_uro",
                    data=classified_data
                )
                logger.info(f"💾 Committed URO to Memory URO across backends: {classified_data['recommended_backends']}")
            except Exception as e:
                logger.error(f"Failed to commit to Memory URO via bus: {e}")

        return classified_data
