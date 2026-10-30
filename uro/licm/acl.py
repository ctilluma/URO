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

from typing import Optional

READ_ROLES = {"operator", "varuos_admin", "admin", "root", "dock-pki"}
WRITE_ROLES = {"varuos_admin", "admin", "root", "dock-pki"}
CONTROL_ROLES = {"varuos_admin"}


def normalize_role(role: Optional[str]) -> str:
    text = str(role or "").strip().lower().replace("_", "-")
    if text in {"dockpki", "dock-pki", "pki"}:
        return "dock-pki"
    if text in {"varuosadmin", "varuos-admin"}:
        return "varuos_admin"
    return text


def authorize(principal: Optional[str], role: Optional[str], tier: str = "read") -> bool:
    """
    S7.9 ACL tiers for LICM:
    - read: authenticated operator
    - write: varuos_admin/admin/root/dock-PKI
    - control: varuos_admin only
    """
    if not principal or not str(principal).strip():
        return False

    normalized_role = normalize_role(role)
    normalized_tier = str(tier or "read").strip().lower()

    if normalized_tier == "read":
        return normalized_role in READ_ROLES
    if normalized_tier == "write":
        return normalized_role in WRITE_ROLES
    if normalized_tier == "control":
        return normalized_role in CONTROL_ROLES
    return False
