# Phase 00 - Continuity and Audit

## Objective
Durable session memory + audit + validation gates before any library code.

## Deliverables
_BUILD/ docs, tools/bootstrap_session.py, tools/classify_modules.py,
tools/no_stub_audit.py, tests/synapse_suite.py, ops/rollout_profile.sh.

## Exit criteria
1. CONFORMANCE_MATRIX.md populated (every file classified REAL/STUB/EMPTY/PARSE_ERROR).
2. Duplicate-basename list reviewed; consolidation order agreed.
3. Baseline synapse_suite run recorded (failures become Phase 4-9 work items).
4. git commit + tag uro-build/phase-00-done.

## Outcome
Closed at commit 40f21c240 with synapse suite 10/10 (baseline-phase00-final.txt).
Tag uro-build/phase-00-done force-moved to closure commit.
Cross-talk consolidated engine-owned (ADR-006); synapse endpoint identity deterministic (ADR-007).