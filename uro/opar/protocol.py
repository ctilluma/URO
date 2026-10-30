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
# MODULE START : uro.opar.protocol
# ---------------------------------------------------------------------
# FILE         : uro/opar/protocol.py
# PURPOSE      : OPARCapability protocol: the interface every capability
#                MUST satisfy (RFC 13).
# STANDARD     : URO-STD-0001 OPAR-24
# =====================================================================
"OPARCapability protocol (RFC 13)."

from __future__ import annotations

from typing import Any, Dict, Optional, Protocol, runtime_checkable

from uro.opar.stages import StageResult

__all__ = ["OPARCapability"]


@runtime_checkable
class OPARCapability(Protocol):
    "PURPOSE: Interface every capability MUST satisfy (RFC 13)."
    capability_id: str

    async def observe(self, stimulus: Any, nte: Dict[str, float]) -> StageResult: ...

    async def plan(self, observation: StageResult, nte: Dict[str, float]) -> StageResult: ...

    async def act(self, plan: StageResult, nte: Dict[str, float]) -> StageResult: ...

    async def review(self, observation: StageResult, plan: StageResult,
                     action: StageResult, nte: Dict[str, float]) -> StageResult: ...

    async def execute(self, stimulus: Any,
                      nte: Optional[Dict[str, float]] = None) -> Dict[str, Any]: ...
# =====================================================================
# MODULE END   : uro.opar.protocol
# =====================================================================
