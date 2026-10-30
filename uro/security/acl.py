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
# MODULE START : uro.security.acl
# ---------------------------------------------------------------------
# FILE         : uro/security/acl.py
# PURPOSE      : Access Control Lists with binary combinators
#                (AND, OR, NAND, NOR). Default-deny.
# STANDARD     : URO-STD-0001 S9.5
# =====================================================================
"""Access Control Lists with binary combinators."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from uro.exceptions import ACLError

__all__ = ["ACLCombinator", "ACLEntry", "ACL"]


class ACLCombinator(Enum):
    """Binary combinators used to fold ACL entry results."""
    AND = auto()
    OR = auto()
    NAND = auto()
    NOR = auto()


@dataclass
class ACLEntry:
    """A single ACL rule."""
    subject: str
    permission: str
    allow: bool = True


class ACL:
    """An ACL that evaluates entries with a combinator."""

    def __init__(self, combinator: ACLCombinator = ACLCombinator.AND) -> None:
        """Create an ACL."""
        self.combinator = combinator
        self.entries: List[ACLEntry] = []

    def add(self, entry: ACLEntry) -> "ACL":
        """Append an entry."""
        self.entries.append(entry)
        return self

    def evaluate(self, subject: str, permission: str) -> bool:
        """Evaluate access for a subject and permission (default-deny)."""
        flags = [e.allow for e in self.entries
                 if e.subject == subject and e.permission == permission]
        if not flags:
            return False
        if self.combinator is ACLCombinator.AND:
            return all(flags)
        if self.combinator is ACLCombinator.OR:
            return any(flags)
        if self.combinator is ACLCombinator.NAND:
            return not all(flags)
        if self.combinator is ACLCombinator.NOR:
            return not any(flags)
        raise ACLError(f"unknown combinator {self.combinator}")
def override_check(acl: "ACL", subject: str, permission: str):
    "PURPOSE: RFC 59.1 override ACL as OR: any permit wins, else any ban."
    permits = [e for e in acl.entries if e.subject == subject and e.permission == permission and e.allow]
    bans = [e for e in acl.entries if e.subject == subject and e.permission == permission and not e.allow]
    if permits:
        return ("permit", permits[0])
    if bans:
        return ("ban", acl)
    return ("none", None)
# =====================================================================
# MODULE END   : uro.security.acl
# =====================================================================
