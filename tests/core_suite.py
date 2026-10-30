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
# === FILE: tests/core_suite.py ===
# PURPOSE: Phase 2 validation: URID roundtrip, link width, header integrity,
#          component enforcement, inheritance, datetime epoch semantics.
# === END FILE HEADER ===
import sys
from pathlib import Path
from types import SimpleNamespace
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.constants import URO_EPOCH
from uro.core.urid import URID
from uro.core.uro import URO
from uro.core.header import build_header, parse_header, verify_header
from uro.core.components import COMPONENTS, missing_components, enforce_components
from uro.core.inheritance import resolve_capability
from uro.core.datetime_uro import DateURO
from uro.exceptions import HeaderIntegrityError, UROStructureError
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 URID hex roundtrip")
def c01():
    u = URID.new()
    assert URID.from_hex(u.to_hex()) == u
@check("02 URO link is 512 bits")
def c02():
    assert len(URO.new().link()) == 64
@check("03 header total width")
def c03():
    assert len(build_header(1, 2, 3)) == 64
@check("04 header verifies clean")
def c04():
    assert verify_header(build_header(10, 20, 30))
@check("05 header tamper detected")
def c05():
    blob = bytearray(build_header(10, 20, 30))
    blob[0] ^= 0xFF
    try:
        parse_header(bytes(blob))
        raise AssertionError("tamper not detected")
    except HeaderIntegrityError:
        pass
@check("06 bare URO fails component enforcement")
def c06():
    u = URO.new()
    assert missing_components(u)
    try:
        enforce_components(u)
        raise AssertionError("enforce did not raise")
    except UROStructureError:
        pass
@check("07 populated object passes enforcement")
def c07():
    obj = SimpleNamespace(urid1=1, urid2=2, header=b"h", payload=b"p", nte={},
                          acl=[], personality={}, capabilities={},
                          associations=[], children={}, inahash="x")
    enforce_components(obj)
@check("08 capability resolves through parent chain")
def c08():
    parent = SimpleNamespace(capabilities={"think": "v1"}, parent=None)
    child = SimpleNamespace(capabilities={}, parent=parent)
    assert resolve_capability(child, "think") == "v1"
@check("09 DateURO epoch anchor")
def c09():
    d = DateURO.from_datetime(URO_EPOCH)
    assert abs(d.offset_seconds) < 1e-9
    assert d.to_datetime() == URO_EPOCH
@check("10 expiration renew vs delete")
def c10():
    r = DateURO(0.0, expires_at=1.0, renew=True)
    d = DateURO(0.0, expires_at=1.0, renew=False)
    assert r.expiration_action(now_seconds=2.0) == "renew"
    assert d.expiration_action(now_seconds=2.0) == "delete"
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
