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
# MODULE START : uro.pathing.swarms
# ---------------------------------------------------------------------
# FILE         : uro/pathing/swarms.py
# PURPOSE      : Swarm object composition and routing tuple semantics
#                (RFC 81).
# STANDARD     : URO-STD-0001 S9
# =====================================================================
"Swarm object and routing tuple semantics (RFC 81)."

from __future__ import annotations

from typing import Any, List

__all__ = ["SwarmObject", "classify_routing"]


class SwarmObject:
    "PURPOSE: Swarm comprises communications, potentiators, associations (RFC 81.1)."

    def __init__(self) -> None:
        self.communications: List[Any] = []
        self.potentiators: List[Any] = []
        self.associations: List[Any] = []


def classify_routing(urid1: str, urid2: str) -> str:
    "PURPOSE: RFC 81.2 routing tuple semantics."
    if urid1 != "0" and urid2 == "0":
        return "request_object"
    if urid1 == "0" and urid2 != "0":
        return "attached_data_send"
    if urid1 != "0" and urid2 != "0":
        return "respond_urid2_from_urid1"
    return "broadcast"
# =====================================================================
# MODULE END   : uro.pathing.swarms
# =====================================================================
