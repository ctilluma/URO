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
# === FILE: tests/boot_suite.py ===
# PURPOSE: Phase 14 validation: 16-step boot order and halt semantics,
#          child boot queues and ACK, four-step self-check quarantine.
# === END FILE HEADER ===
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.boot import BOOT_STEPS, BootRunner, ChildBoot, SELF_CHECK_STEPS, self_check
from uro.core.urid import URID
from uro.nte.state import NTEStateURO
def _sealed(**kw):
    st = NTEStateURO(urid1=kw.get("u1", URID.new()), urid2=URID.new())
    st.seal()
    return st
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 sixteen boot steps in canonical order")
def c01():
    assert len(BOOT_STEPS) == 16
    assert BOOT_STEPS[0] == "loader_verify" and BOOT_STEPS[-1] == "system_ready"
@check("02 full run reaches READY")
def c02():
    r = BootRunner({s: (lambda ctx: True) for s in BOOT_STEPS}).run()
    assert r["status"] == "READY" and r["completed"] == BOOT_STEPS
@check("03 halt on failed step preserves order")
def c03():
    handlers = {s: (lambda ctx: True) for s in BOOT_STEPS}
    handlers["security_init"] = lambda ctx: False
    r = BootRunner(handlers).run()
    assert r["status"] == "HALTED" and r["step"] == "security_init"
    assert len(r["completed"]) == BootRunner.step_index("security_init")
@check("04 default handlers are permissive noops")
def c04():
    assert BootRunner().run()["status"] == "READY"
@check("05 child responses release only on ACK")
def c05():
    cb = ChildBoot("seal", _sealed())
    cb.queue_response("r1")
    cb.queue_response("r2")
    assert cb.drain_on_ack(False) == []
    assert cb.drain_on_ack(True) == ["r1", "r2"]
    assert cb.drain_on_ack(True) == []
@check("06 child seal verification detects tampering")
def c06():
    st = _sealed()
    cb = ChildBoot("seal", st)
    assert cb.boot()["verified"] is True
    st.levels[list(st.levels)[0]] = 99.0
    assert cb.verify_child() is False
@check("07 sealed object passes all four self-checks")
def c07():
    r = self_check(_sealed())
    assert all(r[k] is True for k in SELF_CHECK_STEPS)
    assert r["quarantined"] is False
@check("08 broken seal quarantines")
def c08():
    st = _sealed()
    st.inahash = "deadbeef"
    r = self_check(st)
    assert r["inahash_verify"] is False and r["quarantined"] is True
@check("09 out-of-bounds NTE quarantines")
def c09():
    st = _sealed()
    key = list(st.levels)[0]
    st.levels[key] = 150.0
    r = self_check(st)
    assert r["nte_bounds"] is False and r["quarantined"] is True
@check("10 zero URID fails integrity")
def c10():
    st = _sealed(u1=URID.zero())
    r = self_check(st)
    assert r["urid_integrity"] is False and r["quarantined"] is True
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
