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
# MODULE START : uro.security.hashing
# ---------------------------------------------------------------------
# FILE         : uro/security/hashing.py
# PURPOSE      : Multi-standard hashing. INAHASH composes two families:
#                Blake3-1024( SHA3-1024( MSG ) ).
# STANDARD     : URO-STD-0001 S9.1
# =====================================================================
"""Multi-standard hashing primitives (INAHASH and helpers)."""

from __future__ import annotations

import hashlib as _hashlib

from uro.constants import HASH_1024_BYTES
from uro.exceptions import HashError

__all__ = ["sha3_1024", "blake3_1024", "inahash", "sha512", "sha512x3",
           "blake2b_256", "sha128"]

try:  # pragma: no cover
    import blake3 as _blake3  # type: ignore
    _HAVE_BLAKE3 = True
except Exception:  # pragma: no cover
    _blake3 = None
    _HAVE_BLAKE3 = False


def sha3_1024(data: bytes) -> bytes:
    """1024-bit SHA-3 family digest via SHAKE-256 (FIPS 202)."""
    return _hashlib.shake_256(data).digest(HASH_1024_BYTES)


def blake3_1024(data: bytes) -> bytes:
    """1024-bit BLAKE-family digest (native BLAKE3 or BLAKE2b profile)."""
    if _HAVE_BLAKE3:  # pragma: no cover
        return _blake3.blake3(data).digest(HASH_1024_BYTES)
    try:
        half_a = _hashlib.blake2b(data, digest_size=64,
                                  person=b"URO-INAHASH-A\x00\x00\x00").digest()
        half_b = _hashlib.blake2b(data, digest_size=64,
                                  person=b"URO-INAHASH-B\x00\x00\x00").digest()
        return half_a + half_b
    except Exception as exc:  # pragma: no cover
        raise HashError(f"blake3_1024 failed: {exc}") from exc


def inahash(message: bytes) -> bytes:
    """INAHASH = Blake3-1024( SHA3-1024( MSG ) )."""
    return blake3_1024(sha3_1024(message))


def sha512(data: bytes) -> bytes:
    """SHA-512 digest."""
    return _hashlib.sha512(data).digest()


def sha512x3(data: bytes) -> bytes:
    """Triple-iterated SHA-512 (core-key derivation)."""
    return sha512(sha512(sha512(data)))


def blake2b_256(data: bytes) -> bytes:
    """256-bit BLAKE2b digest (header checksum)."""
    return _hashlib.blake2b(data, digest_size=32).digest()


def sha128(data: bytes) -> bytes:
    """128-bit digest (SHA-256 truncated)."""
    return _hashlib.sha256(data).digest()[:16]
# =====================================================================
# MODULE END   : uro.security.hashing
# =====================================================================

# --- Convergence compatibility exports (auto-generated) ---
# compat:INAHash
class INAHash:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:compute_inahash (canonical alias; single source of truth per RFC 56)
compute_inahash = inahash
