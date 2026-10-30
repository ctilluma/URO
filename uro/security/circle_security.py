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
# MODULE START : uro.security.circle_security
# ---------------------------------------------------------------------
# FILE         : uro/security/circle_security.py
# PURPOSE      : Concentric rings of access control: Store, Owner, Admin,
#                Access, Circle End User (RFC 57).
# STANDARD     : URO-STD-0001 S9
# =====================================================================
"Concentric ring access control (RFC 57)."

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from uro.security.encryption import decrypt, encrypt
from uro.security.hashing import sha512

__all__ = ["CircleSecurity", "CircleEndUser"]


@dataclass
class CircleEndUser:
    "PURPOSE: Circle 32B entity with social lists (RFC 57.5)."
    entity: bytes
    friends: List[str] = field(default_factory=list)
    following: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    acquaintance: List[str] = field(default_factory=list)
    blocked: List[str] = field(default_factory=list)


class CircleSecurity:
    "PURPOSE: Five concentric rings of key protection (RFC 57)."

    def __init__(self, key_512: bytes, owner_priv: bytes, admin_priv: bytes,
                 access_priv: bytes) -> None:
        self.key_512 = key_512
        self.owner_priv = owner_priv
        self.admin_priv = admin_priv
        self.access_priv = access_priv

    def store_digest(self) -> bytes:
        "PURPOSE: Ring 1 Store: SHA512(512b key)."
        return sha512(self.key_512)

    def wrap_owner(self) -> bytes:
        "PURPOSE: Ring 2 Owner: key encrypted under owner private material."
        return encrypt(self.owner_priv, self.key_512)

    def unwrap_owner(self, blob: bytes) -> bytes:
        "PURPOSE: Reverse ring 2."
        return decrypt(self.owner_priv, blob)

    def wrap_admin(self, req: int = 1) -> bytes:
        "PURPOSE: Ring 3 Admin: REQ=1 single wrap; REQ>1 matrix double wrap."
        if req <= 1:
            return encrypt(self.admin_priv, self.key_512)
        return encrypt(self.admin_priv, encrypt(self.admin_priv, self.key_512))

    def unwrap_admin(self, blob: bytes, req: int = 1) -> bytes:
        "PURPOSE: Reverse ring 3 for the given request depth."
        if req <= 1:
            return decrypt(self.admin_priv, blob)
        return decrypt(self.admin_priv, decrypt(self.admin_priv, blob))

    def wrap_access(self) -> bytes:
        "PURPOSE: Ring 4 Access: PKI priv encrypted with AES256(512b key)."
        return encrypt(self.key_512, self.access_priv)

    def unwrap_access(self, blob: bytes) -> bytes:
        "PURPOSE: Reverse ring 4."
        return decrypt(self.key_512, blob)

    def end_user(self, user_priv: bytes) -> CircleEndUser:
        "PURPOSE: Ring 5: AES256(SHA512(UserPriv), PKI(Priv)) 32B entity."
        wrapped = encrypt(sha512(user_priv), self.access_priv)
        return CircleEndUser(entity=wrapped[:32])
# =====================================================================
# MODULE END   : uro.security.circle_security
# =====================================================================
