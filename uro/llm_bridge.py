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
Canonical LLM bridge (uro.llm_bridge).

Provides the swarm-wide LLM bridge factory and capability registry used by the
llm_bridge dock's FastAPI surface. Dependency-light and safe to import anywhere.
"""
import inspect
import logging
import time
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger("uro.llm_bridge")


class LLMBridgeCapabilityRegistry:
    """Registry mapping capability names to callables for the LLM bridge."""

    def __init__(self):
        self._handlers: Dict[str, Callable] = {}

    def register(self, name: str, handler: Callable) -> None:
        self._handlers[name] = handler

    def get(self, name: str) -> Optional[Callable]:
        return self._handlers.get(name)

    def names(self):
        return list(self._handlers.keys())

    def __contains__(self, name: str) -> bool:
        return name in self._handlers


class LLMBridge:
    """Bridges LLM requests to registered capabilities (OPAR Act)."""

    def __init__(self, registry: Optional[LLMBridgeCapabilityRegistry] = None, bus=None):
        self.registry = registry or LLMBridgeCapabilityRegistry()
        self.bus = bus
        self.stats = {"ops": 0, "errors": 0, "successes": 0}

    async def execute(self, request: Any = None, context: Optional[Dict] = None,
                      nte: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        self.stats["ops"] += 1
        t0 = time.time()
        try:
            req = request if isinstance(request, dict) else {"raw": request}
            cap_name = req.get("capability") or req.get("cap") or req.get("intent")
            handler = self.registry.get(cap_name) if cap_name else None
            if handler is None:
                return {"status": "success", "capability": cap_name, "routed": False,
                        "registered": self.registry.names(), "echo": req,
                        "latency_ms": (time.time() - t0) * 1000}
            if inspect.iscoroutinefunction(handler):
                result = await handler(req, context, nte)
            else:
                result = handler(req, context, nte)
            self.stats["successes"] += 1
            return {"status": "success", "capability": cap_name, "routed": True,
                    "result": result, "latency_ms": (time.time() - t0) * 1000}
        except Exception as e:
            self.stats["errors"] += 1
            logger.error("LLMBridge.execute error: %s", e)
            return {"status": "error", "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        return {"stats": self.stats, "registered": self.registry.names()}


_bridge_instance: Optional[LLMBridge] = None


def get_llm_bridge(bus=None) -> LLMBridge:
    """Singleton factory for the canonical LLM bridge."""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = LLMBridge(bus=bus)
    return _bridge_instance
