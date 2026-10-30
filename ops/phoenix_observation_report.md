# PHOENIX DOCK — OBSERVATION REPORT (OPAR Pass 1)

- **Generated:** 2026-10-22T03:59:57Z
- **Repo root:** /home/christian/viridant-auraforge
- **HEAD:** 09797cfae
- **Mode:** READ-ONLY. No source file was modified by this pass.
- **Governing sections:** S13.1, S13.2, S13.5, S9.10, S7.11, S5, S4.3, S3

## 1. Topology & Inventory

| Artifact | Count |
|---|---|
| Python files in dock (excl. __pycache__) | 578 |
| capabilities/cap_*.py | 24 |
| domains/dom_*.py | 24 |
| cns/hyper_nodes/node_*.py | 243 |
| cns/hyper_nodes/ algorithm modules (non-node) | 241 |

Declared in PHOENIX_ARCHITECTURE.md: `24 Domains × 12 Capabilities × 4-Fold Growth = 1,152 Implementations`

Declared in PHOENIX_ARCHITECTURE_FULL.md title: `24 Capabilities x 24 Domains`; body: `24 Capabilities in 6 Groups`

**Observed reality: 24 capabilities, 24 domains.** The two architecture documents disagree with each other and with the tree. See §6.

## 2. Package Hygiene

| Check | Result |
|---|---|
| capabilities/__init__.py | **ABSENT — not an importable package** |
| domains/__init__.py | **ABSENT — not an importable package** |
| cns/__init__.py | present |
| cns/hyper_nodes/__init__.py | present |
| docks/__init__.py | **ABSENT — not an importable package** |
| stray backup artifacts | cns/registry.py.deepforge_bak,main.py.vauros_bak |
| __pycache__ dirs | 5 |

## 3. S13.2 Per-Dock Mandatory Checklist Audit

Counts = number of .py files in the dock containing the pattern.

| S13.2 Requirement | Files | Status |
|---|---|---|
| URID pairs (S2.1)                              |  578 | PRESENT |
| OPAR lifecycle (S3)                            |  320 | PRESENT |
| NTE normalizer (S4.3)                          |    0 | **MISSING** |
| Raw 24-axis NTE reference (S4.2)               |  578 | PRESENT |
| INAHASH (S7.2)                                 |  578 | PRESENT |
| ACL enforcement (S7.9)                         |    0 | **MISSING** |
| PKI / signatures (S7.5-7.6)                    |   80 | PRESENT |
| Custody + 2-way exchange (S7.8)                |  578 | PRESENT |
| Beacons (S9.7)                                 |    1 | PRESENT |
| Memory tiers (S8.1)                            |   62 | PRESENT |
| Cognitive decay 0.95^age (S8.5)                |   56 | PRESENT |
| Sleep / downtime reflection (S8.6-8.7)         |   16 | PRESENT |
| Priority processing (S11.5)                    |   56 | PRESENT |
| Quad-Capability (S5.1)                         |  202 | PRESENT |
| Hot-swap (S11.2)                               |    4 | PRESENT |
| InSPaneda economy (S10.1)                      |    7 | PRESENT |
| Time URO (S10.5)                               |    0 | **MISSING** |
| ANS integration (S10.6)                        |    1 | PRESENT |
| install_tcp_listener wired (S9.10)             |    1 | PRESENT |
| send_to_dock_async used (S9.10)                |    1 | PRESENT |
| Aegis integration (S7.11)                      |   23 | PRESENT |
| Host Controller delegation (S13.1)             |   57 | PRESENT |

## 4. S13.5 / S13.4 Endpoint Surface

S13.5 REQUIRES Phoenix to implement `POST /phoenix/restore` accepting dock_name + reason.

```
/home/christian/viridant-auraforge/docks/phoenix/api.py:57:@app.get("/health")
/home/christian/viridant-auraforge/docks/phoenix/api.py:61:@app.get("/phoenix/status")
/home/christian/viridant-auraforge/docks/phoenix/api.py:65:@app.post("/phoenix/resurrect")
/home/christian/viridant-auraforge/docks/phoenix/api.py:69:@app.post("/phoenix/isolate")
/home/christian/viridant-auraforge/docks/phoenix/api.py:73:@app.post("/phoenix/chrysalis")
/home/christian/viridant-auraforge/docks/phoenix/api.py:77:@app.post("/uro/ingest")
/home/christian/viridant-auraforge/docks/phoenix/api.py:87:@app.post("/uro/register_swarm")
/home/christian/viridant-auraforge/docks/phoenix/api.py:115:@app.get("/uro/self_model")
/home/christian/viridant-auraforge/docks/phoenix/api.py:136:@app.post("/uro/understand")
/home/christian/viridant-auraforge/docks/phoenix/api.py:170:@app.post("/uro/dispatch")
/home/christian/viridant-auraforge/docks/phoenix/api.py:227:@app.post("/uro/coordinate")
/home/christian/viridant-auraforge/docks/phoenix/api.py:322:@app.get("/uro/telemetry")
/home/christian/viridant-auraforge/docks/phoenix/api.py:346:@app.post("/uro/telemetry/record")
/home/christian/viridant-auraforge/docks/phoenix/routes.py:78:@router.get("/health")
/home/christian/viridant-auraforge/docks/phoenix/routes.py:90:@router.get("/phoenix/status")
/home/christian/viridant-auraforge/docks/phoenix/routes.py:105:@router.post("/phoenix/resurrect")
/home/christian/viridant-auraforge/docks/phoenix/routes.py:117:@router.post("/phoenix/quarantine")
/home/christian/viridant-auraforge/docks/phoenix/routes.py:134:@router.post("/phoenix/rollback")
/home/christian/viridant-auraforge/docks/phoenix/routes.py:163:@router.post("/phoenix/graduate")
/home/christian/viridant-auraforge/docks/phoenix/routes.py:178:@router.post("/phoenix/predict")
/home/christian/viridant-auraforge/docks/phoenix/routes.py:198:@router.get("/phoenix/domains")
/home/christian/viridant-auraforge/docks/phoenix/routes.py:233:@router.get("/phoenix/audit")
```

## 5. S9.10 / S14.7 Transport Compliance

| Metric | Value |
|---|---|
| files with raw httpx client calls | 1 |
| files with raw `requests.` calls | 0 |
| files using send_to_dock_async | 1 |
| files using bus.emit_uro_and_await | 40 |
| files using bus.emit_uro | 77 |
| files using async_send_uro_tcp | 0 |
| files wiring install_tcp_listener | 1 |

Raw httpx offenders (if any):
```
docks/phoenix/api.py
```

## 6. Architecture Document Consistency Review

| Source | Claim |
|---|---|
| PHOENIX_ARCHITECTURE.md header | ARCHITECTURE: 24 Domains × 12 Capabilities × 4-Fold Growth = 1,152 Implementations |
| PHOENIX_ARCHITECTURE_FULL.md title | # 24 Capabilities x 24 Domains x Zero-Downtime Healing & Execution |
| PHOENIX_ARCHITECTURE_FULL.md body | ## 24 Capabilities in 6 Groups |
| PHOENIX_BLUEPRINT.py logger | "🔥 Phoenix Architectural Blueprint loaded. 5 Domains defined. Boundaries enforced.") |
| Filesystem capabilities/ | 24 cap_*.py |
| Filesystem domains/ | 24 dom_*.py |

PHOENIX_ARCHITECTURE.md only specifies Domains 1-11 in detail; Domains 12-24 are listed as bare headings under `[Continued in implementation phase]`.

capabilities_spec.json declared keys:
```
top-level type: dict
top-level keys: ['dock', 'dock_title', 'capabilities']
  dock: str phoenix
  dock_title: str Phoenix
  capabilities: list 24
```
## 7. Implementation Depth (console-measured)

| Metric | Value |
|---|---|
| TODO/FIXME/XXX markers | 2235 |
| NotImplementedError raises | 58 |
| bare `pass` bodies | 347 |

## 8. Findings (REVIEW)

1. **Architecture docs contradict each other and the tree.** ARCHITECTURE.md claims a
   24x12x4 = 1152-implementation matrix; ARCHITECTURE_FULL.md claims 24 capabilities in
   6 groups; the filesystem has 24 capabilities and 24 domains. Domains 12-24 are
   headings-only in the doc. One canonical matrix must be declared (S14.4: append, don't delete).
2. **S13.5 endpoint status must be confirmed** — see §4. If `POST /phoenix/restore` is absent,
   the Aegis critical-quarantine chain (S7.11 step 3) cannot complete.
3. **capabilities/ and domains/ lack `__init__.py`** (see §2) — they are not importable packages,
   so any dynamic loader must use file-path import, not dotted import.
4. **Stray `*_bak` artifacts** (`main.py.vauros_bak`, `cns/registry.py.deepforge_bak`) indicate
   prior uncommitted recovery attempts. Per S14.4 they are preserved, not deleted.
5. **Transport posture** — see §5. Phoenix delegates via `bus.emit_uro_and_await`, which is
   now TCP-first at the CoordinatorBus layer (Pass 8). Direct `send_to_dock_async` adoption
   inside capabilities/ is the remaining S13.2 line item.

## 9. PLAN — proposed next passes

- **Pass 2 (PLAN):** reconcile the capability/domain matrix into one canonical
  `PHOENIX_MATRIX_CANONICAL.md` (appended per S14.4), mapping all 24 caps x 24 domains
  x 4-fold growth, and marking each cell CORE / GAP / BEST_PRACTICE / WORLD_FIRST status.
- **Pass 3 (ACT):** guarantee `POST /phoenix/restore` exists and is S13.5-shaped
  (dock_name + reason, wipes state volume, rebuilds from known-good image), wired via
  marker-bounded exact-block replacement (S14.5).
- **Pass 4 (ACT):** add `install_tcp_listener(app, dock_name="phoenix")` at startup and
  route capability-level dock calls through `send_to_dock_async` (S9.10, S13.2).
- **Pass 5 (REVIEW):** AST sweep + core synapse suite + Phoenix pytest collect-only,
  then commit only if green (S14.6).
