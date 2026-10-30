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
# MODULE START : uro.pathing.path_ops
# ---------------------------------------------------------------------
# FILE         : uro/pathing/path_ops.py
# PURPOSE      : Priority sums (RFC 70.3), path hash (RFC 76.4), and
#                path grow/cut/combine (RFC 79).
# STANDARD     : URO-STD-0001 S9
# =====================================================================
"Priority sums, path hash, and path combine operations (RFC 70/76/79)."

from __future__ import annotations

import hashlib
from typing import List, Optional, Tuple

__all__ = ["combine_paths", "path_priority", "fastest_first", "path_hash"]


def combine_paths(p1: Tuple[str, str], p2: Tuple[str, str]) -> Optional[Tuple[str, str]]:
    "PURPOSE: RFC 79: (U1,U2)+(U3,U1) -> (U3,U2); None on junction mismatch."
    if p1[0] != p2[1]:
        return None
    return (p2[0], p1[1])


def path_priority(priorities: List[int]) -> int:
    "PURPOSE: RFC 70.3: sum of all paths = priority."
    return sum(priorities)


def fastest_first(priorities: List[int]) -> List[int]:
    "PURPOSE: RFC 70.3: 0 = fastest; order ascending."
    return sorted(priorities)


def path_hash(src: str, dest: str) -> str:
    "PURPOSE: RFC 76.4: SHA512(src, dest) for quick lookup before full routing."
    return hashlib.sha512((src + dest).encode()).hexdigest()
# =====================================================================
# MODULE END   : uro.pathing.path_ops
# =====================================================================
