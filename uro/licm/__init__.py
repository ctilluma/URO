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


"""V.A.U.R.O.S. Loom Integration Capability Manifest (LICM) Core."""
from __future__ import annotations
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

class LicmUnmeasured(Exception):
    """Raised when a dock cannot provide a real metric (prevents fabrication)."""
    pass

@dataclass
class ViewDefinition:
    name: str
    description: str
    metrics: List[str] = field(default_factory=list)
    controls: List[str] = field(default_factory=list)

@dataclass
class LICMManifest:
    dock_id: str
    menu_label: str
    icon: str
    color_accent: str
    one_line_pitch: str
    views: List[ViewDefinition] = field(default_factory=list)
    ws_channel: str = ""

    def __post_init__(self):
        if not self.ws_channel:
            self.ws_channel = f"{self.dock_id}_events"

@dataclass
class ProvenanceTag:
    value: Any
    source: str = "LIVE"
    derivation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "provenance": self.source,
            "derivation": self.derivation if self.source == "DERIVED" else None,
            "timestamp": time.time()
        }

def tag_live(value: Any) -> ProvenanceTag:
    return ProvenanceTag(value=value, source="LIVE")

def tag_derived(value: Any, derivation: str) -> ProvenanceTag:
    return ProvenanceTag(value=value, source="DERIVED", derivation=derivation)

def tag_unmeasured(reason: str) -> ProvenanceTag:
    return ProvenanceTag(value=None, source="UNMEASURED", derivation=reason)

@dataclass
class LICMProvider:
    status: Callable[[], Dict[str, ProvenanceTag]]
    events_source: Callable[[int], List[Dict[str, Any]]]
    actions: Dict[str, Callable[[Dict[str, Any]], Any]]
    nte: Callable[[], Dict[str, float]]

def build_licm_router(dock_id: str, manifest: LICMManifest, providers: LICMProvider):
    from fastapi import APIRouter, HTTPException
    router = APIRouter(prefix=f"/api/{dock_id}/licm", tags=[f"{dock_id}-licm"])
    
    @router.get("/manifest")
    async def get_manifest():
        return {
            "dock_id": manifest.dock_id, "menu_label": manifest.menu_label,
            "icon": manifest.icon, "color_accent": manifest.color_accent,
            "one_line_pitch": manifest.one_line_pitch,
            "views": [{"name": v.name, "description": v.description, "metrics": v.metrics, "controls": v.controls} for v in manifest.views],
            "ws_channel": manifest.ws_channel
        }
    
    @router.get("/status")
    async def get_status():
        try:
            raw = providers.status()
            return {k: v.to_dict() for k, v in raw.items()}
        except LicmUnmeasured as e:
            raise HTTPException(status_code=501, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Status provider failed: {e}")
            
    @router.get("/events")
    async def get_events(since_seq: int = 0):
        return {"events": providers.events_source(since_seq)}
        
    @router.post("/action/{action_name}")
    async def execute_action(action_name: str, payload: Dict[str, Any]):
        if action_name not in providers.actions:
            raise HTTPException(status_code=404, detail=f"Action {action_name} not found")
        receipt_id = str(uuid.uuid4())
        receipt = {"receipt_id": receipt_id, "dock": dock_id, "action": action_name, "payload": payload, "status": "pending", "timestamp": time.time()}
        try:
            import asyncio
            if asyncio.iscoroutinefunction(providers.actions[action_name]):
                result = await providers.actions[action_name](payload)
            else:
                result = providers.actions[action_name](payload)
            receipt["status"] = "completed"
            receipt["result"] = result
            return receipt
        except Exception as e:
            receipt["status"] = "failed"
            receipt["error"] = str(e)
            return receipt
            
    @router.get("/nte")
    async def get_nte():
        return {"nte_state": providers.nte(), "timestamp": time.time()}
        
    return router


# === START: Canonical Additions ===
LICMView = ViewDefinition  # Canonical alias for backwards compatibility
LICMProviders = LICMProvider  # Canonical plural alias for backwards compatibility

def normalize_nte_state(state_dict: dict) -> dict:
    """Canonical NTE state normalizer [S4.3]. Clamps values and calculates scrutiny."""
    normalized = {}
    for key, val in state_dict.items():
        normalized[key] = max(0.0, min(100.0, float(val))) if isinstance(val, (int, float)) else val
    normalized['scrutiny_level'] = 'HIGH' if normalized.get('epinephrine', 0) > 70 else 'NORMAL'
    return normalized


def normalize_provenance(value: any) -> str:
    """Canonical provenance normalizer."""
    return str(value).upper() if str(value).upper() in {'LIVE', 'DERIVED', 'UNMEASURED'} else 'DERIVED'

# === END: Canonical Additions ===

# === START: Canonical LICM Additions ===

def licm_envelope(kind: str, payload: dict) -> dict:
    """Canonical LICM envelope wrapper [S13.7]."""
    return {"schema_version": "1.0", "kind": kind, "payload": payload, "provenance": "LIVE"}
live = 'LIVE'  # Canonical provenance tag constant
# === END: Canonical LICM Additions ===

def derive_from_registry(key: str, default: str = 'DERIVED') -> str:
    """Canonical LICM derivation tagger [S13.7]."""
    return f"{default}:{key}" if key else default

# === START: lowercase provenance constants ===
unmeasured = 'UNMEASURED'  # Canonical lowercase provenance constant
derived = 'DERIVED'  # Canonical lowercase provenance constant
# === END: lowercase provenance constants ===

# === START: make_urid_pair (dict) ===

def make_urid_pair(urid1: str, urid2: str) -> dict:
    """Canonical URID pair constructor [S2.1]."""
    return {"URID1": str(urid1), "URID2": str(urid2)}
# === END: make_urid_pair ===


# === START: provenance_alias_shim ===
# s13_endpoints.py (phoenix) imports `Provenance`; this module defines
# `ProvenanceTag`. Alias keeps both names working during the rename rollout.
try:
    if "Provenance" not in globals() and "ProvenanceTag" in globals():
        Provenance = ProvenanceTag  # noqa: F821
except Exception:
    pass
# === END: provenance_alias_shim ===
