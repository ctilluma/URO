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
# MODULE START : uro.security.pki
# ---------------------------------------------------------------------
# FILE         : uro/security/pki.py
# PURPOSE      : PKI public-key UROs and URO signatures.
# STANDARD     : URO-STD-0001 S9.4
# =====================================================================
"""PKI public-key UROs and URO signatures."""

from __future__ import annotations

import secrets as _secrets
from typing import Optional

from uro.core.uro import URO
from uro.core.urid import URID
from uro.time_uro import DateURO, now_date_uro
from uro.security.hashing import inahash

__all__ = ["PublicKeyURO", "UROSignature", "sign_uro", "verify_signature"]

# RFC 51.2: air-gapped offline root CA regions.
ROOT_CA_REGIONS = ("S.NA", "S.SA", "S.EU", "S.AF", "S.AS", "S.OC")


class PublicKeyURO(URO):
    """A URO representing a public key and its lifecycle instants."""

    def __init__(self, public_key: bytes) -> None:
        """Create a public-key URO issued now."""
        _identity = URID.new()
        super().__init__(_identity, _identity, {"kind": "PKI.PUBK"})
        self.public_key = public_key
        self.issued: DateURO = now_date_uro()
        self.expires: Optional[DateURO] = None
        self.revoked: Optional[DateURO] = None
        self.certificate: Optional[bytes] = None

    def set_expiration(self, when: DateURO) -> None:
        """Set the expiration instant."""
        self.expires = when

    def revoke(self) -> None:
        """Mark this key as revoked as of now."""
        self.revoked = now_date_uro()

    def is_valid(self) -> bool:
        """Return True if the key is not revoked."""
        return self.revoked is None


class UROSignature(URO):
    """A signature binding an object, signer, owner, and content digest."""

    def __init__(self, signed_object: URO, signer: URO, trust_owner: URO,
                 digest: bytes, signature: bytes) -> None:
        """Create a signature URO."""
        _identity = URID.new()
        super().__init__(_identity, _identity, {"kind": "PKI.SIGN"})
        self.signed_object = signed_object
        self.signer = signer
        self.trust_owner = trust_owner
        self.digest = digest
        self.signature = signature


def sign_uro(signed_object: URO, signer: URO, trust_owner: URO,
             private_key: bytes) -> UROSignature:
    """Sign a URO, producing a UROSignature."""
    digest = inahash(signed_object.link())
    material = digest + signer.link() + trust_owner.link() + private_key
    signature = inahash(material)
    return UROSignature(signed_object, signer, trust_owner, digest, signature)


def verify_signature(sig: UROSignature, private_key: bytes) -> bool:
    """Verify a UROSignature against the claimed content and keys."""
    expected_digest = inahash(sig.signed_object.link())
    if expected_digest != sig.digest:
        return False
    material = sig.digest + sig.signer.link() + sig.trust_owner.link() + private_key
    return _secrets.compare_digest(inahash(material), sig.signature)
# =====================================================================
# MODULE END   : uro.security.pki
# =====================================================================
