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
# MODULE START : uro.security.policy
# ---------------------------------------------------------------------
# FILE         : uro/security/policy.py
# PURPOSE      : Policy UROs bundling any number of ACLs and policies.
# STANDARD     : URO-STD-0001 S9.6
# =====================================================================
"""Policy UROs composing multiple ACLs."""

from __future__ import annotations

from typing import Dict, List

from uro.core.uro import URO
from uro.core.urid import URID
from uro.security.acl import ACL

__all__ = ["PolicyURO"]


def _explicit_decision(acl: ACL, subject: str, permission: str):
    "PURPOSE: Return explicit allow/deny for an entry match, else None."
    for entry in acl.entries:
        if entry.subject == subject and entry.permission == permission:
            return bool(entry.allow)
    return None


class PolicyURO(URO):
    """A URO that carries and evaluates a set of ACLs."""

    def __init__(self, name: str) -> None:
        """Create a named Policy URO."""
        _identity = URID.new()
        super().__init__(_identity, _identity, {"policy": name})
        self._acls: Dict[str, ACL] = {}
        self._overrides: Dict[str, bool] = {}

    def add_acl(self, scope: str, acl: ACL, override: bool = False) -> "PolicyURO":
        "PURPOSE: Attach an ACL to a named scope; override groups decide first (RFC 55.1)."
        self._acls[scope] = acl
        self._overrides[scope] = bool(override)
        return self

    def evaluate(self, scope: str, subject: str, permission: str) -> bool:
        "PURPOSE: Evaluate access; override-group entries decide first (RFC 55.1)."
        for name, is_ov in self._overrides.items():
            if not is_ov:
                continue
            acl = self._acls.get(name)
            if acl is None:
                continue
            hit = _explicit_decision(acl, subject, permission)
            if hit is not None:
                return hit
        acl = self._acls.get(scope)
        if acl is None:
            return False
        return acl.evaluate(subject, permission)

    def scopes(self) -> List[str]:
        """Return the list of configured scopes."""
        return list(self._acls.keys())
# =====================================================================
# MODULE END   : uro.security.policy
# =====================================================================
