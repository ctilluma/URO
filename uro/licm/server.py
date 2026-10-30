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

import inspect
import json
from typing import Any, Dict, Optional

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ._compat import model_dump, model_validate
from .acl import authorize as acl_authorize
from .envelope import licm_envelope
from .events import EventRing
from .exceptions import LicmProvenanceError, LicmUnmeasured
from .ledger import ImmutableLedger
from .manifest import LICMManifest
from .nte import normalize_nte_state
from .provenance import Provenance, unmeasured, validate_status_payload
from .urid import make_urid_pair

_MISSING = object()


class ActionRequest(BaseModel):
    action: str
    args: Dict[str, Any] = Field(default_factory=dict)
    tier: str = "write"


async def invoke_callable(target: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(target):
        return target
    result = target(*args, **kwargs)
    if inspect.isawaitable(result):
        result = await result
    return result


class LicmRuntime:
    def __init__(
        self,
        dock_name: str,
        manifest: LICMManifest,
        providers: Dict[str, Any],
        ring: EventRing,
        ledger: ImmutableLedger,
    ) -> None:
        self.dock_name = dock_name
        self.manifest = manifest
        self.providers = providers or {}
        self.ring = ring
        self.ledger = ledger
        self.handlers: Dict[str, Any] = {}

    async def call_provider(self, name: str, default: Any = _MISSING) -> Any:
        provider = self.providers.get(name)
        if provider is None:
            if default is not _MISSING:
                return default
            raise LicmUnmeasured(f"provider '{name}' not configured")
        return await invoke_callable(provider)

    async def current_nte(self):
        try:
            raw = await self.call_provider("nte", default={})
        except LicmUnmeasured:
            raw = {}
        return normalize_nte_state(raw)

    def record_denial(self, principal: Any, role: Any, tier: str, resource: str, reason: str = "acl_denied"):
        payload = {
            "principal": principal,
            "role": role,
            "tier": tier,
            "resource": resource,
            "reason": reason,
        }
        entry = self.ledger.append("acl_denied", payload)
        self.ring.record("acl_denied", payload, Provenance.LIVE)
        return entry


def build_licm_router(
    dock_name: str,
    manifest: Any,
    providers: Optional[Dict[str, Any]] = None,
    *,
    ring: Optional[EventRing] = None,
    ledger: Optional[ImmutableLedger] = None,
) -> APIRouter:
    if isinstance(manifest, dict):
        manifest = model_validate(LICMManifest, manifest)

    ring = ring or EventRing()
    ledger = ledger or ImmutableLedger()
    runtime = LicmRuntime(dock_name, manifest, providers or {}, ring, ledger)
    router = APIRouter()

    def authorize_or_deny(principal: Any, role: Any, tier: str, resource: str) -> None:
        if not acl_authorize(principal, role, tier):
            runtime.record_denial(principal, role, tier, resource)
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "acl_denied",
                    "principal": principal,
                    "role": role,
                    "tier": tier,
                    "resource": resource,
                },
            )

    @router.get("/licm/manifest")
    async def get_manifest(
        x_uro_principal: Optional[str] = Header(default=None),
        x_uro_role: Optional[str] = Header(default=None),
    ):
        authorize_or_deny(x_uro_principal, x_uro_role, "read", "/licm/manifest")
        nte = await runtime.current_nte()
        payload = model_dump(manifest)
        return licm_envelope(
            make_urid_pair(dock_name, "licm.manifest"),
            payload,
            nte,
            {"kind": "DERIVED", "derivation": "dock-supplied LICM manifest"},
        )

    @router.get("/licm/status")
    async def get_status(
        x_uro_principal: Optional[str] = Header(default=None),
        x_uro_role: Optional[str] = Header(default=None),
    ):
        authorize_or_deny(x_uro_principal, x_uro_role, "read", "/licm/status")
        nte = await runtime.current_nte()

        try:
            payload = await runtime.call_provider("status")
        except LicmUnmeasured as exc:
            payload = {"status": unmeasured(str(exc))}
            return licm_envelope(
                make_urid_pair(dock_name, "licm.status"),
                payload,
                nte,
                {"kind": "UNMEASURED", "reason": str(exc)},
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail={
                    "error": "status_provider_failed",
                    "detail": f"{type(exc).__name__}: {exc}",
                },
            )

        try:
            validate_status_payload(payload)
        except LicmProvenanceError as exc:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "fabricated_status_metrics",
                    "detail": str(exc),
                },
            )

        return licm_envelope(
            make_urid_pair(dock_name, "licm.status"),
            payload,
            nte,
            Provenance.LIVE,
        )

    @router.get("/licm/events")
    async def get_events(
        since_seq: int = 0,
        stream: bool = False,
        accept: Optional[str] = Header(default=None),
        x_uro_principal: Optional[str] = Header(default=None),
        x_uro_role: Optional[str] = Header(default=None),
    ):
        authorize_or_deny(x_uro_principal, x_uro_role, "read", "/licm/events")

        source = runtime.providers.get("events_source")
        if source is not None:
            try:
                extra = await invoke_callable(source)
                if isinstance(extra, list):
                    for item in extra:
                        try:
                            if isinstance(item, dict):
                                kind = item.get("event", item.get("kind", "external"))
                                payload = item.get("payload", item)
                                prov = item.get("provenance", Provenance.LIVE)
                                runtime.ring.record(kind, payload, prov, item.get("nte_state"))
                        except Exception:
                            runtime.ring.record("invalid_event", {"item": str(item)}, Provenance.LIVE)
            except LicmUnmeasured:
                pass

        events, gap, oldest, latest = runtime.ring.since(since_seq)
        wants_sse = bool(stream) or (accept is not None and "text/event-stream" in str(accept).lower())

        if wants_sse:
            async def event_stream():
                resume = {
                    "since_seq": since_seq,
                    "gap": gap,
                    "oldest_seq": oldest,
                    "latest_seq": latest,
                    "ws_channel": manifest.ws_channel,
                }
                yield f"event: licm.resume\ndata: {json.dumps(resume, default=str)}\n\n"
                if gap:
                    yield f"event: licm.gap\ndata: {json.dumps({'gap': True, 'oldest_seq': oldest}, default=str)}\n\n"
                for event in events:
                    yield f"id: {event['seq']}\nevent: {event['event']}\ndata: {json.dumps(event, default=str)}\n\n"

            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-LICM-WS-Channel": manifest.ws_channel,
                },
            )

        payload = {
            "since_seq": since_seq,
            "events": events,
            "gap": gap,
            "oldest_seq": oldest,
            "latest_seq": latest,
            "ws_channel": manifest.ws_channel,
        }
        nte = await runtime.current_nte()
        return licm_envelope(
            make_urid_pair(dock_name, "licm.events"),
            payload,
            nte,
            Provenance.LIVE,
        )

    @router.post("/licm/action")
    async def post_action(
        body: ActionRequest,
        x_uro_principal: Optional[str] = Header(default=None),
        x_uro_role: Optional[str] = Header(default=None),
    ):
        requested_tier = str(body.tier or "write").strip().lower()
        if requested_tier not in {"write", "control"}:
            requested_tier = "write"

        resource = f"/licm/action/{body.action}"
        authorize_or_deny(x_uro_principal, x_uro_role, requested_tier, resource)

        actions = runtime.providers.get("actions") or {}
        action_def = actions.get(body.action)
        if action_def is None:
            raise HTTPException(status_code=404, detail={"error": "action_not_found", "action": body.action})

        if isinstance(action_def, dict):
            handler = action_def.get("handler")
            required_tier = str(action_def.get("tier", requested_tier)).strip().lower()
        else:
            handler = action_def
            required_tier = requested_tier

        if required_tier not in {"write", "control"}:
            required_tier = "write"
        if required_tier != requested_tier:
            authorize_or_deny(x_uro_principal, x_uro_role, required_tier, resource)

        if handler is None:
            raise HTTPException(status_code=500, detail={"error": "action_handler_missing", "action": body.action})

        receipt_payload = {
            "action": body.action,
            "args": body.args,
            "tier": required_tier,
            "principal": x_uro_principal,
            "role": x_uro_role,
        }

        # S14.4: receipt BEFORE effect.
        receipt = runtime.ledger.append("control_receipt", receipt_payload)
        runtime.ring.record("control_receipt", receipt, Provenance.LIVE)

        try:
            result = await invoke_callable(handler, body.args)
        except LicmUnmeasured as exc:
            effect_payload = {
                "action": body.action,
                "receipt_seq": receipt["seq"],
                "status": "unmeasured",
                "reason": str(exc),
            }
            effect = runtime.ledger.append("action_effect", effect_payload)
            runtime.ring.record("action_effect", effect, {"kind": "UNMEASURED", "reason": str(exc)})
            nte = await runtime.current_nte()
            return licm_envelope(
                make_urid_pair(dock_name, "licm.action"),
                {"receipt": receipt, "effect": effect, "result": None},
                nte,
                {"kind": "UNMEASURED", "reason": str(exc)},
            )
        except Exception as exc:
            effect_payload = {
                "action": body.action,
                "receipt_seq": receipt["seq"],
                "status": "error",
                "error": f"{type(exc).__name__}: {exc}",
            }
            effect = runtime.ledger.append("action_effect", effect_payload)
            runtime.ring.record("action_effect", effect, Provenance.LIVE)
            raise HTTPException(
                status_code=502,
                detail={
                    "error": "action_failed",
                    "detail": effect_payload["error"],
                    "receipt_seq": receipt["seq"],
                },
            )

        effect_payload = {
            "action": body.action,
            "receipt_seq": receipt["seq"],
            "status": "ok",
            "result": result,
        }
        effect = runtime.ledger.append("action_effect", effect_payload)
        runtime.ring.record("action_effect", effect, Provenance.LIVE)

        nte = await runtime.current_nte()
        return licm_envelope(
            make_urid_pair(dock_name, "licm.action"),
            {"receipt": receipt, "effect": effect, "result": result},
            nte,
            Provenance.LIVE,
        )

    @router.get("/licm/nte")
    async def get_nte(
        x_uro_principal: Optional[str] = Header(default=None),
        x_uro_role: Optional[str] = Header(default=None),
    ):
        authorize_or_deny(x_uro_principal, x_uro_role, "read", "/licm/nte")
        nte = await runtime.current_nte()
        payload = {
            "nte_state": model_dump(nte),
            "axis_count": nte.axis_count,
        }
        return licm_envelope(
            make_urid_pair(dock_name, "licm.nte"),
            payload,
            nte,
            Provenance.LIVE,
        )

    runtime.handlers = {
        "manifest": get_manifest,
        "status": get_status,
        "events": get_events,
        "action": post_action,
        "nte": get_nte,
    }
    router.licm = runtime
    return router
