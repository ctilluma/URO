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
# MODULE START : uro.security.field_encryption
# ---------------------------------------------------------------------
# FILE         : uro/security/field_encryption.py
# PURPOSE      : Per-field 512b AES keys with user/marketing wraps and
#                dynamic permission granting (RFC 60).
# STANDARD     : URO-STD-0001 S9
# =====================================================================
"Field-level encryption and dynamic permission granting (RFC 60)."

from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Dict

from uro.security.encryption import decrypt, encrypt

__all__ = ["EncryptedField", "FieldCipher"]


@dataclass
class EncryptedField:
    "PURPOSE: Data plus two wrapped-key headers (RFC 60)."
    data: bytes
    header1: bytes
    header2: bytes


class FieldCipher:
    "PURPOSE: Per-field 512b AES key with user and marketing wraps."

    def __init__(self, field_key: bytes, user_priv: bytes, marketing_pki: bytes) -> None:
        self.field_key = field_key
        self.user_priv = user_priv
        self.marketing_pki = marketing_pki

    def encrypt_field(self, plaintext: bytes) -> EncryptedField:
        "PURPOSE: AES256 data with the 512b key; wrap key for user and marketing."
        return EncryptedField(encrypt(self.field_key, plaintext),
                              encrypt(self.user_priv, self.field_key),
                              encrypt(self.marketing_pki, self.field_key))

    def decrypt_field(self, ef: EncryptedField, wrapped_key: bytes,
                      key_material: bytes) -> bytes:
        "PURPOSE: Unwrap the field key with holder material, then decrypt data."
        return decrypt(decrypt(key_material, wrapped_key), ef.data)

    def grant_access(self, grantee_key: bytes) -> Dict[str, bytes]:
        "PURPOSE: RFC 60.4 dynamic grant: Req -> PKI(what URO, random 512b -> id)."
        grant_id = secrets.token_hex(16)
        return {"grant_id": grant_id.encode(),
                "wrapped_key": encrypt(grantee_key, self.field_key)}
# =====================================================================
# MODULE END   : uro.security.field_encryption
# =====================================================================
