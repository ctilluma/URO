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
# MODULE START : uro.core.components
# ---------------------------------------------------------------------
# FILE         : uro/core/components.py
# PURPOSE      : Enforcement of the ten mandatory URO components (RFC 8).
# STANDARD     : URO-STD-0001 S8
# =====================================================================
"Enforcement of the ten mandatory URO components (RFC 8)."

from __future__ import annotations

from typing import Any, List

from uro.exceptions import UROStructureError

__all__ = ["COMPONENTS", "missing_components", "enforce_components"]

# RFC 8: every URO MUST contain these ten components.
COMPONENTS = (
    "urid_pair",
    "header",
    "payload",
    "nte",
    "acl",
    "personality",
    "capabilities",
    "associations",
    "children",
    "inahash",
)

_ATTRS = {
    "urid_pair": ("urid1", "urid2"),
    "header": ("header",),
    "payload": ("payload",),
    "nte": ("nte", "nte_state"),
    "acl": ("acl",),
    "personality": ("personality",),
    "capabilities": ("capabilities",),
    "associations": ("associations",),
    "children": ("children",),
    "inahash": ("inahash",),
}


def _present(obj: Any, component: str) -> bool:
    "PURPOSE: True when any accepted attribute for a component exists and is set."
    for attr in _ATTRS[component]:
        if hasattr(obj, attr) and getattr(obj, attr) is not None:
            return True
    return False


def missing_components(obj: Any) -> List[str]:
    "PURPOSE: List the RFC 8 components absent from obj."
    return [c for c in COMPONENTS if not _present(obj, c)]


def enforce_components(obj: Any) -> None:
    "PURPOSE: Raise UROStructureError when any mandatory component is missing."
    missing = missing_components(obj)
    if missing:
        raise UROStructureError("missing mandatory URO components: " + ", ".join(missing))
# =====================================================================
# MODULE END   : uro.core.components
# =====================================================================
