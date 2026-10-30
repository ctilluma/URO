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
# === FILE: tests/interchange_suite.py ===
# PURPOSE: Phase 9 validation: AUPI wrapper translation, container caching,
#          header delegation, binary/JSON round-trips, hot-swap identity,
#          self-loading, priority precedence and retention.
# === END FILE HEADER ===
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.aupi import AUPI, typed_uro
from uro import interchange
from uro.core.header import build_header as core_build
from uro.core.uro import URO
from uro.exceptions import TranslationError
from uro.hot_swap import hot_swap
from uro.priority import PriorityQueue, RETENTION_SECONDS
from uro.relations.association import Association, ConnectionType
from uro.self_loading import SelfLoader
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 Number to Phone Number wrapper per RFC 84")
def c01():
    a = AUPI()
    a.register("number", "phone", lambda v: "(" + str(v)[:3] + ") " + str(v)[3:])
    out = a.translate(typed_uro("number", "5551234"), "phone")
    assert out.payload["type"] == "phone"
    assert out.payload["value"] == "(555) 1234"
@check("02 translator chains resolve via pathing")
def c02():
    a = AUPI()
    a.register("a", "b", lambda x: x + 1)
    a.register("b", "c", lambda x: x * 2)
    assert len(a.find_path("a", "c")) == 2
    assert a.translate_value(1, "a", "c") == 4
@check("03 missing path raises TranslationError")
def c03():
    a = AUPI()
    try:
        a.translate_value(1, "a", "zzz")
        raise AssertionError("missing path accepted")
    except AssertionError:
        raise
    except TranslationError:
        pass
@check("04 translation records a PATH association")
def c04():
    a = AUPI()
    a.register("number", "phone", lambda v: v)
    src = typed_uro("number", 1)
    out = a.translate(src, "phone")
    assert any(getattr(x, "connection_type", None) == ConnectionType.PATH for x in src.associations)
@check("05 container resolution caches wrapper paths")
def c05():
    a = AUPI()
    a.register("number", "phone", lambda v: v)
    src = typed_uro("number", 9)
    a.resolve_container(src, "phone")
    a.resolve_container(src, "phone")
    assert len(a._container_cache) == 1
@check("06 interchange header delegates to canonical builder")
def c06():
    blob = interchange.build_header(1, 2, 3)
    assert blob == core_build(1, 2, 3)
    assert interchange.parse_header(blob) == (1, 2, 3, 0)
@check("07 binary encode/decode round-trip")
def c07():
    u = URO.new(payload={"k": 1})
    back = interchange.decode_uro(interchange.encode_uro(u))
    assert back.urid1 == u.urid1 and back.urid2 == u.urid2
    assert back.payload == {"k": 1}
@check("08 JSON round-trip")
def c08():
    u = URO.new(payload={"k": 2})
    back = interchange.uro_from_json(interchange.uro_to_json(u))
    assert back.urid1 == u.urid1 and back.payload == {"k": 2}
@check("09 hot-swap preserves URID1 and carries associations")
def c09():
    old = URO.new()
    Association(old, URO.new())
    rec = hot_swap(old, lambda: URO.new())
    assert rec.urid1 == old.urid1
    assert len(rec.carried_associations) == 1
    try:
        hot_swap(old, lambda: URO.new(), verify=lambda u: False)
        raise AssertionError("failed verification accepted")
    except AssertionError:
        raise
    except ValueError:
        pass
@check("10 priority precedence, retention, self-loading")
def c10():
    q = PriorityQueue()
    q.push("low", "L")
    q.push("crit", "C")
    q.push("normal", "N")
    assert [q.pop(), q.pop(), q.pop()] == ["C", "N", "L"]
    assert RETENTION_SECONDS["crit"] > RETENTION_SECONDS["low"]
    sl = SelfLoader()
    sl.pull_config({"mode": "fast"})
    sl.ensure_parent_code("p1", "code")
    assert sl.compile_local("p1") is True
    assert sl.compile_local("missing") is False
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
