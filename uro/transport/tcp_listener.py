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
URO-over-TCP Transport Listener
Async TCP server that receives URO frames and processes them.
"""

import asyncio
import struct
import logging
from typing import Callable, Awaitable, Dict, Any

try:
    import msgpack
    HAS_MSGPACK = True
except ImportError:
    HAS_MSGPACK = False
    import json

logger = logging.getLogger("UROTCPListener")

MAGIC = b'URO\x01'
VERSION = 1
HEADER_SIZE = 16

FLAG_MSGPACK = 0x01
FLAG_JSON = 0x02


class UROTCPError(Exception):
    pass


class UROTCPListener:
    def __init__(self, process_uro: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]], host: str = "0.0.0.0", port: int = 9100):
        self.process_uro = process_uro
        self.host = host
        self.port = port
        self._server = None

    def _parse_frame(self, data: bytes) -> Dict[str, Any]:
        if len(data) < HEADER_SIZE:
            raise UROTCPError(f"Frame too short")
        magic, version, payload_len, flags, reserved = struct.unpack('<4sHIHI', data[:HEADER_SIZE])
        if magic != MAGIC:
            raise UROTCPError(f"Invalid magic")
        payload = data[HEADER_SIZE:HEADER_SIZE + payload_len]
        if flags & FLAG_MSGPACK:
            if not HAS_MSGPACK:
                raise UROTCPError("msgpack not available")
            return msgpack.unpackb(payload, raw=False)
        elif flags & FLAG_JSON:
            return json.loads(payload.decode('utf-8'))
        else:
            raise UROTCPError(f"Unknown flags")

    def _build_frame(self, payload: bytes, flags: int) -> bytes:
        header = struct.pack('<4sHIHI', MAGIC, VERSION, len(payload), flags, 0)
        return header + payload

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        logger.debug(f"TCP connection from {addr}")
        try:
            while True:
                try:
                    header = await reader.readexactly(HEADER_SIZE)
                except asyncio.IncompleteReadError:
                    break
                _, _, payload_len, _, _ = struct.unpack('<4sHIHI', header)
                payload = await reader.readexactly(payload_len)
                uro_dict = self._parse_frame(header + payload)
                try:
                    response_dict = await self.process_uro(uro_dict)
                except Exception as e:
                    logger.error(f"URO processing error: {e}")
                    response_dict = {"status": "error", "error": str(e)}
                if HAS_MSGPACK:
                    response_payload = msgpack.packb(response_dict, use_bin_type=True)
                    response_flags = FLAG_MSGPACK
                else:
                    response_payload = json.dumps(response_dict).encode('utf-8')
                    response_flags = FLAG_JSON
                writer.write(self._build_frame(response_payload, response_flags))
                await writer.drain()
        except Exception as e:
            logger.error(f"Error handling client {addr}: {e}")
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except:
                pass

    async def start(self):
        self._server = await asyncio.start_server(self._handle_client, self.host, self.port)
        logger.info(f"URO TCP listener started on {self.host}:{self.port}")

    async def stop(self):
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            logger.info("URO TCP listener stopped")

    async def serve_forever(self):
        await self.start()
        async with self._server:
            await self._server.serve_forever()
