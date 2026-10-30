# URO BUILD - SESSION BOOTSTRAP

You are resuming the V.A.U.R.O.S. URO library build-out to RFC-DRAFT v3.0.0.
The repository is the durable source of truth. The chat session is disposable.
All decisions, phase state, scaffolds, and continuity data live in `_BUILD/`.

## Goal
Fully implement every code-driven RFC section as a production-grade library.
Final state: zero stubs, zero scaffolding, fully commented code, file headers,
block START/END markers, function-level PURPOSE comments, immediate
implementability, one canonical source of truth per module.

## Non-negotiable principles
1. RFC 1.4 Module Map is the authority.
2. Canonical imports only; no local re-implementation of clamp/cross-talk/decay.
3. RFC 160 Editing Mandate: existing files modified ONLY via Exact Block
   Replacement bounded by START/END markers, occurrence count == 1 verified.
   Net-new files are created whole.
4. Scaffolding is temporary: tagged SCAFFOLD(Phase-N), tracked in
   _BUILD/SCAFFOLD_LEDGER.md, which MUST be empty before sign-off.
5. Definition of Done = measured conformance (RFC 16/17), never asserted.

## Locked decisions (full ADRs in DECISIONS.md)
- ADR-001: Part 16 (Global Infrastructure) EXCLUDED from library scope.
- ADR-002: Restructure via Option A (canonical tree alongside, migrate, delete
  duplicates only after canonical replacement lands and passes).
- ADR-003: Regression matrix / synapse suite / rollout script did not exist;
  they are built from scratch as Phase-0 deliverables.
- ADR-004: Repository-hosted _BUILD/ + bootstrap_session.py is the official
  chat-cloning mechanism.

## Canonical target
See _BUILD/TARGET_TREE.md (summary: core/, nte/, synapse/, opar/,
coordinator_bus.py, quad/, security/, memory/, pathing/, interchange/,
learning/, hardware/, boot/, economy/, docks/, ecosystem/, invariants.py).

## Critical path
Primitives -> Core -> Security primitives -> NTE axes/state -> Synapse
vector/engine -> Synapse persistence -> OPAR package -> CoordinatorBus.

## Resume rule
Before planning or coding, read: SESSION_BOOTSTRAP.md, DECISIONS.md, STATE.md,
MASTER_PLAN.md, TARGET_TREE.md, SCAFFOLD_LEDGER.md, and the current phase
checkpoint in CHECKPOINTS/. Then continue without re-litigating locked
decisions. Or run _BUILD/tools/bootstrap_session.py and paste its bundle.
