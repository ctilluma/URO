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
# MODULE START : uro.core.inheritance
# ---------------------------------------------------------------------
# FILE         : uro/core/inheritance.py
# PURPOSE      : Capability inheritance and security-context propagation
#                across the URO lineage (RFC 9, RFC 2.4).
# STANDARD     : URO-STD-0001 S9
# =====================================================================
"Capability inheritance and abstraction helpers (RFC 9, RFC 2.4)."

from __future__ import annotations

from typing import Any

from uro.exceptions import UROStructureError

__all__ = ["inherit_capabilities", "resolve_capability", "inherit_security_context"]


def inherit_capabilities(child: Any, parent: Any) -> dict:
    "PURPOSE: Merge parent capabilities into child; child entries win (RFC 9.1)."
    merged = dict(getattr(parent, "capabilities", {}) or {})
    merged.update(dict(getattr(child, "capabilities", {}) or {}))
    child.capabilities = merged
    return merged


def resolve_capability(obj: Any, name: str) -> Any:
    "PURPOSE: Walk the parent chain upward to find a capability by name."
    current = obj
    seen = 0
    while current is not None and seen < 64:
        caps = getattr(current, "capabilities", {}) or {}
        if name in caps:
            return caps[name]
        current = getattr(current, "parent", None)
        seen += 1
    raise UROStructureError("capability not resolvable in lineage: " + name)


def inherit_security_context(child: Any, parent: Any) -> Any:
    "PURPOSE: Child inherits the parent ACL/security context (RFC 2.4)."
    if getattr(child, "acl", None) is None:
        child.acl = getattr(parent, "acl", None)
    return child.acl
# =====================================================================
# MODULE END   : uro.core.inheritance
# =====================================================================
