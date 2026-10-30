# LICM DOCK INTEGRATION GUIDE (per-dock checklist)
**You are a dock of the V.A.U.R.O.S. Metaswarm. The Loom renders you via the LICM standard. Follow exactly.**

## Step 1 — Declare your manifest
In your `api.py`, import `from uro.licm import LICMManifest, build_licm_router` and define your manifest: dock_id, menu_label, Lucide icon name, color accent (unique), one-line pitch, view list, ws_channel `<dock>_<domain>_events`.

## Step 2 — Implement providers with REAL data only
- `status()` → return your true operational metrics from live internal state (queues, caches, engines). If a metric does not exist yet, raise `LicmUnmeasured("reason")`. NEVER invent numbers.
- `events_source(since_seq)` → yield genuine lifecycle events from your internal ring buffer (use `uro.licm.events`).
- `actions` → map operator actions to real functions; each writes an immutable control receipt BEFORE executing.
- `nte()` → return your engine's current 24-axis state (S4).

## Step 3 — Mount the router
`app.include_router(build_licm_router("<dock>", MANIFEST, PROVIDERS))`. Startup must also call `install_tcp_listener(app, dock_name=f"<dock>_{AURA_ENV}")` (S9.10).

## Step 4 — Provenance discipline
Every value you return is tagged by the library. If you derive a value from another source (e.g., swarm registry), the library tags it DERIVED and you must supply the derivation string. The Loom badges LIVE/DERIVED/UNMEASURED/DEMO from this tag — your UI honesty depends on it.

## Step 5 — Loom-facing endpoints
Expose the domain endpoints your LICM manifest promises (e.g. `/api/<dock>/status`) by delegating to the same providers, so legacy Loom views and the LICM router share one source of truth.

## Step 6 — Test obligations (S14.6 gates)
Add QA tests: manifest validates; status returns provenance-tagged payload; events seq monotonic; ACL denies unprivileged control; `test_no_fabricated_metrics` passes; dock-name env-suffix asserted.

## Step 7 — Register with the Loom
Submit your manifest block (identity, views, API contract, WS events, compliance check) as a LICM document. The Loom adds your menu entry beneath Cognitive using your icon/color.
