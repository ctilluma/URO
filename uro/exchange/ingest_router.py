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
MODULE: Canonical Ingest Router (Phase C)
INTENT: A mountable FastAPI router implementing the full Receipt protocol on
        live traffic. Every ingest: creates a URO with enrichments, records
        custody, creates a synapse with the source dock, and returns a
        Receipt (FULFILLED / DEFERRED / INCAPABLE).
STANDARD: URO-STD-0001 S26

USAGE (in a dock's main.py):
    from uro.exchange.ingest_router import create_ingest_router

    async def my_process(payload):
        return {"result": "done"}          # -> FULFILLED
        # or: return {"defer": True}       # -> DEFERRED
        # or: raise / return None          # -> DEFERRED

    app.include_router(
        create_ingest_router("my_dock", process_fn=my_process,
                             capabilities=["my.intent"]),
        prefix="/canonical",
    )
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from uro.canonical_integration import (
    CanonicalUROHelper,
    establish_synapse,
    create_dock_uro,
)
from uro.exchange.receipt import ReceiptMode
from uro.registry_bridge import get_registry
from uro.base import OPARPhase

logger = logging.getLogger("CanonicalIngest")


class IngestRequest(BaseModel):
    urid1_source: str = ""
    urid2_instance: str = ""
    intent: str = ""
    payload: Dict[str, Any] = Field(default_factory=dict)
    source_dock: str = ""
    topic: str = "general"


def create_ingest_router(
    dock_name: str,
    process_fn: Optional[Callable] = None,
    capabilities: Optional[List[str]] = None,
) -> APIRouter:
    """
    Build a FastAPI router implementing the canonical Receipt protocol.

    Args:
        dock_name: This dock's name.
        process_fn: Optional async fn(payload) -> dict.
            Return a dict        -> FULFILLED (inline response)
            Return {"defer":..}  -> DEFERRED (async via Observe queue)
            Return None / absent -> DEFERRED
        capabilities: If provided and request intent not in it -> INCAPABLE.
    """
    router = APIRouter()
    helper = CanonicalUROHelper(dock_name=dock_name)
    reg = get_registry()

    @router.post("/uro/ingest")
    async def ingest(req: IngestRequest) -> Dict[str, Any]:
        # 1. Create a complete URO with enrichments (registered in graph)
        uro_data = helper.create_uro(
            payload={**req.payload, "_intent": req.intent},
        )
        base = uro_data["base"]

        # 2. Establish a synapse with the source dock (per-topic trust)
        if req.source_dock:
            src_data = create_dock_uro(dock_name=req.source_dock,
                                       payload={"dock_name": req.source_dock})
            syn = establish_synapse(
                req.source_dock, dock_name,
                src_data["base"], base,
                topic=req.topic,
                endpoint1_nte=src_data["nte_state"],
                endpoint2_nte=uro_data["nte_state"],
            )
            reg.register_synapse(syn)

        # 3. Record custody (Observe)
        helper.record_custody(uro_data, OPARPhase.OBSERVE,
                              {"dopamine": 50.0, "oxytocin": 50.0})

        # 4. Capability gate -> INCAPABLE
        if capabilities and req.intent and req.intent not in capabilities:
            receipt = helper.create_incapable_receipt(
                base,
                reason=f"Dock '{dock_name}' lacks capability '{req.intent}'",
                remediation_suggestion="Route to a capable dock or query cognitive",
            )
            return _receipt_dict(receipt, base)

        # 5. Process -> FULFILLED or DEFERRED
        if process_fn is None:
            receipt = helper.create_deferred_receipt(
                base, complexity_class="no_handler",
                observe_queue_ref=f"/queue/{dock_name}/responses",
            )
            return _receipt_dict(receipt, base)

        try:
            result = await process_fn(req.payload)
        except Exception as e:
            logger.error(f"[{dock_name}] process error: {e}")
            result = None

        if result is None:
            receipt = helper.create_deferred_receipt(
                base, complexity_class="async",
                observe_queue_ref=f"/queue/{dock_name}/responses",
            )
        elif isinstance(result, dict) and result.get("defer"):
            receipt = helper.create_deferred_receipt(
                base, complexity_class=result.get("class", "llm_call"),
                estimated_completion=result.get("eta"),
                observe_queue_ref=f"/queue/{dock_name}/responses",
            )
        else:
            helper.record_custody(uro_data, OPARPhase.REVIEW,
                                  {"dopamine": 70.0, "serotonin": 60.0})
            receipt = helper.create_fulfilled_receipt(base, [result])

        return _receipt_dict(receipt, base)

    return router


def _receipt_dict(receipt, base) -> Dict[str, Any]:
    return {
        "mode": receipt.mode,
        "urid1": base.urid1.to_hex(),
        "urid2": base.urid2.to_hex(),
        "inahash": base.inahash,
        "payload_uros": receipt.payload_uros,
        "reason": receipt.reason,
        "observe_queue_ref": receipt.observe_queue_ref,
        "complexity_class": receipt.complexity_class,
    }
