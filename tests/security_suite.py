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


#!/usr/bin/env python3
# === FILE: tests/security_suite.py ===
# PURPOSE: Phase 3 validation: INAHASH composition (RFC 56), 1024-bit key
#          splitting and nested AES-256 round-trips (RFC 50).
# === END FILE HEADER ===
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.security.hashing import sha3_1024, blake3_1024, inahash, sha512x3
from uro.security.encryption import (
    split_1024_key, double_encrypt, double_decrypt,
    derive_key_from_password, xor_bytes, _aes_key,
)
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 sha3_1024 yields 128 bytes")
def c01():
    assert len(sha3_1024(b"abc")) == 128
@check("02 blake3_1024 yields 128 bytes")
def c02():
    assert len(blake3_1024(b"abc")) == 128
@check("03 inahash deterministic 128 bytes")
def c03():
    a = inahash(b"msg")
    assert len(a) == 128
    assert a == inahash(b"msg")
@check("04 inahash distinguishes messages")
def c04():
    assert inahash(b"a") != inahash(b"b")
@check("05 inahash equals Blake3-1024(SHA3-1024(MSG))")
def c05():
    assert inahash(b"compose") == blake3_1024(sha3_1024(b"compose"))
@check("06 split_1024_key halves and rejects bad size")
def c06():
    k1, k2 = split_1024_key(bytes(range(128)))
    assert len(k1) == 64 and len(k2) == 64
    try:
        split_1024_key(b"short")
        raise AssertionError("bad size accepted")
    except AssertionError:
        raise
    except Exception:
        pass
@check("07 nested AES round-trip")
def c07():
    key = bytes(range(128))
    assert double_decrypt(key, double_encrypt(key, b"secret payload")) == b"secret payload"
@check("08 wrong key fails decrypt")
def c08():
    blob = double_encrypt(bytes(range(128)), b"secret")
    try:
        double_decrypt(bytes(range(128, 256)), blob)
        raise AssertionError("wrong key decrypted")
    except AssertionError:
        raise
    except Exception:
        pass
@check("09 tampered ciphertext fails")
def c09():
    blob = bytearray(double_encrypt(bytes(range(128)), b"secret"))
    blob[-1] ^= 0xFF
    try:
        double_decrypt(bytes(range(128)), bytes(blob))
        raise AssertionError("tamper accepted")
    except AssertionError:
        raise
    except Exception:
        pass
@check("10 key derivation and AES key mixing")
def c10():
    assert derive_key_from_password(b"pw", b"k" * 64) == xor_bytes(sha512x3(b"pw"), b"k" * 64)
    assert len(_aes_key(b"\x00" * 64)) == 32
    assert _aes_key(b"\x00" * 64) != b"\x00" * 32
passed = 0
for name, fn in checks:
    try:
        fn()
        passed += 1
        print("PASS  " + name)
    except Exception as e:
        print("FAIL  " + name + " :: " + type(e).__name__ + ": " + str(e))
print("%d/10 checks passed" % passed)
sys.exit(0 if passed == 10 else 1)
