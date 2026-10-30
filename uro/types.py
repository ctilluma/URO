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
# MODULE START : uro.types
# ---------------------------------------------------------------------
# FILE         : uro/types.py
# PURPOSE      : Shared type aliases and Protocols for the URO library.
# STANDARD     : URO-STD-0001 S1.4
# =====================================================================
"Shared type aliases and Protocols for the URO reference implementation."

from __future__ import annotations

from typing import Any, Dict, Optional, Protocol, Union, runtime_checkable

# RFC 1.2 / 1.4 aliases.
URIDInt = int
URIDHex = str
NTELevels = Dict[str, float]
Payload = Union[bytes, Dict[str, Any]]

@runtime_checkable
class UROCapable(Protocol):
    "PURPOSE: Protocol for objects satisfying the Fractal URO Mandate."
    urid1: Any
    urid2: Any
    inahash: str

    def to_dict(self) -> Dict[str, Any]: ...

@runtime_checkable
class OPARCapable(Protocol):
    "PURPOSE: Protocol for OPAR-24 compliant capabilities (RFC 13)."
    capability_id: str
    async def execute(self, stimulus: Any, nte: Optional[NTELevels] = None) -> Dict[str, Any]: ...
# =====================================================================
# MODULE END   : uro.types
# =====================================================================
