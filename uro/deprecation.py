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
MODULE: Deprecation Lifecycle Tracker
INTENT: Canonical capability for safe refactoring. A deprecated function or
        input format keeps working (backward compatibility) while every use is
        recorded. Self-monitoring then reveals which deprecated items are still
        in use and which have gone quiet and are safe to remove.
STANDARD: URO-STD-0001 - non-fatal, durable, single source of truth.
"""
from __future__ import annotations

import functools
import inspect
import json
import logging
import os
import threading
import time
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger("URO.DEPRECATION")

_STATE_ROOT = os.environ.get("URO_STATE_ROOT", "/opt/uro_state")
_USAGE_FILE = os.path.join(_STATE_ROOT, "deprecation_usage.json")

_lock = threading.Lock()
_registry: Dict[str, Dict[str, Any]] = {}


def _new_record(replacement: str = "", since: str = "", remove_after_days: int = 30) -> Dict[str, Any]:
    return {
        "replacement": replacement, "since": since,
        "remove_after_days": remove_after_days,
        "first_seen": time.time(), "call_count": 0,
        "last_called": None, "last_callers": [], "status": "unused",
    }


def _load() -> None:
    global _registry
    try:
        if os.path.exists(_USAGE_FILE):
            with open(_USAGE_FILE) as f:
                _registry = json.load(f) or {}
    except Exception:
        _registry = {}


def _save() -> None:
    # Durable best-effort; tracking still works in-memory if persistence fails.
    try:
        os.makedirs(_STATE_ROOT, exist_ok=True)
        tmp = _USAGE_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(_registry, f, default=str)
        os.replace(tmp, _USAGE_FILE)
    except Exception as e:
        logger.debug("deprecation usage persist failed (non-fatal): %s", e)


_load()


def _track(key: str, caller: str = "") -> None:
    try:
        with _lock:
            rec = _registry.setdefault(key, _new_record())
            rec["call_count"] = int(rec.get("call_count", 0)) + 1
            rec["last_called"] = time.time()
            rec["status"] = "active"
            if caller:
                rec["last_callers"] = (rec.get("last_callers") or [])[-9:] + [caller]
            _save()
    except Exception:
        pass  # non-fatal: tracking must never break the wrapped call


def deprecated(name: Optional[str] = None, replacement: str = "", since: str = "",
               remove_after_days: int = 30) -> Callable:
    """Mark a function deprecated while keeping it fully functional and backward
    compatible. Every invocation is recorded so the system can later confirm it
    is safe to remove. Works for sync and async functions."""
    def wrap(fn: Callable) -> Callable:
        key = name or f"{fn.__module__}.{fn.__qualname__}"
        with _lock:
            _registry.setdefault(key, _new_record(replacement, since, remove_after_days))
            _save()

        if inspect.iscoroutinefunction(fn):
            @functools.wraps(fn)
            async def ainner(*args, **kwargs):
                _track(key)
                return await fn(*args, **kwargs)
            ainner.__deprecated_key__ = key
            return ainner

        @functools.wraps(fn)
        def inner(*args, **kwargs):
            _track(key)
            return fn(*args, **kwargs)
        inner.__deprecated_key__ = key
        return inner
    return wrap


def register_deprecated(item: str, replacement: str = "", since: str = "",
                        remove_after_days: int = 30) -> None:
    """Register a deprecated input/format/endpoint that is not a wrapped function."""
    try:
        with _lock:
            _registry.setdefault(item, _new_record(replacement, since, remove_after_days))
            _save()
    except Exception:
        pass


def note_deprecated_use(item: str, caller: str = "") -> None:
    """Record that a deprecated input/format was received (keeps it marked active)."""
    _track(item, caller)


def deprecation_health(now: Optional[float] = None) -> Dict[str, Any]:
    """Self-monitoring report. Classifies every deprecated item:
       active   - still being called within its grace window
       dormant  - was called, but silent for >= remove_after_days
       unused   - registered but never called
       removable- dormant + unused (safe to remove)"""
    now = now or time.time()
    out: Dict[str, Any] = {"active": [], "dormant": [], "unused": [], "removable": [], "items": {}}
    try:
        with _lock:
            for key, rec in _registry.items():
                threshold = float(rec.get("remove_after_days", 30))
                last = rec.get("last_called")
                if int(rec.get("call_count", 0)) == 0:
                    cls, quiet = "unused", None
                else:
                    quiet = (now - last) / 86400.0 if last else None
                    cls = "dormant" if (quiet is not None and quiet >= threshold) else "active"
                rec["status"] = cls
                out[cls].append(key)
                if cls in ("dormant", "unused"):
                    out["removable"].append(key)
                out["items"][key] = {
                    "call_count": int(rec.get("call_count", 0)),
                    "last_called": rec.get("last_called"),
                    "quiet_days": round(quiet, 2) if isinstance(quiet, float) else None,
                    "replacement": rec.get("replacement", ""),
                    "status": cls,
                }
            _save()
    except Exception as e:
        out["error"] = str(e)
    return out
