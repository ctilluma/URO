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
V.A.U.R.O.S. COORDINATOR BUS (Canonical URO Version)
Keeps the FULL original API (emit, register_capabilities, retrieve_memory,
store_memory, query_cognitive, request_llm, emit_uro_and_await, etc.) and
layers canonical URO integration on top:

  * Every emission creates/updates a Synapse Vector URO (per-topic trust).
  * The synapse load is the COMBINATION of both endpoints' NTE states
    (native crossed with current, shared between the two).
  * Every emission records a custody event.
  * UROs carry NTE state and INAHASH seals.

Downstream LLMs: do NOT remove methods here. Docks depend on the full API.
"""
from __future__ import annotations
import traceback

import os, asyncio, logging, socket, time
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

from uro.canonical_integration import (
    create_dock_uro,
    establish_synapse,
    record_dock_custody,
    CanonicalUROHelper,
)

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
from uro.base import Quadrant, OPARPhase
from uro.cognition.myelination import record_synapse_use


# URO-over-TCP transport (universal client, available via /opt/uro mount)
try:
    from uro.transport.universal_client import async_send_uro_tcp
    HAS_TCP_TRANSPORT = True
except Exception as _tcp_import_err:
    HAS_TCP_TRANSPORT = False
    async_send_uro_tcp = None

logger = logging.getLogger("CoordinatorBus")


def generate_urid() -> str:
    import hashlib
    return hashlib.blake2b(os.urandom(64)).hexdigest()[:32]


def get_coordinator_url() -> str:
    url = os.getenv("COORDINATOR_URL")
    if url:
        return url
    for host in ["coordinator", "coordinator_prod", "coordinator_dev", "coordinator_staging"]:
        try:
            socket.gethostbyname(host)
            return f"http://{host}:8000"
        except socket.gaierror:
            continue
    return "http://coordinator:8000"


# --- Original request models (docks depend on these) ---
class MemoryRetrieveURO(BaseModel):
    urid1_source: str = ""
    urid2_instance: str = Field(default_factory=generate_urid)
    intent: str = "memory.retrieve"
    key: str = ""
    vector_hash: str = ""
    query_tensor: List[float] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemoryStoreURO(BaseModel):
    urid1_source: str = ""
    urid2_instance: str = Field(default_factory=generate_urid)
    intent: str = "memory.store"
    key: str = ""
    entity: str = ""
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    ttl: Optional[int] = None


class CognitiveQueryURO(BaseModel):
    urid1_source: str = ""
    urid2_instance: str = Field(default_factory=generate_urid)
    intent: str = "cognitive.query"
    query: str = ""
    context: Dict[str, Any] = Field(default_factory=dict)
    vector_embedding: Optional[List[float]] = None


class LLMRequestURO(BaseModel):
    urid1_source: str = ""
    urid2_instance: str = Field(default_factory=generate_urid)
    intent: str = "llm.synthesize"
    user_prompt: str = ""
    context: Dict[str, Any] = Field(default_factory=dict)
    model_preference: Optional[str] = None


class CapabilityRegistrationURO(BaseModel):
    urid1_source: str = ""
    urid2_instance: str = Field(default_factory=generate_urid)
    intent: str = "coordinator.register_capability"
    dock_name: str = ""
    capabilities: List[str] = Field(default_factory=list)
    dock_endpoint: str = ""
    version: str = "1.0.0"


class GenericURO(BaseModel):
    urid1_source: str = ""
    urid2_instance: str = ""
    intent: str = ""
    payload: Dict[str, Any] = {}
    target_dock: str = ""
    source_dock: str = ""
    timestamp: float = 0.0
    opar_phase: str = "observe"
    quad_capability: str = "base"
    nte_vector: Dict[str, float] = {}
    topic: str = "general"

    def __init__(self, **data):
        if "timestamp" not in data or data.get("timestamp", 0.0) == 0.0:
            data["timestamp"] = time.time()
        super().__init__(**data)


class CoordinatorBus:
# === START: tcp_first_coord_init ===
    def __init__(self, dock_name: str):
        self.dock_name = dock_name
        self.coordinator_url = get_coordinator_url()
        self.client = _CanonicalTransportWrapper(timeout=30.0)
# === END: tcp_first_coord_init ===
        self._registered = False
        self._helper = CanonicalUROHelper(dock_name=dock_name)
        self._synapses: Dict[str, Any] = {}
        logger.info(f"🚌 CoordinatorBus initialized for {dock_name} -> {self.coordinator_url}")
        
        # TCP transport state
        self._tcp_port = 9100
        self._tcp_failed_cache = {}  # dock -> timestamp of last TCP failure
        self._tcp_failure_ttl = 60  # seconds before retrying a failed dock

    # --- Canonical integration helpers ---

    def register(self, *args):
        """Register a capability/domain/instance with the bus.
        
        Accepts flexible signatures:
        - register(instance)
        - register(name, instance)
        - register(dock_name, cap_name, execute_fn)
        """
        if not hasattr(self, '_registry'):
            self._registry = {}
        
        if len(args) == 1:
            # register(instance)
            instance = args[0]
            name = getattr(instance, '__class__', type(instance)).__name__
            self._registry[name] = instance
        elif len(args) == 2:
            # register(name, instance)
            name, instance = args
            self._registry[name] = instance
        elif len(args) >= 3:
            # register(dock_name, cap_name, execute_fn)
            key = f"{args[0]}.{args[1]}" if len(args) >= 2 else args[0]
            self._registry[key] = args[2] if len(args) >= 3 else args[1]
        
        self._registered = True
        return True

    def _ensure_synapse(self, target_dock: str, topic: str):
        """Create/cache a synapse with combined load from both endpoints."""
        key = f"{self.dock_name}->{target_dock}:{topic}"
        if key not in self._synapses:
            self_uro = self._helper.create_uro(payload={"dock_name": self.dock_name})["base"]
            tgt_data = create_dock_uro(dock_name=target_dock, payload={"dock_name": target_dock})
            tgt_uro = tgt_data["base"]
            self._synapses[key] = establish_synapse(
                self.dock_name, target_dock, self_uro, tgt_uro,
                topic=topic,
                endpoint1_nte=self._helper.create_uro(payload={}).get("nte_state", {}),
                endpoint2_nte=tgt_data.get("nte_state", {}),
            )
        return self._synapses[key]

    def _record_emission_custody(self, phase: str = OPARPhase.OBSERVE):
        uro_data = self._helper.create_uro(payload={"dock_name": self.dock_name})
        if isinstance(uro_data, dict):
            uro_data.setdefault("custody_chain", [])
            uro_data.setdefault("urid", "unknown")
            uro_data.setdefault("inahash", "")
            uro_data.setdefault("source", "unknown")
            uro_data.setdefault("nte_state", {})
        try:
            if isinstance(uro_data, dict):
                uro_data.setdefault("custody_chain", [])
                uro_data.setdefault("urid", "unknown")
                uro_data.setdefault("inahash", "")
                uro_data.setdefault("source", "unknown")
                uro_data.setdefault("nte_state", {})
            try:
                if isinstance(uro_data, dict):
                    uro_data.setdefault("custody_chain", [])
                    uro_data.setdefault("urid", "unknown")
                    uro_data.setdefault("inahash", "")
                    uro_data.setdefault("source", "unknown")
                    uro_data.setdefault("nte_state", {})
                try:
                    if isinstance(uro_data, dict):
                        uro_data.setdefault("custody_chain", [])
                        uro_data.setdefault("urid", "unknown")
                        uro_data.setdefault("inahash", "")
                        uro_data.setdefault("source", "unknown")
                        uro_data.setdefault("nte_state", {})
                    try:
                        self._helper.record_custody(uro_data, phase, {"dopamine": 50.0})
                    except Exception as _ce:
                        logger.warning("[CoordinatorBus] custody recording skipped (non-fatal): %s", _ce)
                except Exception as _ce:
                    logger.warning("[CoordinatorBus] custody recording skipped (non-fatal): %s", _ce)
            except Exception as _ce:
                logger.warning("[CoordinatorBus] custody recording skipped (non-fatal): %s", _ce)
        except Exception as _ce:
            logger.warning("[CoordinatorBus] custody recording skipped (non-fatal): %s", _ce)
        return uro_data

    # --- Original API (preserved) ---

    def _resolve_dock_hostname(self, target_dock: str) -> str:
        """Map logical dock name to container hostname."""
        import os
        env = os.getenv("AURA_ENV", "prod")
        if target_dock.endswith(f"_{env}"):
            return target_dock
        return f"{target_dock}_{env}"

    def _is_tcp_cached_failure(self, dock: str) -> bool:
        """Check if dock recently failed TCP (within TTL)."""
        import time
        if dock in self._tcp_failed_cache:
            if time.time() - self._tcp_failed_cache[dock] < self._tcp_failure_ttl:
                return True
            del self._tcp_failed_cache[dock]
        return False

    def _cache_tcp_failure(self, dock: str):
        """Cache a TCP failure for this dock."""
        import time
        self._tcp_failed_cache[dock] = time.time()

    async def _emit_via_tcp(self, uro, target_dock: str):
        """Emit URO via TCP directly to target dock. Returns dict or None."""
        if not HAS_TCP_TRANSPORT or async_send_uro_tcp is None:
            return None
        
        hostname = self._resolve_dock_hostname(target_dock)
        
        if self._is_tcp_cached_failure(hostname):
            return None
        
        try:
            uro_dict = uro.dict() if hasattr(uro, 'dict') else uro
            logger.debug(f"[{self.dock_name}] TCP emit -> {hostname}:{self._tcp_port}")
            response = await async_send_uro_tcp(hostname, self._tcp_port, uro_dict, timeout=3.0)
            if response.get("status") == "ok":
                return response
            else:
                logger.warning(f"[{self.dock_name}] TCP emit returned non-ok: {response.get('error')}")
                self._cache_tcp_failure(hostname)
                return None
        except Exception as e:
            logger.debug(f"[{self.dock_name}] TCP emit failed to {hostname}: {e}")
            self._cache_tcp_failure(hostname)
            return None

    async def close(self):
        """Clean up transport resources. (Universal client manages its own pool.)"""
        pass

    async def emit(self, uro: BaseModel) -> Optional[Dict[str, Any]]:
        try:
            if hasattr(uro, 'urid1_source') and not uro.urid1_source:
                uro.urid1_source = self.dock_name
            
            # Try TCP transport first (universal, no manual enable needed)
            target_dock = getattr(uro, 'target_dock', None)
            if target_dock:
                tcp_result = await self._emit_via_tcp(uro, target_dock)
                if tcp_result is not None:
                    return tcp_result
                # Fall through to HTTP if TCP failed
            
            # HTTP fallback (original path through coordinator)
            res = await self.client.post(f"{self.coordinator_url}/uro/ingest", json=uro.dict())
            if res.status_code == 200:
                return res.json()
            else:
                logger.warning(f"Coordinator returned {res.status_code}: {res.text}")
                return None
        except Exception as e:
            logger.error(f"CoordinatorBus emission failed: {e}")
            return None

    async def emit_uro(self, intent: str, payload: Dict[str, Any] = None,
                       target_dock: str = "", topic: str = "general", **kwargs) -> Optional[Dict[str, Any]]:
        try:
            if target_dock:
                syn = self._ensure_synapse(target_dock, topic)
            self._record_emission_custody()
            uro = GenericURO(
                intent=intent,
                payload=payload or {},
                target_dock=target_dock,
                source_dock=self.dock_name,
                urid1_source=self.dock_name,
                topic=topic,
                **kwargs
            )
            start_time = time.perf_counter()
            result = await self.emit(uro)
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            
            if target_dock:
                outcome = {
                    "success": result is not None,
                    "latency_ms": latency_ms,
                    "intent": intent,
                    "topic": topic,
                }
                syn = self._synapses.get(f"{self.dock_name}->{target_dock}:{topic}")
                self._modulate_synapse_obj(syn, outcome)
            
            if getattr(self, '_durable_engine', None):
                try: self._durable_engine.commit_uro_transition(uro.urid if hasattr(uro, 'urid') else str(uro), 'emit', data=payload)
                except Exception: pass
            return result if result is not None else {"status": "no_response"}
        except Exception as e:
            logger.error(f"[CoordinatorBus] emit_uro error: {e}")
            return {"status": "error", "message": str(e)}

    async def register_capabilities(self, capabilities: List[str], endpoint: str):
        reg_uro = CapabilityRegistrationURO(
            urid1_source=self.dock_name, dock_name=self.dock_name,
            capabilities=capabilities, dock_endpoint=endpoint
        )
        result = await self.emit(reg_uro)
        if result:
            self._registered = True
            logger.info(f"✅ {self.dock_name} registered {len(capabilities)} capabilities")
        else:
            logger.error(f"❌ {self.dock_name} capability registration failed")
        return result

    async def retrieve_memory(self, key: str = "", vector_hash: str = "", query_tensor: List[float] = None) -> Optional[Dict]:
        return await self.emit(MemoryRetrieveURO(urid1_source=self.dock_name, key=key, vector_hash=vector_hash, query_tensor=query_tensor or []))

    async def store_memory(self, key: str, data: Dict, entity: str = "", ttl: int = None) -> Optional[Dict]:
        return await self.emit(MemoryStoreURO(urid1_source=self.dock_name, key=key, entity=entity, data=data, ttl=ttl))

    async def query_cognitive(self, query: str, context: Dict = None) -> Optional[Dict]:
        return await self.emit(CognitiveQueryURO(urid1_source=self.dock_name, query=query, context=context or {}))

    async def request_llm(self, prompt: str, context: Dict = None, model: str = None) -> Optional[Dict]:
        return await self.emit(LLMRequestURO(urid1_source=self.dock_name, user_prompt=prompt, context=context or {}, model_preference=model))

    def _safe_record_use(self, obj, *args, **kwargs):
        """Non-fatal usage bookkeeping: tolerate None/missing receivers."""
        try:
            if obj is None:
                return None
            fn = getattr(obj, "record_use", None)
            if fn is None:
                return None
            return fn(*args, **kwargs)
        except Exception as _ru:
            logger.warning("[CoordinatorBus] record_use skipped (non-fatal): %s", _ru)
            return None

    def _modulate_synapse_obj(self, syn, outcome: dict):
        """Bidirectional 24-axis modulation with deferred I/O and legacy fallback."""
        try:
            if syn is None:
                return
            # Attempt modern 24-axis modulation
            if hasattr(syn, "record_interaction"):
                syn.record_interaction(outcome)
            else:
                # Legacy fallback for older docks during swarm-wide rollout
                self._safe_record_use(syn, bool(outcome.get("success", False)))
            
            # Deferred I/O: mark dirty to avoid blocking the async event loop
            try:
                from uro.synapse.persistence import mark_dirty
                mark_dirty(syn)
            except Exception:
                pass # Persistence unavailable or failed
        except Exception as _me:
            logger.debug("[CoordinatorBus] synapse modulation skipped (non-fatal): %s", _me)

    async def emit_uro_and_await(self, intent: str, payload: Dict[str, Any] = None,
                                  target_dock: str = "", timeout: float = 30.0,
                                  topic: str = "general", **kwargs) -> Optional[Dict[str, Any]]:
        correlation_id = kwargs.get('urid2_instance') or generate_urid()
        response_future = asyncio.get_event_loop().create_future()
        if not hasattr(self, '_pending_responses'):
            self._pending_responses = {}
        self._pending_responses[correlation_id] = response_future

        try:
            if target_dock:
                self._ensure_synapse(target_dock, topic)
            self._record_emission_custody()

            uro = GenericURO(
                intent=intent,
                payload=payload or {},
                target_dock=target_dock,
                source_dock=self.dock_name,
                urid1_source=self.dock_name,
                urid2_instance=correlation_id,
                topic=topic,
                **kwargs
            )
            start_time = time.perf_counter()
            emit_result = await self.emit(uro)
            if not emit_result:
                logger.error(f"[CoordinatorBus] Failed to emit URO for {intent}")
                return None

            try:
                response = await asyncio.wait_for(response_future, timeout=timeout)
                latency_ms = (time.perf_counter() - start_time) * 1000.0
                if target_dock and (f"{self.dock_name}->{target_dock}:{topic}" in self._synapses):
                    syn = self._synapses[f"{self.dock_name}->{target_dock}:{topic}"]
                    outcome = {"success": True, "latency_ms": latency_ms, "intent": intent, "topic": topic}
                    self._modulate_synapse_obj(syn, outcome)
                    record_synapse_use(getattr(syn, "synapse_urid", None).to_hex(), True)
                return response
            except asyncio.TimeoutError:
                latency_ms = (time.perf_counter() - start_time) * 1000.0
                logger.warning(f"[CoordinatorBus] Timeout for {intent} ({correlation_id})")
                if target_dock and (f"{self.dock_name}->{target_dock}:{topic}" in self._synapses):
                    syn = self._synapses[f"{self.dock_name}->{target_dock}:{topic}"]
                    outcome = {"success": False, "latency_ms": latency_ms, "intent": intent, "topic": topic}
                    self._modulate_synapse_obj(syn, outcome)
                    if (syn_urid := getattr(syn, "synapse_urid", None)) is not None:
                        record_synapse_use(syn_urid.to_hex(), False)
                return None
            finally:
                self._pending_responses.pop(correlation_id, None)
        except Exception as e:
            if isinstance(e, (asyncio.TimeoutError, TimeoutError)):
                logger.warning("[CoordinatorBus] emit_uro_and_await timeout (non-fatal; caller fallback engaged): %s", e)
                return None
            if isinstance(e, (asyncio.TimeoutError, TimeoutError, asyncio.CancelledError)):
                logger.warning("[CoordinatorBus] emit_uro_and_await timeout (degraded; caller fallback engaged)")
            elif isinstance(e, (AttributeError, KeyError, TypeError)):
                logger.warning("[CoordinatorBus] emit_uro_and_await degraded (data-shape; caller fallback engaged): %r", e)
            else:
                logger.error(f"[CoordinatorBus] emit_uro_and_await error: {e}")
            logger.warning("[CoordinatorBus] TRACEBACK-INSTRUMENTED:\n" + traceback.format_exc())  # TRACEBACK-INSTRUMENTED
            if hasattr(self, '_pending_responses'):
                self._pending_responses.pop(correlation_id, None)
            return None

    def resolve_pending_response(self, correlation_id: str, response: Dict[str, Any]):
        if hasattr(self, '_pending_responses') and correlation_id in self._pending_responses:
            future = self._pending_responses[correlation_id]
            if not future.done():
                future.set_result(response)

    async def close(self):
        await self.client.aclose()

    async def register_capability(self, capability: str, dock: str = None) -> dict:
        dock_name = dock or self.dock_name
        try:
            return await self.emit_uro(
                intent="coordinator.register_capability",
                payload={"capability": capability, "dock_name": dock_name},
                target_dock="coordinator",
                topic="capability_registration"
            )
        except Exception as e:
            print(f"[CoordinatorBus] Warning: Could not register {capability}: {e}")
            return {"status": "error", "message": str(e)}


async def initialize_dock_with_coordinator(dock_name: str, capabilities: List[str], endpoint: str) -> CoordinatorBus:
    bus = CoordinatorBus(dock_name)
    await bus.register_capabilities(capabilities, endpoint)
    async def _periodic_registration():
        while True:
            await asyncio.sleep(300)
            await bus.register_capabilities(capabilities, endpoint)
    asyncio.create_task(_periodic_registration())
    return bus


# === CANONICAL ADAPTER: dock-facing bus methods (Fractal URO Mandate) ===
def _bus_store_me(self, *args, **kwargs):
    """Canonical adapter for dock store_me requests."""
    if hasattr(self, 'publish'):
        return self.publish("store_me", *args, **kwargs)
    return None

def _bus_emit_uro(self, *args, **kwargs):
    """Canonical adapter for dock emit_uro requests."""
    if hasattr(self, 'publish'):
        return self.publish("emit_uro", *args, **kwargs)
    return None

CoordinatorBus.store_me = _bus_store_me
CoordinatorBus.emit_uro = _bus_emit_uro

# --- Convergence compatibility exports (auto-generated) ---
# compat:DEFERRED
try:
    from uro.exchange.receipt import ReceiptMode as _RM
    DEFERRED = getattr(_RM, "DEFERRED", "DEFERRED")
except Exception:
    DEFERRED = "DEFERRED"
# compat:FULFILLED
try:
    from uro.exchange.receipt import ReceiptMode as _RM
    FULFILLED = getattr(_RM, "FULFILLED", "FULFILLED")
except Exception:
    FULFILLED = "FULFILLED"
# compat:INCAPABLE
try:
    from uro.exchange.receipt import ReceiptMode as _RM
    INCAPABLE = getattr(_RM, "INCAPABLE", "INCAPABLE")
except Exception:
    INCAPABLE = "INCAPABLE"
# compat:Receipt
try:
    from uro.receipt import Receipt
except Exception:
    Receipt = None
