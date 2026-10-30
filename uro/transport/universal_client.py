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
Universal URO-over-TCP Client (send-side for all docks)
Available to all docks via the read-only mount  ./uro/uro -> /opt/uro/uro.
Import:  from uro.transport.universal_client import send_uro_tcp, async_send_uro_tcp

Provides both sync and async interfaces for sending UROs over TCP with:
- Connection pooling (reuses TCP connections)
- msgpack serialization (when available)
- Automatic HTTP fallback on connection failure
- Timeout handling

Usage (sync):
    from uro.transport.universal_client import send_uro_tcp
    result = send_uro_tcp("memory_prod", 9100, {"intent": "memory.store", "payload": {...}})

Usage (async):
    from uro.transport.universal_client import async_send_uro_tcp
    result = await async_send_uro_tcp("memory_prod", 9100, {"intent": "memory.store", "payload": {...}})
"""

import asyncio
import struct
import json
import socket
import logging
import threading
from typing import Dict, Any, Optional, Tuple
from contextlib import contextmanager

logger = logging.getLogger("URO_TCP_Client")

MAGIC = b'URO\x01'
VERSION = 1
HEADER_SIZE = 16
FLAG_MSGPACK = 0x01
FLAG_JSON = 0x02

try:
    import msgpack
    HAS_MSGPACK = True
except ImportError:
    HAS_MSGPACK = False


class _ConnectionPool:
    """Thread-safe connection pool for TCP connections."""
    
    def __init__(self, max_connections: int = 10):
        self._pools: Dict[str, list] = {}
        self._lock = threading.Lock()
        self._max = max_connections
    
    def get(self, host: str, port: int, timeout: float = 5.0) -> socket.socket:
        key = f"{host}:{port}"
        with self._lock:
            pool = self._pools.setdefault(key, [])
            while pool:
                sock = pool.pop()
                try:
                    sock.settimeout(0.1)
                    sock.recv(1, socket.MSG_PEEK)
                    sock.settimeout(timeout)
                    return sock
                except:
                    try:
                        sock.close()
                    except:
                        pass
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            return sock
    
    def put(self, host: str, port: int, sock: socket.socket):
        key = f"{host}:{port}"
        with self._lock:
            pool = self._pools.setdefault(key, [])
            if len(pool) < self._max:
                pool.append(sock)
            else:
                try:
                    sock.close()
                except:
                    pass
    
    def close_all(self):
        with self._lock:
            for pool in self._pools.values():
                for sock in pool:
                    try:
                        sock.close()
                    except:
                        pass
            self._pools.clear()


_sync_pool = _ConnectionPool(max_connections=10)


def _serialize_payload(uro: Dict[str, Any]) -> Tuple[bytes, int]:
    if HAS_MSGPACK:
        return msgpack.packb(uro, use_bin_type=True), FLAG_MSGPACK
    return json.dumps(uro, default=str).encode('utf-8'), FLAG_JSON


def _deserialize_response(data: bytes, flags: int) -> Dict[str, Any]:
    if flags & FLAG_MSGPACK and HAS_MSGPACK:
        return msgpack.unpackb(data, raw=False)
    return json.loads(data.decode('utf-8'))


def _build_frame(payload: bytes, flags: int) -> bytes:
    return struct.pack('<4sHIHI', MAGIC, VERSION, len(payload), flags, 0) + payload


def send_uro_tcp(host: str, port: int, uro: Dict[str, Any], timeout: float = 5.0) -> Dict[str, Any]:
    """
    Send a URO over TCP (sync interface).
    
    Args:
        host: Target dock hostname (e.g., "memory_prod")
        port: Target TCP port (default 9100)
        uro: URO dict with 'intent' and 'payload'
        timeout: Connection and read timeout in seconds
    
    Returns:
        Response dict from the target dock
    
    Raises:
        Exception on connection failure, timeout, or protocol error
    """
    sock = _sync_pool.get(host, port, timeout)
    
    try:
        # Serialize and send
        payload, flags = _serialize_payload(uro)
        frame = _build_frame(payload, flags)
        sock.sendall(frame)
        
        # Read response header
        header = b''
        while len(header) < HEADER_SIZE:
            chunk = sock.recv(HEADER_SIZE - len(header))
            if not chunk:
                raise ConnectionError("Connection closed by peer")
            header += chunk
        
        magic, version, resp_len, resp_flags, _ = struct.unpack('<4sHIHI', header)
        if magic != MAGIC:
            raise ValueError(f"Invalid magic: {magic}")
        
        # Read response payload
        resp_data = b''
        while len(resp_data) < resp_len:
            chunk = sock.recv(resp_len - len(resp_data))
            if not chunk:
                raise ConnectionError("Connection closed by peer")
            resp_data += chunk
        
        # Deserialize and return
        response = _deserialize_response(resp_data, resp_flags)
        
        # Return connection to pool
        _sync_pool.put(host, port, sock)
        
        return response
    
    except Exception:
        # Don't return broken connection to pool
        try:
            sock.close()
        except:
            pass
        raise


class _AsyncConnectionPool:
    """Async connection pool for TCP connections."""
    
    def __init__(self, max_connections: int = 10):
        self._pools: Dict[str, list] = {}
        self._lock = asyncio.Lock()
        self._max = max_connections
    
    async def get(self, host: str, port: int, timeout: float = 5.0):
        key = f"{host}:{port}"
        async with self._lock:
            pool = self._pools.setdefault(key, [])
            while pool:
                reader, writer = pool.pop()
                try:
                    # Quick health check
                    writer.write(b'')
                    await writer.drain()
                    return reader, writer
                except:
                    try:
                        writer.close()
                        await writer.wait_closed()
                    except:
                        pass
            
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=timeout
            )
            return reader, writer
    
    async def put(self, host: str, port: int, reader, writer):
        key = f"{host}:{port}"
        async with self._lock:
            pool = self._pools.setdefault(key, [])
            if len(pool) < self._max:
                pool.append((reader, writer))
            else:
                try:
                    writer.close()
                    await writer.wait_closed()
                except:
                    pass
    
    async def close_all(self):
        async with self._lock:
            for pool in self._pools.values():
                for reader, writer in pool:
                    try:
                        writer.close()
                        await writer.wait_closed()
                    except:
                        pass
            self._pools.clear()


_async_pool = _AsyncConnectionPool(max_connections=10)


async def async_send_uro_tcp(host: str, port: int, uro: Dict[str, Any], timeout: float = 5.0) -> Dict[str, Any]:
    """
    Send a URO over TCP (async interface).
    
    Args:
        host: Target dock hostname (e.g., "memory_prod")
        port: Target TCP port (default 9100)
        uro: URO dict with 'intent' and 'payload'
        timeout: Connection and read timeout in seconds
    
    Returns:
        Response dict from the target dock
    
    Raises:
        Exception on connection failure, timeout, or protocol error
    """
    reader, writer = await _async_pool.get(host, port, timeout)
    
    try:
        # Serialize and send
        payload, flags = _serialize_payload(uro)
        frame = _build_frame(payload, flags)
        writer.write(frame)
        await writer.drain()
        
        # Read response header
        header = await asyncio.wait_for(reader.readexactly(HEADER_SIZE), timeout=timeout)
        magic, version, resp_len, resp_flags, _ = struct.unpack('<4sHIHI', header)
        if magic != MAGIC:
            raise ValueError(f"Invalid magic: {magic}")
        
        # Read response payload
        resp_data = await asyncio.wait_for(reader.readexactly(resp_len), timeout=timeout)
        
        # Deserialize and return
        response = _deserialize_response(resp_data, resp_flags)
        
        # Return connection to pool
        await _async_pool.put(host, port, reader, writer)
        
        return response
    
    except Exception:
        # Don't return broken connection to pool
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass
        raise


def cleanup_pools():
    """Close all pooled connections (call on shutdown)."""
    _sync_pool.close_all()
    # For async pool, use in an async context


# ===========================================================================
# Route-cached TCP transport — "learn the route once, then go direct"
# The coordinator acts as a route oracle on first contact; the route is then
# cached and reused for direct TCP sends. On failure/timeout the cache entry
# is invalidated and the coordinator is re-queried.
# ===========================================================================
import os as _os
import time as _time


class RouteEntry:
    __slots__ = ("dock", "endpoint", "tcp_port", "http_port", "method", "expires_at")

    def __init__(self, dock, endpoint, tcp_port=9100, http_port=8000,
                 method="POST", ttl=300):
        self.dock = dock
        self.endpoint = endpoint
        self.tcp_port = tcp_port
        self.http_port = http_port
        self.method = method
        self.expires_at = _time.time() + ttl

    def expired(self) -> bool:
        return _time.time() > self.expires_at


class RouteCache:
    """Caches intent -> (dock, endpoint) routes resolved via the coordinator oracle."""

    def __init__(self, coordinator_host: Optional[str] = None,
                 coordinator_http_port: int = 8000):
        env = _os.getenv("AURA_ENV", "prod")
        self._coord_host = coordinator_host or f"coordinator_{env}"
        self._coord_port = coordinator_http_port
        self._cache: Dict[str, RouteEntry] = {}
        self._lock = asyncio.Lock()
        self._http = None

    async def _client(self):
        if self._http is None:
            import httpx
            self._http = httpx.AsyncClient(timeout=5.0)
        return self._http

    async def resolve(self, intent: str) -> Optional[RouteEntry]:
        async with self._lock:
            entry = self._cache.get(intent)
            if entry is not None and not entry.expired():
                return entry
        # Cache miss / expired -> ask the Nexus routing fabric
        try:
            env = _os.getenv("AURA_ENV", "prod")
            nexus_host = f"nexus_{env}"
            client = await self._client()
            url = f"http://{nexus_host}:8000/nexus/resolve"
            resp = await client.post(url, json={"intent": intent})
            if resp.status_code == 200:
                d = resp.json()
                if d.get("status") == "resolved" and d.get("dock"):
                    entry = RouteEntry(
                        d["dock"], d["endpoint"],
                        d.get("tcp_port", 9100), d.get("http_port", 8000),
                        d.get("method", "POST"), d.get("ttl", 300),
                    )
                    async with self._lock:
                        self._cache[intent] = entry
                    logger.info(f"[RouteCache] learned route for '{intent}' -> "
                                f"{entry.dock}{entry.endpoint} (source: {d.get('source', 'registry')})")
                    return entry
        except Exception as e:
            logger.debug(f"[RouteCache] Nexus resolve failed for '{intent}': {e}")
        return None

    def invalidate(self, intent: str) -> None:
        self._cache.pop(intent, None)
        logger.debug(f"[RouteCache] invalidated route for '{intent}'")

    async def close(self):
        if self._http:
            await self._http.aclose()
            self._http = None


_route_cache = RouteCache()


def _dock_host(dock: str) -> str:
    """Resolve a logical dock name to its container hostname (adds env suffix)."""
    env = _os.getenv("AURA_ENV", "prod")
    if dock.endswith(f"_{env}"):
        return dock
    return f"{dock}_{env}"


async def send_uro_routed(intent: str, payload: Dict[str, Any],
                          timeout: float = 5.0) -> Dict[str, Any]:
    """
    Route-cached TCP send. Bypasses the coordinator once the route is learned.

    Flow:
      1. Resolve route from cache, or query the coordinator oracle on first use.
      2. Send DIRECT over TCP to the resolved dock+endpoint.
      3. On failure/timeout: invalidate the cached route, re-resolve, retry TCP once.
      4. Final fallback: HTTP direct to the dock endpoint.
    """
    last_err = None
    for _attempt in range(2):  # initial attempt + one retry after invalidation
        route = await _route_cache.resolve(intent)
        if route is None:
            break
        try:
            uro = {"intent": route.endpoint, "payload": payload}
            resp = await async_send_uro_tcp(_dock_host(route.dock), route.tcp_port, uro, timeout=timeout)
            if resp.get("status") == "ok" or resp.get("http_status") is not None:
                resp = dict(resp)
                resp["transport"] = "tcp_direct"
                return resp
            _route_cache.invalidate(intent)
            last_err = resp.get("error", "non-ok response")
        except Exception as e:
            _route_cache.invalidate(intent)
            last_err = str(e)

    # Fallback: HTTP direct to the dock endpoint (route known)
    route = await _route_cache.resolve(intent)
    if route is not None:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=timeout) as client:
                url = f"http://{_dock_host(route.dock)}:{route.http_port}{route.endpoint}"
                r = await client.post(url, json=payload)
                try:
                    body = r.json()
                except Exception:
                    body = {"raw": r.text[:500]}
                return {"status": "ok" if r.status_code < 400 else "error",
                        "http_status": r.status_code, "transport": "http_direct",
                        "dock": route.dock, "path": route.endpoint, "result": body}
        except Exception as e:
            last_err = str(e)

    return {"status": "error", "error": f"no route or all transports failed: {last_err}"}

# Compatibility export (fix for ImportError in inter_dock_client.py)
HAS_TCP_TRANSPORT = True
