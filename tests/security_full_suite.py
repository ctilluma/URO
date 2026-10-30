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
# === FILE: tests/security_full_suite.py ===
# PURPOSE: Phase 13 validation: uPass chain, circle rings, field encryption,
#          user keyring wraps, custody exchange, policy/ACL overrides, PKI.
# === END FILE HEADER ===
import dataclasses
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.security.ldap import LDAP_FIELDS, LDAPRecord, upass_chain
from uro.security.circle_security import CircleSecurity
from uro.security.field_encryption import FieldCipher
from uro.security.user_keys import UserKeyring
from uro.security import custody as cust
from uro.security.policy import PolicyURO
from uro.security.acl import ACL, ACLEntry, override_check
from uro.security.pki import PublicKeyURO, ROOT_CA_REGIONS
from uro.security.identity import Identity
from uro.security.encryption import decrypt
from uro.security.hashing import sha512
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 uPass six-step chain per RFC 58.2")
def c01():
    k = upass_chain(b"secret")
    k2 = upass_chain(b"secret")
    assert (k.step1, k.step2, k.step3) == (k2.step1, k2.step2, k2.step3)
    assert len({k.step1, k.step2, k.step3, k.step4, k.step5, k.step6}) == 6
    assert k.encryption_key == k.step3 and k.verify_key == k.step4
    assert upass_chain(b"other").step6 != k.step6
@check("02 LDAP record carries the eight schema fields")
def c02():
    rec = LDAPRecord.from_upass("alice", b"pw", "uuid-1")
    names = tuple(f.name for f in dataclasses.fields(rec))
    assert names == LDAP_FIELDS
    assert rec.password == upass_chain(b"pw").server_verify_key
@check("03 circle rings wrap and unwrap per RFC 57")
def c03():
    cs = CircleSecurity(b"K" * 64, b"O" * 32, b"A" * 32, b"P" * 64)
    assert cs.store_digest() == sha512(b"K" * 64)
    assert cs.unwrap_owner(cs.wrap_owner()) == b"K" * 64
    assert cs.unwrap_admin(cs.wrap_admin(2), 2) == b"K" * 64
    assert cs.unwrap_access(cs.wrap_access()) == b"P" * 64
    assert len(cs.end_user(b"U" * 32).entity) == 32
@check("04 field encryption with dual headers and grants")
def c04():
    fc = FieldCipher(b"F" * 64, b"U" * 32, b"M" * 32)
    ef = fc.encrypt_field(b"pii")
    assert fc.decrypt_field(ef, ef.header1, b"U" * 32) == b"pii"
    assert fc.decrypt_field(ef, ef.header2, b"M" * 32) == b"pii"
    g = fc.grant_access(b"G" * 32)
    assert decrypt(b"G" * 32, g["wrapped_key"]) == b"F" * 64
@check("05 user keyring wraps per RFC 53.1")
def c05():
    kr = UserKeyring.create(b"pw", b"E" * 64, b"PRIV" * 8, b"I" * 32)
    assert kr.unlock(b"pw") == b"PRIV" * 8
    assert kr.recovery_proof(b"I" * 32) == sha512(b"pw")
@check("06 custody chain and 2-way exchange per RFC 63")
def c06():
    chain = []
    rec = cust.send_custody(chain, b"S" * 32, b"obj")
    assert rec["hash_of_trust"] == chain[0]["hash"]
    sigs = cust.two_way_exchange(b"S" * 32, b"R" * 32, b"snd", b"rcv")
    assert cust.verify_two_way(b"S" * 32, b"R" * 32, b"snd", b"rcv", sigs) is True
    assert cust.verify_two_way(b"S" * 32, b"R" * 32, b"snd", b"tampered", sigs) is False
@check("07 policy override groups win per RFC 55.1")
def c07():
    pol = PolicyURO("p")
    user_acl = ACL(); user_acl.add(ACLEntry("alice", "read", True))
    group_acl = ACL(); group_acl.add(ACLEntry("alice", "read", False))
    pol.add_acl("user", user_acl)
    pol.add_acl("group", group_acl, override=True)
    assert pol.evaluate("user", "alice", "read") is False
    pol2 = PolicyURO("p2")
    deny_acl = ACL(); deny_acl.add(ACLEntry("bob", "write", False))
    ov_acl = ACL(); ov_acl.add(ACLEntry("bob", "write", True))
    pol2.add_acl("user", deny_acl)
    pol2.add_acl("admins", ov_acl, override=True)
    assert pol2.evaluate("user", "bob", "write") is True
@check("08 ACL override OR semantics per RFC 59.1")
def c08():
    acl = ACL()
    acl.add(ACLEntry("x", "r", True))
    acl.add(ACLEntry("x", "r", False))
    assert override_check(acl, "x", "r")[0] == "permit"
    ban_only = ACL(); ban_only.add(ACLEntry("x", "r", False))
    kind, obj = override_check(ban_only, "x", "r")
    assert kind == "ban" and obj is ban_only
    assert override_check(acl, "nobody", "r")[0] == "none"
@check("09 PKI regions and key lifecycle per RFC 51")
def c09():
    assert ROOT_CA_REGIONS == ("S.NA", "S.SA", "S.EU", "S.AF", "S.AS", "S.OC")
    pk = PublicKeyURO(b"pubkey")
    assert pk.is_valid() is True
    pk.revoke()
    assert pk.is_valid() is False
@check("10 identity verification and time binding per RFC 54")
def c10():
    ident = Identity("alice", b"pw")
    assert ident.verify_password(b"pw") is True
    assert ident.verify_password(b"nope") is False
    tok = ident.issue_token(indefinite=True)
    assert tok.indefinite is True
    ident.bind_time_uro("date-uro-1")
    assert ident.bound_time_uro == "date-uro-1"
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
