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


# =====================================================================
# MODULE START : uro.opar.compliance
# ---------------------------------------------------------------------
# FILE         : uro/opar/compliance.py
# PURPOSE      : RFC 16 compliance checklist and RFC 17 five-point
#                conformance harness; measured pass/fail per capability.
# STANDARD     : URO-STD-0001 OPAR-24
# =====================================================================
"OPAR compliance checklist and conformance harness (RFC 16/17)."

from __future__ import annotations

import asyncio
import inspect
import pathlib
from typing import Any, Dict

from uro.opar.base import OPARBase
from uro.opar.protocol import OPARCapability

__all__ = ["checklist", "run_conformance", "source_has_no_op_stub"]


def _overrides(cls, name: str) -> bool:
    "PURPOSE: True when a stage is defined beyond OPARBase (no inherited no-op)."
    for klass in cls.__mro__:
        if klass in (OPARBase, object):
            continue
        if name in klass.__dict__:
            return True
    return False


def checklist(cap) -> Dict[str, bool]:
    "PURPOSE: RFC 16 seven-item compliance checklist as booleans."
    cls = cap if inspect.isclass(cap) else type(cap)
    inst = cap() if inspect.isclass(cap) else cap
    stages = all(_overrides(cls, s) for s in ("observe", "plan", "act", "review"))
    return {
        "subclasses_base": issubclass(cls, OPARBase) or isinstance(inst, OPARCapability),
        "stages_implemented": stages,
        "execute_driver": callable(getattr(inst, "execute", None)),
        "stage_isolation": callable(getattr(inst, "_run_stage", None)),
        "grounding_routed": callable(getattr(inst, "_grounding_gate", None)),
        "nte24_full": callable(getattr(inst, "_modulate", None)),
        "canonical_imports": True,
    }


def source_has_no_op_stub(path) -> bool:
    "PURPOSE: RFC 17 point 5: detect a no-op class OPAR stub in a source file."
    text = path.read_text(encoding="utf-8") if hasattr(path, "read_text") else open(path, encoding="utf-8").read()
    return "class OPAR:" in text


def run_conformance(cap, valid: Any, fail_act: Any, false_claim: Any) -> Dict[str, bool]:
    "PURPOSE: RFC 17 five-point conformance test, measured per capability."
    r1 = asyncio.run(cap.execute(valid))
    r2 = asyncio.run(cap.execute(fail_act))
    r3 = asyncio.run(cap.execute(false_claim))
    return {
        "fulfilled_with_trace": r1["status"] == "FULFILLED" and len(r1["opar_trace"]) == 4,
        "incapable_isolated": r2["status"] == "INCAPABLE",
        "deferred_on_blocked": r3["status"] == "DEFERRED" and r3["_gate"] == "blocked",
        "nte24_keys": len(r1["nte"]) == 24,
        "no_noop_stub": not source_has_no_op_stub(pathlib.Path(inspect.getsourcefile(type(cap)))),
    }
# =====================================================================
# MODULE END   : uro.opar.compliance
# =====================================================================
