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

import asyncio
import json
from typing import Any, Dict


def install_tcp_listener(app: Any, dock_name: str = "dock", port: int = 9100, host: str = "0.0.0.0") -> Any:
    """
    TCP Universal Listener scaffold.

    Starts an asyncio TCP server on port 9100 that speaks HTTP and bridges
    requests into the FastAPI/ASGI app. This gives docks the same OPAR/FastAPI
    processing path over TCP-first transport, with HTTP remaining as fallback.
    """
    state: Dict[str, Any] = {"server": None, "error": None}

    async def _read_request(reader):
        header_data = b""
        while b"\r\n\r\n" not in header_data:
            chunk = await reader.read(4096)
            if not chunk:
                break
            header_data += chunk

        if not header_data:
            return None

        head, _, rest = header_data.partition(b"\r\n\r\n")
        lines = head.decode("utf-8", "replace").splitlines()
        if not lines:
            return None

        method, path, _ = lines[0].split(" ", 2)
        headers = {}
        for line in lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip().lower()] = value.strip()

        length = int(headers.get("content-length", "0") or 0)
        body = rest
        while len(body) < length:
            chunk = await reader.read(min(4096, length - len(body)))
            if not chunk:
                break
            body += chunk

        return method, path, headers, body[:length]

    async def _handler(reader, writer):
        try:
            request = await asyncio.wait_for(_read_request(reader), timeout=10.0)
            if request is None:
                writer.close()
                return

            method, path, headers, body = request

            try:
                import httpx

                transport = httpx.ASGITransport(app=app)
                async with httpx.AsyncClient(transport=transport, base_url="http://tcp") as client:
                    forwarded_headers = {
                        key: value
                        for key, value in headers.items()
                        if key not in {"content-length", "host"}
                    }
                    response = await client.request(method, path, content=body, headers=forwarded_headers)

                status = response.status_code
                response_headers = dict(getattr(response, "headers", {}))
                response_body = response.content
            except Exception as exc:
                status = 503
                response_headers = {"Content-Type": "application/json"}
                response_body = json.dumps(
                    {
                        "error": "tcp_listener_asgi_bridge_unavailable",
                        "detail": str(exc),
                    }
                ).encode("utf-8")

            reason = {
                200: "OK",
                403: "Forbidden",
                404: "Not Found",
                500: "Internal Server Error",
                502: "Bad Gateway",
                503: "Service Unavailable",
            }.get(status, "OK")

            out_lines = [
                f"HTTP/1.1 {status} {reason}",
                "Connection: close",
                f"Content-Length: {len(response_body)}",
            ]
            for key, value in response_headers.items():
                out_lines.append(f"{key}: {value}")

            writer.write(("\r\n".join(out_lines) + "\r\n\r\n").encode("utf-8") + response_body)
            await writer.drain()
        except Exception:
            pass
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass

    async def _start():
        try:
            state["server"] = await asyncio.start_server(_handler, host, port)
        except Exception as exc:
            state["error"] = str(exc)

    async def _stop():
        server = state.get("server")
        if server is not None:
            server.close()
            try:
                await server.wait_closed()
            except Exception:
                pass

    try:
        app.add_event_handler("startup", _start)
        app.add_event_handler("shutdown", _stop)
    except Exception:
        pass

    try:
        if not hasattr(app.state, "uro_tcp_listeners"):
            app.state.uro_tcp_listeners = []
        app.state.uro_tcp_listeners.append(
            {
                "dock_name": dock_name,
                "port": port,
                "host": host,
                "state": state,
                "protocol": "tcp-first",
                "http_fallback_port": 8000,
            }
        )
    except Exception:
        pass

    return app
