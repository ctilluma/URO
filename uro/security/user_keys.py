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
# MODULE START : uro.security.user_keys
# ---------------------------------------------------------------------
# FILE         : uro/security/user_keys.py
# PURPOSE      : User encryption and keying wraps: core key, user PKI wrap,
#                standard wrap, password-recovery wrap (RFC 53).
# STANDARD     : URO-STD-0001 S9
# =====================================================================
"User encryption and keying wraps (RFC 53)."

from __future__ import annotations

from dataclasses import dataclass

from uro.security.encryption import derive_key_from_password, decrypt, encrypt
from uro.security.hashing import sha512

__all__ = ["UserKeyring"]


@dataclass
class UserKeyring:
    "PURPOSE: Wraps for private key and recovery per RFC 53.1."
    core_key: bytes
    standard_wrap: bytes
    recovery_wrap: bytes
    user_pki_wrap: bytes

    @classmethod
    def create(cls, password: bytes, encrypt_key: bytes, private_key: bytes,
               inspa_enc: bytes) -> "UserKeyring":
        "PURPOSE: Build all RFC 53.1 wraps from a password."
        core = derive_key_from_password(password, encrypt_key)
        pki_wrap = encrypt(core, private_key)
        std = encrypt(sha512(sha512(password)), private_key)
        rec = encrypt(sha512(inspa_enc), sha512(password))
        return cls(core_key=core, standard_wrap=std, recovery_wrap=rec,
                   user_pki_wrap=pki_wrap)

    def unlock(self, password: bytes) -> bytes:
        "PURPOSE: Recover the private key via the standard wrap (RFC 53.1 step 4)."
        return decrypt(sha512(sha512(password)), self.standard_wrap)

    def recovery_proof(self, inspa_enc: bytes) -> bytes:
        "PURPOSE: Recover SHA512(password) via the recovery wrap (RFC 53.1 step 5)."
        return decrypt(sha512(inspa_enc), self.recovery_wrap)
# =====================================================================
# MODULE END   : uro.security.user_keys
# =====================================================================
