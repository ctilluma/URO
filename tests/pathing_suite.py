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
# === FILE: tests/pathing_suite.py ===
# PURPOSE: Phase 8 validation: connector matrix, TV ladder, beacon sequences,
#          onion layering, CRO matrix, combine/priority/hash, stack, swarms.
# === END FILE HEADER ===
import hashlib
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uro.pathing.connectors import Connector, ConnectorType
from uro.pathing.trust import TrustValueProtocol
from uro.pathing.beacons import (BeaconType, PARENT_SEQUENCE, CHILD_SEQUENCE,
                                 INTERFACE_SEQUENCE)
from uro.pathing.onion import OnionRouter
from uro.pathing.cro_matrix import resolve_cro
from uro.pathing.path_ops import combine_paths, path_priority, fastest_first, path_hash
from uro.pathing.stack_processing import ProcessingStack
from uro.pathing.swarms import SwarmObject, classify_routing
checks = []
def check(name):
    def wrap(fn):
        checks.append((name, fn))
        return fn
    return wrap
@check("01 connector matrix per RFC 80 incl SELF rows")
def c01():
    assert Connector.from_urid_pair("0", "B").type == ConnectorType.OUTPUT
    assert Connector.from_urid_pair("A", "0").type == ConnectorType.INPUT
    assert Connector.from_urid_pair("S", "B", "S").type == ConnectorType.LINK
    assert Connector.from_urid_pair("A", "S", "S").type == ConnectorType.CHILD
    assert Connector.from_urid_pair("A", "B", "S").type == ConnectorType.PATH
    assert Connector.from_urid_pair("A", "A").type == ConnectorType.LINK
@check("02 TV consensus ladder per RFC 73")
def c02():
    tvp = TrustValueProtocol()
    same = [{"value": 7}] * 10
    r = tvp.evaluate_responses(same)
    assert r["status"] == "consensus" and r["trust_points"] == 1 and r["actions"] == ["use_result"]
    n9 = [{"value": 7}] * 9 + [{"value": 8}]
    r = tvp.evaluate_responses(n9)
    assert r["status"] == "tv_check" and r["actions"] == ["use_high_tv_responder"]
    n8 = [{"value": 7}] * 8 + [{"value": 8}] * 2
    r = tvp.evaluate_responses(n8)
    assert r["status"] == "deep_check"
    assert "explore_hypotheses" in r["actions"] and "ask_minority_deep_check" in r["actions"]
    n5 = [{"value": 7}] * 5 + [{"value": 8}] * 5
    r = tvp.evaluate_responses(n5)
    assert r["status"] == "reanalyze" and r["actions"] == ["reanalyze_query"]
@check("03 beacon sequences per RFC 74")
def c03():
    assert INTERFACE_SEQUENCE == tuple(BeaconType)
    assert len(PARENT_SEQUENCE) == 3 and PARENT_SEQUENCE[0][1] == "0 0 CRO"
    assert CHILD_SEQUENCE == ("native", "processable", "understood", "request_beacon_response")
@check("04 onion layers expose only self and next")
def c04():
    router = OnionRouter()
    enc = router.encrypt_path(["A", "B", "C"], {"m": 1})
    assert enc["hop"] == "A"
    d = router.decrypt_layer(enc, "A")
    assert d["next_hop"] == "B"
    layer_b = d["inner"]
    assert layer_b["hop"] == "B"
    d2 = router.decrypt_layer(layer_b, "B")
    assert d2["next_hop"] == "C"
    try:
        router.decrypt_layer(enc, "B")
        raise AssertionError("wrong hop accepted")
    except AssertionError:
        raise
    except Exception:
        pass
@check("05 CRO resolution matrix rows per RFC 72")
def c05():
    assert resolve_cro(0, 0, 0, 0) == "Source / Destination ACL / Personality"
    assert resolve_cro(0, 0, 0, 1) == "Return new non-source dependent CRO"
    assert resolve_cro(0, 1, 0, 0) == "Path to handle CRO1"
    assert resolve_cro(1, 0, 1, 0) == "Path to convert type CRO1 to CRO2"
    assert resolve_cro(1, 1, 1, 1) == "Return CRO2 from Source / Data CRO1"
@check("06 path combine rule per RFC 79")
def c06():
    assert combine_paths(("U1", "U2"), ("U3", "U1")) == ("U3", "U2")
    assert combine_paths(("U1", "U2"), ("U3", "U9")) is None
@check("07 priority sum and fastest-first per RFC 70.3")
def c07():
    assert path_priority([1, 2, 3]) == 6
    assert fastest_first([3, 0, 2]) == [0, 2, 3]
@check("08 path hash is SHA512(src, dest)")
def c08():
    assert path_hash("A", "B") == hashlib.sha512(b"AB").hexdigest()
    assert len(path_hash("A", "B")) == 128
@check("09 stack processing per RFC 77")
def c09():
    st = ProcessingStack()
    st.push("a")
    st.push("b")
    st.add_result_item("c")
    assert st.items == ["c", "a", "b"]
    assert st.process_top(lambda x: x) == "b"
    assert st.pop_as_far_as(lambda x: x == "b") == ["b"]
    assert st.items == ["c", "a"]
@check("10 swarm routing tuples per RFC 81")
def c10():
    assert classify_routing("U", "0") == "request_object"
    assert classify_routing("0", "U") == "attached_data_send"
    assert classify_routing("U", "U") == "respond_urid2_from_urid1"
    sw = SwarmObject()
    assert sw.communications == [] and sw.potentiators == [] and sw.associations == []
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
