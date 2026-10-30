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
# MODULE START : uro.security.ldap
# ---------------------------------------------------------------------
# FILE         : uro/security/ldap.py
# PURPOSE      : LDAP schema fields and the six-step uPass hash chain
#                (RFC 58).
# STANDARD     : URO-STD-0001 S9
# =====================================================================
"LDAP schema and uPass hash chain (RFC 58)."

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import blake3 as _blake3

from uro.security.encryption import xor_bytes

__all__ = ["LDAP_FIELDS", "LDAPRecord", "UpassKeys", "upass_chain"]

LDAP_FIELDS = ("username", "password", "encryption_key", "recovery_key",
               "public_cert", "private_key", "uuid", "active")


def _b3(data: bytes) -> bytes:
    "PURPOSE: BLAKE3 32-byte digest."
    return _blake3.blake3(data).digest()


def _sha512(data: bytes) -> bytes:
    "PURPOSE: SHA-512 digest."
    return hashlib.sha512(data).digest()


def _sha256(data: bytes) -> bytes:
    "PURPOSE: SHA-256 digest."
    return hashlib.sha256(data).digest()


@dataclass
class UpassKeys:
    "PURPOSE: The six-step uPass derivation outputs (RFC 58.2)."
    step1: bytes
    step2: bytes
    step3: bytes
    step4: bytes
    step5: bytes
    step6: bytes

    @property
    def encryption_key(self) -> bytes:
        "PURPOSE: Step 3 is the encryption key."
        return self.step3

    @property
    def verify_key(self) -> bytes:
        "PURPOSE: Step 4 is the verify key."
        return self.step4

    @property
    def server_user_enc_key(self) -> bytes:
        "PURPOSE: Step 5 server user encrypted key."
        return self.step5

    @property
    def server_verify_key(self) -> bytes:
        "PURPOSE: Step 6 server stored verify key."
        return self.step6


def upass_chain(upass: bytes) -> UpassKeys:
    "PURPOSE: RFC 58.2 alternating BLAKE3/SHA512 six-step chain."
    s1 = _b3(_sha512(xor_bytes(_sha256(upass), _b3(upass))))
    s2 = _sha512(_b3(s1))
    s3 = _b3(_sha512(s2))
    s4 = _sha512(_b3(s3))
    s5 = _b3(_sha512(s4))
    s6 = _sha512(_b3(s5))
    return UpassKeys(s1, s2, s3, s4, s5, s6)


@dataclass
class LDAPRecord:
    "PURPOSE: LDAP schema fields per RFC 58.1."
    username: str
    password: bytes
    encryption_key: bytes = b""
    recovery_key: bytes = b""
    public_cert: bytes = b""
    private_key: bytes = b""
    uuid: str = ""
    active: bool = True

    @classmethod
    def from_upass(cls, username: str, upass: bytes, uuid: str) -> "LDAPRecord":
        "PURPOSE: Build a record storing only derived server keys (RFC 58)."
        k = upass_chain(upass)
        return cls(username=username, password=k.server_verify_key,
                   encryption_key=k.encryption_key, uuid=uuid)
# =====================================================================
# MODULE END   : uro.security.ldap
# =====================================================================
