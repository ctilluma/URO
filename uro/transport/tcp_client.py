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
URO-over-TCP Transport Client
High-performance binary transport for dock-to-dock URO exchange.
Replaces HTTP/JSON with persistent TCP connections + msgpack serialization.
"""

import asyncio
import struct
import logging
from typing import Optional, Dict, Any

try:
    import msgpack
    HAS_MSGPACK = True
except ImportError:
    HAS_MSGPACK = False
    import json

logger = logging.getLogger("UROTCPClient")

MAGIC = b'URO\x01'
VERSION = 1
HEADER_SIZE = 16

FLAG_MSGPACK = 0x01
FLAG_JSON = 0x02


class UROTCPError(Exception):
    pass


class ConnectionPool:
    def __init__(self, host: str, port: int, max_connections: int = 5):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self._pool: asyncio.Queue = asyncio.Queue(maxsize=max_connections)
        self._created = 0
        self._lock = asyncio.Lock()

    async def _create_connection(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        self._created += 1
        return reader, writer

    async def acquire(self):
        if not self._pool.empty():
            return await self._pool.get()
        async with self._lock:
            if self._created < self.max_connections:
                return await self._create_connection()
        return await asyncio.wait_for(self._pool.get(), timeout=30.0)

    async def release(self, reader_writer):
        try:
            await asyncio.wait_for(self._pool.put(reader_writer), timeout=1.0)
        except asyncio.TimeoutError:
            reader, writer = reader_writer
            writer.close()
            await writer.wait_closed()
            self._created -= 1

    async def close_all(self):
        while not self._pool.empty():
            try:
                reader, writer = self._pool.get_nowait()
                writer.close()
                await writer.wait_closed()
            except asyncio.QueueEmpty:
                break


class UROTCPClient:
    def __init__(self, max_pool_size: int = 5, request_timeout: float = 30.0):
        self.max_pool_size = max_pool_size
        self.request_timeout = request_timeout
        self._pools: Dict[str, ConnectionPool] = {}
        self._lock = asyncio.Lock()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _get_pool(self, host: str, port: int) -> ConnectionPool:
        key = f"{host}:{port}"
        if key not in self._pools:
            async with self._lock:
                if key not in self._pools:
                    self._pools[key] = ConnectionPool(host, port, self.max_pool_size)
        return self._pools[key]

    def _serialize_payload(self, uro_dict: Dict[str, Any]) -> tuple:
        if HAS_MSGPACK:
            return msgpack.packb(uro_dict, use_bin_type=True), FLAG_MSGPACK
        else:
            return json.dumps(uro_dict).encode('utf-8'), FLAG_JSON

    def _build_frame(self, payload: bytes, flags: int) -> bytes:
        header = struct.pack('<4sHIHI', MAGIC, VERSION, len(payload), flags, 0)
        return header + payload

    def _parse_frame(self, data: bytes) -> Dict[str, Any]:
        if len(data) < HEADER_SIZE:
            raise UROTCPError(f"Frame too short: {len(data)}")
        magic, version, payload_len, flags, reserved = struct.unpack('<4sHIHI', data[:HEADER_SIZE])
        if magic != MAGIC:
            raise UROTCPError(f"Invalid magic: {magic}")
        payload = data[HEADER_SIZE:HEADER_SIZE + payload_len]
        if flags & FLAG_MSGPACK:
            if not HAS_MSGPACK:
                raise UROTCPError("msgpack not available")
            return msgpack.unpackb(payload, raw=False)
        elif flags & FLAG_JSON:
            return json.loads(payload.decode('utf-8'))
        else:
            raise UROTCPError(f"Unknown flags: {flags}")

    async def send_uro(self, host: str, port: int, uro_dict: Dict[str, Any], timeout: Optional[float] = None) -> Dict[str, Any]:
        timeout = timeout or self.request_timeout
        pool = await self._get_pool(host, port)
        payload, flags = self._serialize_payload(uro_dict)
        frame = self._build_frame(payload, flags)
        reader, writer = await pool.acquire()
        try:
            writer.write(frame)
            await writer.drain()
            response_header = await asyncio.wait_for(reader.readexactly(HEADER_SIZE), timeout=timeout)
            _, _, response_len, _, _ = struct.unpack('<4sHIHI', response_header)
            response_payload = await asyncio.wait_for(reader.readexactly(response_len), timeout=timeout)
            return self._parse_frame(response_header + response_payload)
        except asyncio.TimeoutError:
            raise UROTCPError(f"Timeout after {timeout}s to {host}:{port}")
        except Exception as e:
            writer.close()
            await writer.wait_closed()
            pool._created -= 1
            raise UROTCPError(f"Transport error: {e}")
        finally:
            try:
                await pool.release((reader, writer))
            except:
                pass

    async def close(self):
        for pool in self._pools.values():
            await pool.close_all()
        self._pools.clear()
