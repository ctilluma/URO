# REGRESSION MATRIX

## 1. Synapse 10-check suite (tests/synapse_suite.py)
01 canonical imports resolve (no _CompatStub).
02 synapse constructs between two endpoints.
03 NTE state has exactly 24 axes.
04 all axes initialize at baseline 50.0.
05 InteractionOutcome tolerates partial payloads; success mandatory.
06 record_interaction modulates all 24 axes (keys preserved, values move).
07 cross-talk is engine-owned; E/I balance rule observable.
08 decay_synapse moves axes toward 50.0.
09 persistence round-trips synapse identity and levels.
10 CoordinatorBus modulation is non-fatal.

## 2. OPAR conformance (opar/compliance.py)
FULFILLED + full opar_trace on valid stimulus; INCAPABLE without exception
escape on failing act; DEFERRED when grounding blocks; receipt["nte"] has 24
keys; no no-op OPAR stub remains.

## 3. Import hygiene
Direct canonical imports work; no _CompatStub reliance; no duplicate
source-of-truth modules active.

## 4. Bit widths
UUID 128; URID 256; URO 512; INAHASH 1024; NTE state 1536 bits.

## 5. Non-fatal mandate
Modulation, persistence, and grounding-gate failures never break message flow.

## 6. Final gate
_BUILD/tools/no_stub_audit.py --gate exits 0; SCAFFOLD_LEDGER has no [OPEN].
