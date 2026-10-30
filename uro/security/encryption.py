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
# MODULE START : uro.security.encryption
# ---------------------------------------------------------------------
# FILE         : uro/security/encryption.py
# PURPOSE      : Symmetric encryption. 1024-bit key = K1||K2;
#                MSG = AES256(K2, AES256(K1, MSG)). AES via `cryptography`
#                when present, else a labeled SHAKE-256 stream fallback.
# STANDARD     : URO-STD-0001 S9.2
# =====================================================================
"""Symmetric encryption primitives for URO data and keys."""

from __future__ import annotations

import hashlib as _hashlib
import os as _os
from typing import Tuple

from uro.constants import KEY_1024_BYTES, SHA512_BYTES
from uro.exceptions import EncryptionError
from uro.security.hashing import sha512x3

__all__ = ["xor_bytes", "derive_key_from_password", "split_1024_key",
           "encrypt", "decrypt", "double_encrypt", "double_decrypt"]

try:  # pragma: no cover
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM as _AESGCM
    _HAVE_AES = True
except Exception:  # pragma: no cover
    _AESGCM = None
    _HAVE_AES = False


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR two equal-length byte strings."""
    if len(a) != len(b):
        raise EncryptionError("xor_bytes requires equal-length inputs")
    return bytes(x ^ y for x, y in zip(a, b))


def derive_key_from_password(password: bytes, encrypt_key: bytes) -> bytes:
    """key = SHA512x3(password) XOR encrypt_key."""
    core = sha512x3(password)
    return xor_bytes(core, encrypt_key[:SHA512_BYTES].ljust(SHA512_BYTES, b"\0"))


def split_1024_key(key: bytes) -> Tuple[bytes, bytes]:
    """Split a 128-byte key into (K1, K2)."""
    if len(key) != KEY_1024_BYTES:
        raise EncryptionError(f"expected {KEY_1024_BYTES}-byte key, got {len(key)}")
    return key[:SHA512_BYTES], key[SHA512_BYTES:]


def _shake_stream(seed: bytes, length: int) -> bytes:
    """Generate a pseudorandom keystream via SHAKE-256."""
    return _hashlib.shake_256(seed).digest(length)


def _aes_key(half_key: bytes) -> bytes:
    "PURPOSE: Derive a 256-bit AES key from a 512-bit half-key via SHA-512 truncation (ADR-010)."
    return _hashlib.sha512(half_key).digest()[:32]


def _sym_encrypt(key: bytes, plaintext: bytes) -> bytes:
    """Encrypt with the active backend, returning nonce||ciphertext."""
    if _HAVE_AES:  # pragma: no cover
        aes_key = _aes_key(key)
        nonce = _os.urandom(12)
        ct = _AESGCM(aes_key).encrypt(nonce, plaintext, None)
        return nonce + ct
    nonce = _os.urandom(16)
    keystream = _shake_stream(key + nonce, len(plaintext))
    return nonce + xor_bytes(plaintext, keystream)


def _sym_decrypt(key: bytes, blob: bytes) -> bytes:
    """Decrypt a nonce||ciphertext blob."""
    if _HAVE_AES:  # pragma: no cover
        aes_key = _aes_key(key)
        nonce, ct = blob[:12], blob[12:]
        return _AESGCM(aes_key).decrypt(nonce, ct, None)
    nonce, ct = blob[:16], blob[16:]
    keystream = _shake_stream(key + nonce, len(ct))
    return xor_bytes(ct, keystream)


def encrypt(key: bytes, plaintext: bytes) -> bytes:
    """Single-layer encrypt."""
    return _sym_encrypt(key, plaintext)


def decrypt(key: bytes, blob: bytes) -> bytes:
    """Single-layer decrypt."""
    return _sym_decrypt(key, blob)


def double_encrypt(key_1024: bytes, plaintext: bytes) -> bytes:
    """Double-layer encrypt using a 1024-bit key (K1 then K2)."""
    k1, k2 = split_1024_key(key_1024)
    return _sym_encrypt(k2, _sym_encrypt(k1, plaintext))


def double_decrypt(key_1024: bytes, blob: bytes) -> bytes:
    """Reverse double_encrypt."""
    k1, k2 = split_1024_key(key_1024)
    return _sym_decrypt(k1, _sym_decrypt(k2, blob))
# =====================================================================
# MODULE END   : uro.security.encryption
# =====================================================================
