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
# MODULE START : uro.pathing.cro_matrix
# ---------------------------------------------------------------------
# FILE         : uro/pathing/cro_matrix.py
# PURPOSE      : CRO resolution matrix (RFC 72): significance lookup for
#                CRO1/CRO2 URID presence flag quadruples.
# STANDARD     : URO-STD-0001 S9
# =====================================================================
"CRO resolution matrix (RFC 72)."

from __future__ import annotations

__all__ = ["CRO_RESOLUTION", "resolve_cro"]

# Keys are (URID1, URID2, URID3, URID4) presence flags as 0/1.
CRO_RESOLUTION = {
    (0, 0, 0, 0): "Source / Destination ACL / Personality",
    (0, 0, 0, 1): "Return new non-source dependent CRO",
    (0, 1, 0, 0): "Path to handle CRO1",
    (1, 0, 1, 0): "Path to convert type CRO1 to CRO2",
    (1, 1, 1, 1): "Return CRO2 from Source / Data CRO1",
}


def resolve_cro(urid1: bool, urid2: bool, urid3: bool, urid4: bool) -> str:
    "PURPOSE: Look up the RFC 72 significance for a CRO flag quadruple."
    key = (int(bool(urid1)), int(bool(urid2)), int(bool(urid3)), int(bool(urid4)))
    if key not in CRO_RESOLUTION:
        raise KeyError("unmapped CRO combination: " + str(key))
    return CRO_RESOLUTION[key]
# =====================================================================
# MODULE END   : uro.pathing.cro_matrix
# =====================================================================
