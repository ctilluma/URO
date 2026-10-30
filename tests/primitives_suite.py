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
# === FILE: tests/primitives_suite.py ===
# PURPOSE: Phase 1 validation suite for RFC 1.2 bit widths, 6.2 epoch, 110 currency.
# === END FILE HEADER ===
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from uro import constants as c

checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap

@check("01 UUID is 128 bits")
def c01():
    assert c.UUID_BITS == 128

@check("02 URID is 256 bits")
def c02():
    assert c.URID_BITS == 256

@check("03 URO is 512 bits")
def c03():
    assert c.URO_BITS == 512

@check("04 Hash is 1024 bits")
def c04():
    assert c.HASH_BITS == 1024

@check("05 NTE State is 1536 bits")
def c05():
    assert c.NTE_STATE_BITS == 1536

@check("06 Epoch is 14-MAY-1973 00:12:24")
def c06():
    assert c.URO_EPOCH.year == 1973
    assert c.URO_EPOCH.month == 5
    assert c.URO_EPOCH.day == 14
    assert c.URO_EPOCH.hour == 0
    assert c.URO_EPOCH.minute == 12
    assert c.URO_EPOCH.second == 24

@check("07 InSPativo is 1000 InSPaneda")
def c07():
    assert c.INSPANEDA_PER_INSPATIVO == 1000

@check("08 Network tax is 10%")
def c08():
    assert c.TRANSACTION_FEE_PERCENT == 10

@check("09 OPARError exists")
def c09():
    from uro.exceptions import OPARError
    assert issubclass(OPARError, Exception)

@check("10 types.py Protocols exist")
def c10():
    from uro.types import UROCapable, OPARCapable
    assert UROCapable and OPARCapable

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
