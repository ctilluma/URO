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
MODULE: Cognitive Persistence (Robust)
INTENT: Saves/restores CognitiveCore state via memory dock's HTTP API
        (not the fire-and-forget coordinator bus). Ensures state survives
        restart by calling /memory/store and /memory/retrieve directly.
STANDARD: URO-STD-0001 S30
"""
from __future__ import annotations

import os
import logging
from typing import Optional, Dict, Any


from uro.cognition.core import CognitiveCore
# === START: canonical_transport_wrapper ===

class _MockResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code
    def json(self): return self._data
    def raise_for_status(self):
        if self.status_code != 200: raise Exception(f"HTTP {self.status_code}")

class _CanonicalTransportWrapper:
    """S9.10 TCP-First Transport Wrapper for legacy httpx call sites."""
    def __init__(self, timeout=20.0):
        self.timeout = timeout
        
    async def post(self, url, json=None, **kwargs):
        from uro.transport.inter_dock_client import send_to_dock_async
        from urllib.parse import urlparse
        parsed = urlparse(url)
        dock_name = parsed.hostname.split('_')[0] if '_' in (parsed.hostname or "") else (parsed.hostname or "memory")
        endpoint = parsed.path
        res = await send_to_dock_async(dock_name, endpoint, json or {}, method="POST", timeout=self.timeout)
        return _MockResponse(res, 200 if res is not None else 500)
        
    async def get(self, url, **kwargs):
        from uro.transport.inter_dock_client import send_to_dock_async
        from urllib.parse import urlparse
        parsed = urlparse(url)
        dock_name = parsed.hostname.split('_')[0] if '_' in (parsed.hostname or "") else (parsed.hostname or "memory")
        endpoint = parsed.path
        res = await send_to_dock_async(dock_name, endpoint, {}, method="GET", timeout=self.timeout)
        return _MockResponse(res, 200 if res is not None else 500)

    async def __aenter__(self): return self
    async def __aexit__(self, *args): pass

# === END: canonical_transport_wrapper ===


logger = logging.getLogger("CognitivePersistence")


class CognitivePersistence:
    """Saves/restores CognitiveCore to/from memory dock via HTTP."""

# === START: tcp_first_pers_init ===
    def __init__(self, dock_name: str = "cognitive"):
        self.dock_name = dock_name
        self.memory_url = self._get_memory_url()
        self.client = _CanonicalTransportWrapper(timeout=20.0)
# === END: tcp_first_pers_init ===

    def _get_memory_url(self) -> str:
        """Resolve memory dock URL."""
        env = os.getenv("AURA_ENV", "prod")
        for host in [f"memory_{env}", "memory_prod", "memory"]:
            try:
                return f"http://{host}:8000"
            except:
                continue
        return "http://memory_prod:8000"

    async def save(self, core: CognitiveCore) -> bool:
        """Save CognitiveCore snapshot to memory dock."""
        try:
            snapshot = core.snapshot()
            payload = {
                "key": f"{self.dock_name}_core_snapshot",
                "data": snapshot,
                "tier": "structured_memory",  # Permanent storage
                "ttl": None,  # No expiry
                "metadata": {"source": self.dock_name, "type": "core_snapshot"}
            }
            r = await self.client.post(f"{self.memory_url}/memory/store", json=payload)
            if r.status_code == 200:
                logger.info(f"💾 Saved CognitiveCore snapshot ({len(core.episodes)} episodes)")
                return True
            else:
                logger.error(f"Failed to save: {r.status_code} {r.text}")
                return False
        except Exception as e:
            logger.error(f"Save error: {e}")
            return False

    async def restore(self, core: CognitiveCore) -> bool:
        """Restore CognitiveCore from memory dock."""
        try:
            payload = {"key": f"{self.dock_name}_core_snapshot"}
            r = await self.client.post(f"{self.memory_url}/memory/retrieve", json=payload)
            if r.status_code == 200:
                result = r.json()
                if "data" in result:
                    snapshot = result["data"]
                    # Restore episodes
                    if "episodes" in snapshot:
                        core.episodes = snapshot["episodes"]
                        core.by_id = {ep["id"]: ep for ep in core.episodes}
                    # Restore prototypes
                    if "prototypes" in snapshot:
                        core.matrix.prototypes = snapshot["prototypes"]
                    # Restore NTE
                    if "nte" in snapshot:
                        from uro.nte.axes import NTEAxis
                        for ax_name, level in snapshot["nte"].items():
                            try:
                                ax = NTEAxis(ax_name)
                                core.nte.set_level(ax, level)
                            except:
                                pass
                    logger.info(f"✅ Restored CognitiveCore: {len(core.episodes)} episodes")
                    return True
                else:
                    logger.warning("No snapshot found in memory dock")
                    return False
            else:
                logger.error(f"Restore failed: {r.status_code} {r.text}")
                return False
        except Exception as e:
            logger.error(f"Restore error: {e}")
            return False

    async def close(self):
        await self.client.aclose()
