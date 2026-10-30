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


from __future__ import annotations

import unittest

from fastapi import HTTPException

from uro.licm import (
    EventRing,
    LicmProvenanceError,
    Provenance,
    build_licm_router,
    compute_envelope_seal,
    derive_from_registry,
    licm_envelope,
    live,
    make_urid_pair,
    normalize_provenance,
    unmeasured,
    validate_status_payload,
)
from uro.licm import acl
from uro.licm.server import ActionRequest


def good_status():
    return {
        "uptime_s": live(123.4),
        "memory_mb": derive_from_registry(256, derivation="stub.registry.memory_rss_mb"),
        "queue_depth": unmeasured("no queue sensor"),
        "nested": {
            "requests_total": live(7),
        },
    }


def bad_status():
    return {"uptime_s": 123.4}


def nte_provider():
    return {"glutamate": 70.0, "focus": 61.0}


async def noop_action(args):
    return {"echo": args}


class LicmAcceptanceSuite(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.manifest = {
            "dock_id": "stub-dock",
            "menu_label": "Stub Dock",
            "icon": "flask",
            "color_accent": "#33cc99",
            "pitch": "Stub dock for LICM acceptance",
            "views": [{"id": "status", "label": "Status", "source": "/licm/status"}],
            "endpoints": [{"path": "/licm/status", "method": "GET", "tier": "read"}],
            "ws_channel": "stub.licm.events",
            "compliance": {"S2": True, "S4": True, "S7": True, "S9": True},
        }
        self.providers = {
            "status": good_status,
            "nte": nte_provider,
            "actions": {
                "noop": noop_action,
                "danger": {"handler": noop_action, "tier": "control"},
            },
        }
        self.router = build_licm_router("stubdock", self.manifest, self.providers)
        self.runtime = self.router.licm
        self.operator = {"x_uro_principal": "operator-1", "x_uro_role": "operator"}
        self.root = {"x_uro_principal": "root", "x_uro_role": "root"}
        self.varuos_admin = {"x_uro_principal": "vauros-admin", "x_uro_role": "varuos_admin"}

    async def test_001_envelope_sealing_and_nte_normalization(self):
        envelope = licm_envelope(
            make_urid_pair("stubdock", "test.object"),
            {"metric": live(1)},
            {"glutamate": 60.0},
            live("ok"),
        )

        self.assertEqual(envelope["nte_state"]["axis_count"], 24)
        self.assertEqual(len(envelope["nte_state"]["levels"]), 24)
        self.assertEqual(envelope["nte_state"]["levels"]["GLUTAMATE"], 60.0)
        self.assertEqual(envelope["nte_state"]["levels"]["GABA"], 50.0)

        recomputed, _ = compute_envelope_seal(envelope)
        self.assertEqual(envelope["inahash"], recomputed)

        tampered = dict(envelope)
        tampered["payload"] = {"metric": live(2)}
        tampered_seal, _ = compute_envelope_seal(tampered)
        self.assertNotEqual(envelope["inahash"], tampered_seal)

    async def test_002_event_sequence_monotonicity(self):
        ring = EventRing(capacity=5)
        seqs = [ring.record("test", {"i": i}, Provenance.LIVE)["seq"] for i in range(5)]
        self.assertEqual(seqs, [1, 2, 3, 4, 5])
        self.assertEqual(ring.latest()["seq"], 5)

    async def test_003_provenance_enum_enforcement(self):
        self.assertEqual(normalize_provenance("live")["kind"], "LIVE")
        self.assertEqual(normalize_provenance({"kind": "DERIVED", "derivation": "test.source"})["kind"], "DERIVED")

        with self.assertRaises(LicmProvenanceError):
            normalize_provenance("bogus")

        with self.assertRaises(LicmProvenanceError):
            normalize_provenance({"kind": "DERIVED"})

        with self.assertRaises(LicmProvenanceError):
            normalize_provenance({"kind": "UNMEASURED"})

    async def test_004_acl_matrix(self):
        self.assertTrue(acl.authorize("op", "operator", "read"))
        self.assertFalse(acl.authorize("op", "operator", "write"))
        self.assertFalse(acl.authorize("op", "operator", "control"))

        self.assertTrue(acl.authorize("admin", "admin", "read"))
        self.assertTrue(acl.authorize("admin", "admin", "write"))
        self.assertFalse(acl.authorize("admin", "admin", "control"))

        self.assertTrue(acl.authorize("va", "varuos_admin", "read"))
        self.assertTrue(acl.authorize("va", "varuos_admin", "write"))
        self.assertTrue(acl.authorize("va", "varuos_admin", "control"))

        self.assertTrue(acl.authorize("root", "root", "write"))
        self.assertFalse(acl.authorize("root", "root", "control"))

        self.assertTrue(acl.authorize("pki", "dock-pki", "write"))
        self.assertFalse(acl.authorize(None, "operator", "read"))

    async def test_005_acl_denial_emits_event_and_ledger_entry(self):
        before_events = len(self.runtime.ring)
        before_ledger = len(self.runtime.ledger.entries)

        with self.assertRaises(HTTPException):
            await self.runtime.handlers["status"]()

        self.assertEqual(len(self.runtime.ring), before_events + 1)
        self.assertEqual(len(self.runtime.ledger.entries), before_ledger + 1)
        self.assertEqual(self.runtime.ring.latest()["event"], "acl_denied")
        self.assertEqual(self.runtime.ledger.entries[-1]["event"], "acl_denied")

    async def test_006_action_acl_receipts_and_effects(self):
        with self.assertRaises(HTTPException):
            await self.runtime.handlers["action"](
                body=ActionRequest(action="noop", args={}, tier="write"),
                x_uro_principal="op",
                x_uro_role="operator",
            )
        self.assertEqual(self.runtime.ring.latest()["event"], "acl_denied")

        response = await self.runtime.handlers["action"](
            body=ActionRequest(action="noop", args={"x": 1}, tier="write"),
            x_uro_principal="root",
            x_uro_role="root",
        )
        self.assertEqual(response["payload"]["result"]["echo"], {"x": 1})
        self.assertEqual(response["payload"]["receipt"]["event"], "control_receipt")
        self.assertEqual(response["payload"]["effect"]["event"], "action_effect")
        self.assertLess(response["payload"]["receipt"]["seq"], response["payload"]["effect"]["seq"])

        with self.assertRaises(HTTPException):
            await self.runtime.handlers["action"](
                body=ActionRequest(action="danger", args={}, tier="control"),
                x_uro_principal="root",
                x_uro_role="root",
            )

        response_control = await self.runtime.handlers["action"](
            body=ActionRequest(action="danger", args={}, tier="control"),
            x_uro_principal="va",
            x_uro_role="varuos_admin",
        )
        self.assertEqual(response_control["payload"]["receipt"]["payload"]["tier"], "control")

    async def test_007_sse_resume_after_gap(self):
        ring = self.runtime.ring
        ring.capacity = 3

        for i in range(5):
            ring.record("metric", {"i": i}, Provenance.LIVE)

        events, gap, oldest, latest = ring.since(1)
        self.assertTrue(gap)
        self.assertEqual(oldest, 3)
        self.assertEqual([event["seq"] for event in events], [3, 4, 5])
        self.assertEqual(latest, 5)

        response = await self.runtime.handlers["events"](
            since_seq=1,
            stream=True,
            accept="text/event-stream",
            **self.operator,
        )
        self.assertEqual(response.media_type, "text/event-stream")

        chunks = []
        async for chunk in response.body_iterator:
            chunks.append(chunk)
        text = "".join(chunks)

        self.assertIn("licm.resume", text)
        self.assertIn("licm.gap", text)
        self.assertIn('"seq": 3', text)

    async def test_008_integration_stub_dock_loom_proxy_and_restart_resume(self):
        manifest_env = await self.runtime.handlers["manifest"](**self.operator)
        self.assertEqual(manifest_env["payload"]["dock_id"], "stub-dock")
        self.assertEqual(manifest_env["provenance"]["kind"], "DERIVED")

        status_env = await self.runtime.handlers["status"](**self.operator)
        self.assertEqual(status_env["payload"]["uptime_s"]["provenance"], "LIVE")
        self.assertEqual(status_env["payload"]["memory_mb"]["derivation"], "stub.registry.memory_rss_mb")
        self.assertEqual(status_env["payload"]["queue_depth"]["provenance"], "UNMEASURED")

        await self.runtime.handlers["action"](
            body=ActionRequest(action="noop", args={"x": 1}),
            **self.root,
        )

        events_env = await self.runtime.handlers["events"](
            since_seq=0,
            stream=False,
            accept="application/json",
            **self.operator,
        )
        self.assertFalse(events_env["payload"]["gap"])
        latest = events_env["payload"]["latest_seq"]
        self.assertGreaterEqual(latest, 2)

        snapshot = self.runtime.ring.snapshot()

        restarted_router = build_licm_router("stubdock", self.manifest, self.providers)
        restarted_runtime = restarted_router.licm
        restarted_runtime.ring.load_snapshot(snapshot)

        await restarted_runtime.handlers["action"](
            body=ActionRequest(action="noop", args={"x": 2}),
            **self.root,
        )

        resumed_env = await restarted_runtime.handlers["events"](
            since_seq=latest,
            stream=False,
            accept="application/json",
            **self.operator,
        )
        self.assertFalse(resumed_env["payload"]["gap"])
        self.assertTrue([event for event in resumed_env["payload"]["events"] if event["seq"] > latest])

    async def test_009_qa_gate_no_fabricated_metrics(self):
        validate_status_payload(good_status())

        with self.assertRaises(LicmProvenanceError):
            validate_status_payload({"bad": 1})

        with self.assertRaises(LicmProvenanceError):
            validate_status_payload({"bad": {"value": 1}})

        with self.assertRaises(LicmProvenanceError):
            validate_status_payload({"bad": {"value": 1, "provenance": "DEMO"}})

        with self.assertRaises(LicmProvenanceError):
            validate_status_payload({"bad": {"value": 1, "provenance": "DERIVED"}})

        bad_router = build_licm_router(
            "stubdock",
            self.manifest,
            {"status": lambda: {"bad": 1}, "nte": lambda: {}},
        )

        with self.assertRaises(HTTPException) as ctx:
            await bad_router.licm.handlers["status"](**self.operator)
        self.assertEqual(ctx.exception.status_code, 500)

    async def test_010_client_env_suffix_and_latency_measurement(self):
        import uro.licm.client as licm_client

        async def fake_send(**kwargs):
            return {"status_code": 200, "body": {"ok": True}, "transport": "tcp"}

        original = licm_client.send_to_dock_async
        licm_client.send_to_dock_async = fake_send
        try:
            result = await licm_client.licm_call("cognitive", "/licm/status", method="GET")
            self.assertTrue(result["ok"])
            self.assertTrue(result["dock"].endswith("_" + licm_client.AURA_ENV))
            self.assertGreaterEqual(result["latency_s"], 0.0)
        finally:
            licm_client.send_to_dock_async = original


if __name__ == "__main__":
    unittest.main(verbosity=2)
