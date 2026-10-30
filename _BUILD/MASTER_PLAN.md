# MASTER PLAN

## Phase 0 - Continuity, Audit, Validation Foundation
1. _BUILD/ continuity structure. 2. bootstrap_session.py. 3. classify_modules.py.
4. CONFORMANCE_MATRIX.md. 5. tests/synapse_suite.py. 6. ops/rollout_profile.sh.
7. SCAFFOLD_LEDGER.md. 8. Commit + tag uro-build/phase-00-done.

## Phase 1 - Primitives: constants.py, exceptions.py, types.py
## Phase 2 - Core: core/urid.py, core/uro.py, core/header.py, core/components.py,
   core/inheritance.py, core/datetime_uro.py
## Phase 3 - Security primitives: security/inahash.py, security/encryption.py
## Phase 4 - NTE axes/state: nte/axes.py, nte/state.py
## Phase 5 - NTE math: nte/cross_talk.py, polarity.py, math_influence.py,
   firing.py, reward.py, ans.py
## Phase 6 - Synapse vector/engine: synapse/vector.py, synapse/engine.py
## Phase 7 - Synapse persistence: synapse/persistence.py
## Phase 8 - OPAR package: opar/base.py, protocol.py, stages.py, grounding.py,
   compliance.py
## Phase 9 - CoordinatorBus: coordinator_bus.py (consolidate 4 copies)
## Phase 10 - Quad + CROATE: quad/*
## Phase 11 - Security full: pki, identity, acl, policy, circle_security,
   field_encryption, custody, ldap
## Phase 12 - Memory: hierarchy, movement, consolidation, sleep
## Phase 13 - Pathing: pathing, associations, cro_matrix, trust_value, beacons,
   resolution, onion, path_ops, connectors, swarms
## Phase 14 - Interchange: upi, aupi, interchange, self_loading, priority
## Phase 15 - Learning/AIAI: primitives, pattern, action_uros, attention,
   companion, robotics, sensory, wetware
## Phase 16 - Boot + ANS lifecycle: boot_sequence, child_boot, self_check
## Phase 17 - Economy: currency, token_transfer, marketplace, social_pricing,
   supply_chain
## Phase 18 - Docks + interceptor: dock, manifest, registry, interceptor, dock_defs
## Phase 19 - Ecosystem: api/URO_API.py, connectors/db.py, api_creator.py
## Phase 20 - Invariants + final gate: invariants.py, glossary.py,
   no_stub_audit.py --gate clean, SCAFFOLD_LEDGER empty

## Critical path
1 -> 2 -> 3 -> 4 -> 6 -> 7 -> 8 -> 9. Everything else hangs off this spine.
