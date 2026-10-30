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
VAUROS Canonical Cognitive Integration Bridge
Provides a unified, cache-first interface for any dock (Coder, Architect, etc.)
to request semantic generation, reasoning, or code synthesis.

MANDATE: Only Cognitive has direct access to the LLM. 
This library routes through Cognitive to enforce caching and NTE awareness.
"""
# === START: canonical_transport_wrapper ===

class _MockResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code
    def json(self): return self._data if self._data else {}
    def raise_for_status(self):
        if self.status_code != 200: raise Exception(f"HTTP {self.status_code}")
    @property
    def text(self): return str(self._data)
    @property
    def content(self): return str(self._data).encode('utf-8')

class _CanonicalTransportWrapper:
    """S9.10 TCP-First Transport Wrapper for legacy httpx call sites."""
    def __init__(self, timeout=20.0):
        self.timeout = timeout
        
    async def post(self, url, json=None, **kwargs):
        from uro.transport.inter_dock_client import send_to_dock_async
        from urllib.parse import urlparse
        parsed = urlparse(url)
        host = parsed.hostname or "memory"
        dock_name = host.split('_')[0] if '_' in host else host
        if not dock_name: dock_name = "memory"
        endpoint = parsed.path
        res = await send_to_dock_async(dock_name, endpoint, json or {}, method="POST", timeout=self.timeout)
        return _MockResponse(res, 200 if res is not None else 500)
        
    async def get(self, url, **kwargs):
        from uro.transport.inter_dock_client import send_to_dock_async
        from urllib.parse import urlparse
        parsed = urlparse(url)
        host = parsed.hostname or "memory"
        dock_name = host.split('_')[0] if '_' in host else host
        if not dock_name: dock_name = "memory"
        endpoint = parsed.path
        res = await send_to_dock_async(dock_name, endpoint, {}, method="GET", timeout=self.timeout)
        return _MockResponse(res, 200 if res is not None else 500)

    async def __aenter__(self): return self
    async def __aexit__(self, *args): pass

# === END: canonical_transport_wrapper ===


from uro.transport.inter_dock_client import send_to_dock_async

import logging
import json
import uuid
from typing import Dict, Any, Optional

logger = logging.getLogger("uro.cognitive_integration.bridge")

# Cognitive is the gateway for all LLM interactions
COGNITIVE_URL = "http://cognitive_prod:8000"

async def request_semantic_generation(
    file_path: str, 
    original_code: str, 
    prompt: str, 
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Canonical entry point for requesting code generation or semantic analysis.
    
    Args:
        file_path: The relative path of the file being modified.
        original_code: The current source code (for context/caching).
        prompt: The instruction or improvement plan.
        context: Additional context (NTE state, architectural constraints).
        
    Returns:
        Dict containing 'status', 'generated_code', and 'cache_hit' flag.
    """
    # Generate a unique query ID for tracking and caching
    query_id = f"coder_gen_{uuid.uuid4().hex[:8]}"
    
    # Construct the exact QueryPayload schema expected by Cognitive
    payload = {
        "query_id": query_id,
        "session_id": "coder_cap_45",
        "text": prompt,
        "username": "aura_forge_coder",
        "role": "coder"
    }
    
# === START: tcp_first_bridge ===
    try:
        # Use canonical TCP-first transport (S9.10)
        data = await send_to_dock_async(
            dock_name="cognitive",
            endpoint="/process_query",
            payload=payload,
            method="POST",
            timeout=300.0
        )
        if data is None:
            return {"status": "error", "error": "Cognitive returned no data", "generated_code": ""}
            
        # Extract generated code from Cognitive's response
        # Cognitive often returns the result in 'rag_context', 'response', or 'working_memory'
        generated = data.get("generated_code") or data.get("response", {}).get("text", "")
        
        # Attempt to parse rag_context if it contains the code
        if not generated and data.get("rag_context"):
            try:
                rag = json.loads(data["rag_context"])
                generated = rag.get("full_response", "") or rag.get("text", "")
            except Exception:
                pass
        
        # Fallback to working_memory if available
        if not generated and data.get("working_memory"):
            wm = data["working_memory"]
            generated = wm[-1] if isinstance(wm, list) and wm else str(wm)
        
        return {
            "status": "success",
            "generated_code": generated,
            "cache_hit": data.get("cache_hit", False),
            "raw_response": data
        }
    except Exception as e:
        logger.error(f"Cognitive generation request failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e), "generated_code": ""}
# === END: tcp_first_bridge ===
