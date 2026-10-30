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


from __future__ import annotations
import struct

import asyncio
import functools
import json
import os
from typing import Any, Dict, Optional

try:
    import httpx
except Exception:
    httpx = None

TCP_PORT = int(os.getenv("URO_TCP_PORT", "9100"))
HTTP_PORT = int(os.getenv("URO_HTTP_PORT", "8000"))


def _resolve_host(dock_name: str) -> str:
    raw = os.getenv("URO_DOCK_HOSTS", "")
    if raw:
        try:
            mapping = json.loads(raw)
            if dock_name in mapping:
                return str(mapping[dock_name])
        except Exception:
            pass
    return str(dock_name)


def _parse_http_response(data: bytes) -> Dict[str, Any]:
    try:
        head, _, body = data.partition(b"\r\n\r\n")
        lines = head.decode("utf-8", "replace").splitlines()
        status_line = lines[0] if lines else "HTTP/1.1 502 Bad Gateway"
        parts = status_line.split(" ", 2)
        status_code = int(parts[1]) if len(parts) >= 2 else 502

        headers: Dict[str, str] = {}
        for line in lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip().lower()] = value.strip()

        text = body.decode("utf-8", "replace")
        if "json" in headers.get("content-type", ""):
            try:
                parsed: Any = json.loads(text)
            except Exception:
                parsed = text
        else:
            parsed = text

        return {
            "status_code": status_code,
            "headers": headers,
            "body": parsed,
            "transport": "tcp",
        }
    except Exception as exc:
        return {
            "status_code": 502,
            "headers": {},
            "body": f"invalid TCP response: {exc}",
            "transport": "tcp",
        }


async def _tcp_request(dock_name: str, endpoint: str, payload: Any, method: str, headers: Optional[Dict[str, str]], timeout: float):
    host = _resolve_host(dock_name)
    if ":" in host:
        host_name, port_raw = host.split(":", 1)
        port = int(port_raw)
    else:
        host_name = host
        port = TCP_PORT

    # Proper URO Binary Framing
    body = b"" if payload is None else json.dumps(payload).encode("utf-8")
    
    # Build URO Frame: magic(4s) + version(H) + payload_len(I) + flags(H) + reserved(I)
    # Total header size = 4 + 2 + 4 + 2 + 4 = 16 bytes
    MAGIC = b'URO\x01'
    version = 1
    flags = 0
    reserved = 0
    header = struct.pack('<4sHIHI', MAGIC, version, len(body), flags, reserved)
    
    reader, writer = await asyncio.open_connection(host_name, port)
    try:
        # Send framed data
        writer.write(header + body)
        await writer.drain()
        
        # Read response (assume it's also framed, or at least read until close)
        # For simplicity, we read the header first to get the response payload length
        resp_header = await reader.readexactly(16)
        _, _, resp_len, _, _ = struct.unpack('<4sHIHI', resp_header)
        data = await reader.readexactly(resp_len)
        
        # Parse the JSON response
        response = {"status_code": 200, "body": json.loads(data.decode('utf-8'))}
    except Exception as e:
        # Fallback: if the server doesn't respond with a frame, try reading raw
        try:
            raw_data = await reader.read()
            response = {"status_code": 200, "body": raw_data.decode('utf-8', errors='ignore')}
        except:
            raise e
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass

    response = _parse_http_response(data)
    if response["status_code"] >= 400:
        raise ConnectionError(f"TCP transport returned {response['status_code']}: {response['body']}")
    return response


async def _http_request(dock_name: str, endpoint: str, payload: Any, method: str, headers: Optional[Dict[str, str]], timeout: float):
    host = _resolve_host(dock_name)
    if ":" not in host:
        host = f"{host}:{HTTP_PORT}"

    url = f"http://{host}{endpoint}"
    merged_headers = {"Content-Type": "application/json", **(headers or {})}

    if httpx is not None:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(method.upper(), url, json=payload, headers=merged_headers)
            try:
                body: Any = response.json()
            except Exception:
                body = response.text
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": body,
                "transport": "http",
            }

    import urllib.request

    def sync_request():
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, data=data, method=method.upper(), headers=merged_headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read()
                content_type = response.headers.get("Content-Type", "")
                text = raw.decode("utf-8", "replace")
                try:
                    parsed = json.loads(text) if "json" in content_type else text
                except Exception:
                    parsed = text
                return {
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "body": parsed,
                    "transport": "http",
                }
        except Exception as exc:
            status = getattr(exc, "code", 502)
            try:
                raw = exc.read() if hasattr(exc, "read") else str(exc).encode("utf-8")
                body = raw.decode("utf-8", "replace")
            except Exception:
                body = str(exc)
            return {
                "status_code": status,
                "headers": {},
                "body": body,
                "transport": "http",
            }

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, functools.partial(sync_request))


async def send_to_dock_async(
    dock_name: str,
    endpoint: str,
    payload: Any = None,
    method: str = "POST",
    timeout: float = 5.0,
    headers: Optional[Dict[str, str]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Canonical URO inter-dock transport.
    TCP-first on port 9100, HTTP fallback on port 8000.
    """
    last_error: Optional[Exception] = None

    try:
        return await asyncio.wait_for(
            _tcp_request(dock_name, endpoint, payload, method, headers, timeout),
            timeout=timeout,
        )
    except Exception as exc:
        last_error = str(exc) or type(exc).__name__

    try:
        return await asyncio.wait_for(
            _http_request(dock_name, endpoint, payload, method, headers, timeout),
            timeout=timeout,
        )
    except Exception as exc:
        http_error = str(exc) or type(exc).__name__
        raise ConnectionError(
            f"TCP-first transport failed for {dock_name}{endpoint}: tcp={last_error}; http={http_error}"
        ) from exc

# === START: Canonical Additions ===

async def send_to_registry(dock_name: str, payload: dict) -> dict:
    """Canonical registry sender fallback."""
    return await send_to_dock_async("registry", "/registry/register_simple", payload)


async def learn_from_cognitive(dock_id: str, insight: dict) -> dict:
    """Canonical inter-dock learning dispatcher."""
    payload = {
        "intent": "ingest_chaos_insight",
        "source_dock": "chaos",
        "target_dock": dock_id,
        "insight": insight,
        "timestamp": __import__('time').time()
    }
    return await send_to_dock_async("cognitive", "/api/cognitive/beliefs/ingest", payload)


async def send_uro_dispatch(target_dock: str, uro_payload: dict) -> dict:
    """Canonical URO dispatch wrapper."""
    return await send_to_dock_async(target_dock, "/dispatch", uro_payload)

# === END: Canonical Additions ===
