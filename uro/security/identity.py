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
# MODULE START : uro.security.identity
# ---------------------------------------------------------------------
# FILE         : uro/security/identity.py
# PURPOSE      : Identity verification and tokens.
# STANDARD     : URO-STD-0001 S9.3
# =====================================================================
"""Identity verification and tokens."""

from __future__ import annotations

import secrets as _secrets
from dataclasses import dataclass
from typing import Dict

from uro.exceptions import IdentityError
from uro.security.hashing import sha512, sha512x3

__all__ = ["Identity", "IdentityToken"]


@dataclass
class IdentityToken:
    """A token maintaining verified identity."""
    token: str
    subject: str
    indefinite: bool = False
    revoked: bool = False


class Identity:
    """Represents a verified identity bound to a URO."""

    def __init__(self, subject: str, password: bytes) -> None:
        """Create and register an identity from a password."""
        self.subject = subject
        self._core_key = sha512x3(password)
        self._verifier = sha512(self._core_key)
        self._tokens: Dict[str, IdentityToken] = {}

    def verify_password(self, password: bytes) -> bool:
        """Verify a candidate password against the stored verifier."""
        candidate = sha512(sha512x3(password))
        return _secrets.compare_digest(candidate, self._verifier)

    def bind_time_uro(self, time_uro) -> None:
        "PURPOSE: RFC 54.4: assign the response-and-time URO to a DateURO."
        self.bound_time_uro = time_uro

    def issue_token(self, indefinite: bool = False) -> IdentityToken:
        """Issue a new identity token."""
        tok = IdentityToken(token=_secrets.token_hex(32),
                            subject=self.subject, indefinite=indefinite)
        self._tokens[tok.token] = tok
        return tok

    def validate_token(self, token: str) -> bool:
        """Check whether a token is currently valid."""
        t = self._tokens.get(token)
        return t is not None and not t.revoked

    def revoke_token(self, token: str) -> None:
        """Revoke an issued token."""
        t = self._tokens.get(token)
        if t is None:
            raise IdentityError("unknown token")
        t.revoked = True
# =====================================================================
# MODULE END   : uro.security.identity
# =====================================================================
