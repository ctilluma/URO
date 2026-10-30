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
V.A.U.R.O.S. URO NETWORK INTERCEPTOR (v2 - Infra Bypassed)
Enforces URO purity at the network layer. Intercepts dock-to-dock HTTP calls
and routes them through the Coordinator. 
CRITICAL: Infrastructure backends (Redis, Qdrant, Postgres) are BYPASSED.
"""
from uro.transport.inter_dock_client import send_to_dock_async

import httpx
import requests
import os
import logging
from urllib.parse import urlparse

logger = logging.getLogger("URO.Interceptor")

# URO Docks that MUST route through the Coordinator
KNOWN_DOCKS = [
    "cognitive", "memory", "llm_bridge", "query", "coder", "sast", "dast",
    "chaos", "sentinel", "observer", "boardroom", "refinery", "gateway",
    "dns", "iast", "oracle", "aegis", "airlock", "phoenix", "loom",
    "architect", "host_controller"
]

# Infrastructure Backends that docks talk to DIRECTLY (Bypass Interceptor)
INFRASTRUCTURE_BACKENDS = [
    "redis", "qdrant", "postgres", "pg", "mongodb", "mongo",
    "elasticsearch", "kafka", "rabbitmq", "minio", "s3",
    "mysql", "mariadb", "clickhouse", "prometheus", "loki"
]

def is_dock_url(url: str) -> tuple:
    if not url or not isinstance(url, str): return False, None
    try:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
        
        # 1. NEVER intercept infrastructure backends
        for infra in INFRASTRUCTURE_BACKENDS:
            if infra in hostname:
                return False, None
                
        # 2. NEVER intercept the coordinator itself
        if "coordinator" in hostname:
            return False, None
            
        # 3. Check if it's a known URO dock
        for dock in KNOWN_DOCKS:
            if dock in hostname:
                return True, dock
    except Exception:
        pass
    return False, None

# ============================================================================
# PATCH HTTPX (Async)
# ============================================================================
_original_httpx_post = httpx.AsyncClient.post
_original_httpx_get = httpx.AsyncClient.get

async def _patched_httpx_post(self, url, *args, **kwargs):
    is_dock, target_dock = is_dock_url(url)
    if is_dock:
        logger.info(f"[URO Interceptor] ⚡ Redirecting httpx POST {url} -> Coordinator (Target: {target_dock})")
        headers = kwargs.get("headers", {})
        headers["X-URO-Target-Dock"] = target_dock
        headers["X-URO-Original-URL"] = url
        kwargs["headers"] = headers

        parsed = urlparse(url)
        # Smart Coordinator Resolution
        coord_url = os.getenv("COORDINATOR_URL")
        if not coord_url:
            import socket
            for host in ["coordinator", "coordinator_prod", "coordinator_dev", "coordinator_staging"]:
                try:
                    socket.gethostbyname(host)
                    coord_url = f"http://{host}:8000"
                    break
                except socket.gaierror: continue
            if not coord_url: coord_url = "http://coordinator:8000"
            
        new_url = f"{coord_url}{parsed.path}"
        return await _original_httpx_post(self, new_url, *args, **kwargs)
    return await _original_httpx_post(self, url, *args, **kwargs)

async def _patched_httpx_get(self, url, *args, **kwargs):
    is_dock, target_dock = is_dock_url(url)
    if is_dock:
        logger.info(f"[URO Interceptor] ⚡ Redirecting httpx GET {url} -> Coordinator (Target: {target_dock})")
        headers = kwargs.get("headers", {})
        headers["X-URO-Target-Dock"] = target_dock
        headers["X-URO-Original-URL"] = url
        kwargs["headers"] = headers

        parsed = urlparse(url)
        coord_url = os.getenv("COORDINATOR_URL")
        if not coord_url:
            import socket
            for host in ["coordinator", "coordinator_prod", "coordinator_dev", "coordinator_staging"]:
                try:
                    socket.gethostbyname(host)
                    coord_url = f"http://{host}:8000"
                    break
                except socket.gaierror: continue
            if not coord_url: coord_url = "http://coordinator:8000"
            
        new_url = f"{coord_url}{parsed.path}"
        return await _original_httpx_get(self, new_url, *args, **kwargs)
    return await _original_httpx_get(self, url, *args, **kwargs)

# === START: disable_interceptor_monkeypatch ===
# === START: disable_interceptor_monkeypatch ===
# Disabled: All docks now use canonical send_to_dock_async (S9.10)
# httpx.AsyncClient.post = _patched_httpx_post
# httpx.AsyncClient.get = _patched_httpx_get
# === END: disable_interceptor_monkeypatch ===
# === END: disable_interceptor_monkeypatch ===

# ============================================================================
# PATCH REQUESTS (Sync)
# ============================================================================
_original_requests_post = requests.post
_original_requests_get = requests.get

def _patched_requests_post(url, *args, **kwargs):
    is_dock, target_dock = is_dock_url(url)
    if is_dock:
        logger.info(f"[URO Interceptor] ⚡ Redirecting requests POST {url} -> Coordinator (Target: {target_dock})")
        headers = kwargs.get("headers", {})
        headers["X-URO-Target-Dock"] = target_dock
        headers["X-URO-Original-URL"] = url
        kwargs["headers"] = headers

        parsed = urlparse(url)
        coord_url = os.getenv("COORDINATOR_URL")
        if not coord_url:
            import socket
            for host in ["coordinator", "coordinator_prod", "coordinator_dev", "coordinator_staging"]:
                try:
                    socket.gethostbyname(host)
                    coord_url = f"http://{host}:8000"
                    break
                except socket.gaierror: continue
            if not coord_url: coord_url = "http://coordinator:8000"
            
        new_url = f"{coord_url}{parsed.path}"
        return _original_requests_post(new_url, *args, **kwargs)
    return _original_requests_post(url, *args, **kwargs)

def _patched_requests_get(url, *args, **kwargs):
    is_dock, target_dock = is_dock_url(url)
    if is_dock:
        logger.info(f"[URO Interceptor] ⚡ Redirecting requests GET {url} -> Coordinator (Target: {target_dock})")
        headers = kwargs.get("headers", {})
        headers["X-URO-Target-Dock"] = target_dock
        headers["X-URO-Original-URL"] = url
        kwargs["headers"] = headers

        parsed = urlparse(url)
        coord_url = os.getenv("COORDINATOR_URL")
        if not coord_url:
            import socket
            for host in ["coordinator", "coordinator_prod", "coordinator_dev", "coordinator_staging"]:
                try:
                    socket.gethostbyname(host)
                    coord_url = f"http://{host}:8000"
                    break
                except socket.gaierror: continue
            if not coord_url: coord_url = "http://coordinator:8000"
            
        new_url = f"{coord_url}{parsed.path}"
        return _original_requests_get(new_url, *args, **kwargs)
    return _original_requests_get(url, *args, **kwargs)

requests.post = _patched_requests_post
requests.get = _patched_requests_get

def activate():
    logger.info("🛡️ URO Network Interceptor v2 Active. Infra backends bypassed.")

# Auto-activate on import
activate()
