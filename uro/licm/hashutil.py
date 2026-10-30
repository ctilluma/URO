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

import json
from typing import Any, Tuple
from uro.base_uros import INAHASH

def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def inahash(data: bytes) -> Tuple[str, str]:
    """
    URO S7.2 INAHASH: Uses canonical INAHASH.compute.
    Returns (hex_digest, algorithm_name).
    """
    digest = INAHASH.compute(data)
    return digest, "INAHASH.canonical"

def seal_object(obj: Any) -> Tuple[str, str]:
    return inahash(canonical_json(obj))
