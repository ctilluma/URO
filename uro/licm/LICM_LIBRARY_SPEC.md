# LICM STANDARD LIBRARY — CREATION SPECIFICATION (uro.licm)
**Target location:** `uro/licm/` · **Consumers:** every dock + the Loom · **Mandate:** URO S1–S14

## 1. Purpose
One shared library that implements the Loom Integration Capability Manifest (LICM) contract so every dock exposes identical, URO-compliant observability/control surfaces, and the Loom renders them uniformly. No dock may hand-roll its own LICM endpoints.

## 2. Module layout
- `uro/licm/__init__.py` — public exports.
- `uro/licm/manifest.py` — `LICMManifest` pydantic model: dock_id, menu_label, icon, color_accent, pitch, views[], endpoints[], ws_channel, compliance{S2,S4,S7,S9}.
- `uro/licm/envelope.py` — `licm_envelope(urid_pair, payload, nte_state, provenance)`; provenance ∈ {LIVE, DERIVED, DEMO, UNMEASURED}; attaches `generated_at`, `inahash` seal (S7.2: Blake3-1024(SHA3-1024(msg))).
- `uro/licm/server.py` — `build_licm_router(dock_name, manifest, providers)` returning a FastAPI APIRouter with: GET `/licm/manifest`, GET `/licm/status`, GET `/licm/events` (SSE + JSON fallback, `since_seq` resume), POST `/licm/action` (ACL-gated), GET `/licm/nte`.
- `uro/licm/client.py` — `licm_call(dock, path, ...)` using `send_to_dock_async(dock_name=f"{dock}_{AURA_ENV}")` TCP-first, HTTP fallback (S9.10); measures real latency (S14.7).
- `uro/licm/events.py` — monotonic-seq ring buffer (default 2000), `record_event(kind, payload, provenance)`, gap-free resume.
- `uro/licm/provenance.py` — helpers: `derive_from_registry(...)`, `live(...)`, `unmeasured(reason)`; DERIVED payloads MUST include `derivation` string naming the source.

## 3. Provider contract (what each dock supplies)
`providers = {"status": callable, "events_source": callable, "actions": {name: callable}, "nte": callable}`. Callables may be async. Any provider may raise `LicmUnmeasured(reason)`.

## 4. Hard rules
1. Every response is a URO with `urid_pair` (S2) and normalized 24-axis `nte_state` via `normalize_nte_state` (S4.3).
2. ACL tiers (S7.9): read=authenticated operator; write=varuos_admin/admin/root/dock-PKI; control=varuos_admin only; denials emit `acl_denied` event + immutable ledger entry.
3. Append-only event history; control receipts written BEFORE effects (S14.4).
4. No silent fallbacks: upstream errors surface verbatim with status codes; missing measurements return provenance=UNMEASURED with reason, never fabricated numbers.
5. Inter-dock transport only via `client.licm_call` (S9.10); env-suffixed dock names mandatory.
6. Loom WebSocket channel name = manifest.ws_channel; envelope includes `seq`, `ts`, `event`, `payload`, `nte_state`.

## 5. Acceptance criteria for the library build
- Unit tests: envelope sealing, seq monotonicity, provenance enum enforcement, ACL matrix, SSE resume after gap.
- Integration test: mount router on a stub dock; Loom proxy fetches manifest+status+events; kill dock mid-stream and verify resume via since_seq.
- QA gate: `test_no_fabricated_metrics` — any status field without LIVE/DERIVED/UNMEASURED provenance fails the suite.
