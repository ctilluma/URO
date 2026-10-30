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


"""V.A.U.R.O.S. Belief Faculty (Phase 3c.1).

A stateful epistemic service that unifies the four Phase-3b modules
(belief_state, belief_graph, calibration, belief_revision) behind one API,
with pluggable persistence.

Design laws:
- claim_hash is deterministic and normalized (same claim -> same belief state).
- Ingest applies evidence with per-origin saturation (repetition is not evidence).
- Query returns posterior mean + recalibrated confidence.
- Revision uses the entanglement graph to auto-contract contradictions.
- State is JSON-serializable so it can persist to Redis / disk.
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

import hashlib
import re
import json
from typing import Dict, Any, Optional

from uro.belief_state import new_belief, apply_evidence, posterior_mean, posterior_variance, belief_strength
from uro.belief_graph import new_synapse_graph, add_synapse, propagate_delta
from uro.calibration import (
    new_calibration_ledger, add_observation, record_prediction,
    resolve_prediction, recalibrate,
)
from uro.belief_revision import revise as agm_revise, is_believed, contradictions_of


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).strip().lower())


def claim_hash(text: str) -> str:
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()[:32]


def default_state() -> Dict[str, Any]:
    return {
        "ledger": {},
        "graph": new_synapse_graph(),
        "calibration": new_calibration_ledger(),
    }


class InMemoryStore:
    """Reference persistence backend for tests."""
    def __init__(self):
        self._state = None

    def load(self) -> Dict[str, Any]:
        return self._state if self._state is not None else default_state()

    def save(self, state: Dict[str, Any]) -> None:
        self._state = state


class RedisStore:
    """Redis-backed persistence for the live swarm.

    Stores the entire belief state as one JSON blob (atomic + simple).
    For very large ledgers, shard per-claim in a later phase.
    """
    def __init__(self, redis_client, key: str = "vauros.belief.faculty.state"):
        self.redis = redis_client
        self.key = key

    def load(self) -> Dict[str, Any]:
        try:
            raw = self.redis.get(self.key)
            if raw:
                return json.loads(raw)
        except Exception:
            pass
        return default_state()

    def save(self, state: Dict[str, Any]) -> None:
        try:
            self.redis.set(self.key, json.dumps(state))
        except Exception:
            pass


class BeliefFaculty:
    def __init__(self, store=None):
        self.store = store or InMemoryStore()
        self.state = self.store.load()

    # -- persistence --------------------------------------------------------
    def _persist(self):
        self.store.save(self.state)

    # -- ingestion ----------------------------------------------------------
    def ingest(self, text: str, trust: float, origin: str,
               stance: str = "confirm", now: Optional[float] = None) -> Dict[str, Any]:
        """Apply one piece of evidence to the claim's belief state (saturating)."""
        h = claim_hash(text)
        ledger = self.state["ledger"]
        b = ledger.get(h) or new_belief(h, now=now)
        b = apply_evidence(b, origin=origin, trust=trust, stance=stance, now=now)
        ledger[h] = b
        self._persist()
        return b

    # -- entanglement -------------------------------------------------------
    def link(self, text_a: str, text_b: str, relation: str = "supports",
             weight: float = 1.0) -> None:
        add_synapse(self.state["graph"], claim_hash(text_a), claim_hash(text_b),
                    weight=weight, relation=relation)
        self._persist()

    def propagate(self, text: str, delta: float, max_depth: int = 2) -> None:
        """Explicitly propagate a belief-strength delta through the entanglement graph."""
        h = claim_hash(text)
        self.state["ledger"] = propagate_delta(
            self.state["graph"], self.state["ledger"], h, delta, max_depth=max_depth)
        self._persist()

    # -- revision -----------------------------------------------------------
    def revise(self, text: str, trust: float, origin: str,
               now: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """AGM revision: contract entangled contradictions, then expand by text."""
        h = claim_hash(text)
        contra = contradictions_of(self.state["graph"], h)
        self.state["ledger"] = agm_revise(
            self.state["ledger"], h, trust, origin, contradictions=contra, now=now)
        self._persist()
        return self.state["ledger"].get(h)

    # -- calibration --------------------------------------------------------
    def record_calibration(self, confidence: float, outcome: int,
                           now: Optional[float] = None) -> None:
        add_observation(self.state["calibration"], confidence, outcome, now=now)
        self._persist()

    def resolve(self, text: str, outcome: int, now: Optional[float] = None) -> None:
        """Resolve a known claim against ground truth, feeding the calibration ledger."""
        h = claim_hash(text)
        b = self.state["ledger"].get(h)
        if b is None:
            return
        record_prediction(self.state["calibration"], h, posterior_mean(b), now=now)
        resolve_prediction(self.state["calibration"], h, outcome, now=now)
        self._persist()

    # -- query --------------------------------------------------------------
    def query(self, text: str) -> Dict[str, Any]:
        """Return the belief state + recalibrated confidence for a claim."""
        h = claim_hash(text)
        b = self.state["ledger"].get(h)
        if b is None:
            return {"known": False, "claim_hash": h, "confidence": 0.0,
                    "mean": 0.5, "recalibrated_confidence": 0.0}
        mean = posterior_mean(b)
        recal = recalibrate(self.state["calibration"], mean)
        return {
            "known": True,
            "claim_hash": h,
            "mean": mean,
            "variance": posterior_variance(b),
            "strength": belief_strength(b),
            "recalibrated_confidence": recal,
            "status": b.get("status", "active"),
            "believed": is_believed(b),
        }


class MemoryDockStore:
    """Memory-dock-backed persistence for BeliefFaculty.
    
    All storage goes through the Memory dock's HTTP API, never direct Redis.
    This maintains the swarm's architectural invariant: only Memory touches storage.
    """
    def __init__(self, memory_dock_url: str, key: str = "vauros.belief.faculty.state"):
        self.memory_dock_url = memory_dock_url.rstrip('/')
        self.key = key
    
# === START: tcp_first_store ===
    async def _store(self, state: Dict[str, Any]) -> None:
        """Store belief state via Memory dock."""
        try:
            await send_to_dock_async(
                dock_name="memory",
                endpoint="/memory/store",
                payload={
                    "key": self.key,
                    "data": {"state": state},
                    "memory_type": "belief_state",
                    "ttl_seconds": None  # Permanent
                },
                method="POST",
                timeout=5.0
            )
        except Exception:
            pass  # Fire-and-forget: belief state persistence is best-effort
# === END: tcp_first_store ===
    
# === START: tcp_first_load ===
    async def _load(self) -> Optional[Dict[str, Any]]:
        """Load belief state via Memory dock."""
        try:
            data = await send_to_dock_async(
                dock_name="memory",
                endpoint=f"/memory/retrieve/{self.key}",
                payload={},
                method="GET",
                timeout=5.0
            )
            if data:
                return data.get("data", {}).get("state")
        except Exception:
            pass
        return None
# === END: tcp_first_load ===
    
    def load(self) -> Dict[str, Any]:
        """Synchronous wrapper (runs async load in event loop)."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is running, create a new thread
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self._load())
                    result = future.result(timeout=5.0)
            else:
                result = loop.run_until_complete(self._load())
        except Exception:
            result = None
        return result if result is not None else default_state()
    
    def save(self, state: Dict[str, Any]) -> None:
        """Synchronous wrapper (runs async store in event loop)."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self._store(state))
                    future.result(timeout=5.0)
            else:
                loop.run_until_complete(self._store(state))
        except Exception:
            pass
