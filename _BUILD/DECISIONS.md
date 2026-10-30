# DECISIONS / ADR LOG
Append-only. Never delete history.

## ADR-001 - Exclude Part 16
Date: 2026-10-29
Status: Accepted
Part 16 (Global Infrastructure: MagLev, water biovirons, physical logistics)
is excluded from the library build-out. Part 17 remains in scope but minimal
(only code-relevant slivers: 8-hour mandate tracking, token payout schedules,
audit/governance), deferred to the end.

## ADR-002 - Restructure using Option A
Date: 2026-10-29
Status: Accepted
Build the canonical architecture (TARGET_TREE.md) alongside the existing tree.
Migrate imports and callers. Validate. Delete duplicates only after their
canonical replacement lands and passes. End state must match TARGET_TREE.md.

## ADR-003 - Build validation and regression from scratch
Date: 2026-10-29
Status: Accepted
tests/synapse_suite.py, ops/rollout_profile.sh, and the regression matrix did
not exist. They are created as first-class Phase-0 deliverables. The suite is
expected to FAIL until Phases 4-9 land; that failure is the honest baseline.

## ADR-004 - Repository-hosted chat continuity
Date: 2026-10-29
Status: Accepted
Chat continuity lives in the repository, not in chat memory. Official
mechanism: _BUILD/ project memory plus _BUILD/tools/bootstrap_session.py,
which emits a single paste-able full-awareness bundle for any new session.

## ADR-005 - Phase-0 patch: project-root resolution and suite hardening
Date: 2026-10-29
Status: Accepted
Git toplevel is the multi-project repo (viridant-auraforge), one level above
the URO project directory. All _BUILD tools now resolve the project root via
_BUILD ancestry (script location), with git toplevel only as fallback. The
synapse suite runner stringifies exceptions so a single failure can never
crash the gate. Declared third-party deps (pydantic et al.) are environment
prerequisites, not code defects; install them before baseline runs.

## ADR-006 - Engine-owned cross-talk consolidation
Date: 2026-10-29
Status: Accepted
The 24x24 second pass now lives entirely in uro.synapse.engine per RFC 38 and 28.2. The prior delegation to uro.nte.cross_talk URO objects was removed from the modulation path to eliminate a dual source of truth. Public apply_cross_talk exposes the pass with string-key tolerance.

## ADR-007 - Deterministic synapse endpoint identity at creation
Date: 2026-10-29
Status: Accepted
get_or_create_synapse now pre-coerces string endpoints via the probed URID factory and force-writes the raw endpoint-pair index entry after save. This guarantees the pair index key is stable across create and lookup regardless of pydantic validator coercion behavior, fixing RFC 41.3 URID identity round-trip.

## ADR-008 - Types package replaced with types.py
Date: 2026-10-29
Status: Accepted
The uro/types/ directory (which contained only a _CompatStub __init__.py) was removed and replaced with uro/types.py containing shared type aliases and Protocols per RFC 1.4. No blast radius existed for the old directory.

## ADR-009 - Direct submodule imports until package init consolidation
Date: 2026-10-29
Status: Accepted
uro/core/__init__.py exposes a permissive __getattr__ returning _CompatStub, which intercepts attribute-form imports (from uro.core import header) before submodule resolution. The core init __getattr__ now attempts importlib submodule resolution first and falls back to the legacy stub only for genuinely absent names. Remaining package inits follow in the import-hygiene consolidation pass; suites use full-path from-imports meanwhile.

## ADR-010 - Phase 3 crypto canonicalizations
Date: 2026-10-29
Status: Accepted
1) SHA3-1024 is realized as SHAKE-256 (FIPS 202 SHA3 family) with 1024-bit output; Blake3-1024 uses native BLAKE3 XOF (blake3 1.0.11 installed). 2) AES-256 half-key derivation: each 512-bit K half is compressed to a 256-bit AES key via SHA-512 truncation to 32 bytes, replacing naive truncation that discarded 256 bits of entropy per half. 3) compute_inahash compat export now aliases canonical uro.security.hashing.inahash instead of importing uro.vauros_crypto, eliminating a dual source of truth.

## ADR-011 - Single canonical 24-axis NTEAxis enum
Date: 2026-10-29
Status: Accepted
Owner directive supersedes the DD-1 Option B composite reading: the canonical axis taxonomy is the single 24-member NTEAxis enum in uro/nte/axes.py (12 biological + 12 cognitive members), with AXES_24 derived from it. CognitiveAxis remains solely as a deprecated compatibility alias whose values are a subset of NTEAxis. NTEState24 is therefore NTEStateURO.levels with 24 keys, not a join of two 12-axis states. All consumers import axis definitions from uro.nte.axes (DD-1 centralization retained). Legacy 12-axis modules (neurotransmitters.NTEState, nte_state.py, local NTE_AXES tuples) are brought to 24 or aliased to canonical during Phase 4.

## ADR-012 - Legacy NTE fork consolidation to 24 axes
Date: 2026-10-29
Status: Accepted
Per owner directive (ADR-011), all NTE state modules converge on the single 24-axis NTEAxis taxonomy. uro.nte.neurotransmitters: the 10-member NTE enum fork is replaced by an alias to NTEAxis; NTEState is rebased to 24 canonical axes on its legacy [0,1] scale with to_canonical/from_canonical bridges to the canonical [0,100] scale; Receptor/Synapse firing model (RFC 29/30) retained unchanged. uro.nte.nte_state: rewritten as a canonical alias to NTEStateURO when no importers exist (scan-verified); otherwise reported for manual migration. 12-axis docstrings in uro/nte/state.py and the uro/__init__ NTE comment corrected to 24. The 12-axis migration docstring in uro/synapse/persistence.py is retained intentionally (forward disk migration).

## ADR-013 - nte_state.py brought up to 24 axes with API-compatible rewrite
Date: 2026-10-29
Status: Accepted
The scan-verified alias of uro/nte/nte_state.py was skipped because naive substring matching reported 22 references (most are syn.nte_state attribute uses, not module imports). Rather than alias or leave the 12-axis fork, the module is rewritten in place as an API-compatible 24-axis view on the legacy [0,1] scale: kwargs constructor, attribute access via __getattr__/__setattr__, as_dict() returning all 24 canonical axes, to_canonical() bridge, and legacy extras (endorphins, histamine) quarantined outside the canonical state. Real module importers keep working unchanged.


## ADR-014 - Phase 5 NTE math modules created; cross_talk URO remains policy-only
Date: 2026-10-29
Status: Accepted
Net-new modules uro/nte/polarity.py (RFC 25), math_influence.py (RFC 27), firing.py (RFC 29/30), reward.py (RFC 31/32), ans.py (RFC 34) implement the NTE math layer. uro/nte/cross_talk.py is retained as a sealed, versioned policy artifact for governance and inspection only; per ADR-006 the synapse engine remains the sole executor of the 28.2 second pass, and nte_math_suite check 03 asserts the engine source contains no uro.nte.cross_talk import.

## ADR-015 - Phase 6 synapse vector conformance
Date: 2026-10-29
Status: Accepted
SynapseVectorURO already carried all twelve RFC 36.1 fields and five of six 36.2 methods. Two gaps closed by count-verified replacement: (1) genesis_trust_level now delegates to the canonical GenesisTrustEnforcer (child=100/new=0 via parent_inahash lineage) instead of a hard-coded 0.0, with an is_child lineage probe added; (2) record_interaction wraps modulation in try/except per the RFC 35.6 non-fatal mandate. uro/synapse/__init__ __getattr__ now resolves real submodules before serving compat stubs (ADR-009 pattern).

## ADR-016 - Dock-convention validator no longer invents values for absent optional fields
Date: 2026-10-29
Status: Accepted
The SynapseVectorURO _accept_dock_convention before-validator filled every missing str field with the sentinel default and every missing float with 0.5, overriding field defaults (parent_inahash became truthy, breaking the genesis child/new rule; last_used and created_at became 0.5). The str and float branches now substitute sentinels only when the field is required; absent optional fields keep their declared defaults and explicit nulls stay None. Provided-value normalization for dock compatibility is unchanged.

## ADR-017 - Memory engine extended in place for RFC 64-69
Date: 2026-10-29
Status: Accepted
uro/memory/engine.py is extended via count-verified Exact Block Replacements rather than rewrite: retrieve now performs the RFC 65.1 SHORT-to-WORKING promotion; MemoryItem gains saved_long to model RFC 66 dual residence; connection_pass/apply_pass implement the four per-pass outcomes from use counter, ACL, potentiators, and last access; introspect implements the 65.2 clear cascade; consolidate accepts an epinephrine parameter for the 67.1 stress trigger; sleep_mode and the morning-question queue implement 68; downtime_reflection implements 69; cache_time implements 67.3. The tier enum keeps SF/F/M/S with ARCHIVE as the HD subdivision of long-term storage.

## ADR-018 - Phase 8 pathing conformance and RFC 72/73/74/77/79/80/81 modules
Date: 2026-10-29
Status: Accepted
trust.py evaluate_responses realigned to the RFC 73 ladder (100 consensus with trust point, 90 TV check with higher-TV responder, 75-89 deep check with minority hypothesis exploration, below 75 reanalyze). connectors.from_urid_pair gains self_urid to disambiguate the RFC 80 SELF rows (LINK vs CHILD). beacons.py gains the RFC 74 parent/child/interface sequences as module constants. Net-new uro/pathing/cro_matrix.py (RFC 72), path_ops.py (RFC 70.3/76.4/79), stack_processing.py (RFC 77), swarms.py (RFC 81). uro/relations/__init__ getattr now submodule-first (ADR-009). relations/ remains the implementation home for Association/PathURO pending a later consolidation pass into pathing/ per the target tree.

## ADR-019 - Phase 9 interchange modules and header single-sourcing
Date: 2026-10-29
Status: Accepted
uro/interchange.py header builders now delegate to uro.core.header (RFC 7 single source) instead of a parallel struct+blake2b implementation. AUPI gains RFC 88 container resolution with a localized wrapper-path cache. Net-new root modules uro/hot_swap.py (RFC 85 identity-preserving swap), uro/self_loading.py (RFC 86), uro/priority.py (RFC 87) live at package root pending the deferred interchange/ package consolidation; creating that package now would shadow uro/interchange.py for existing importers.

## ADR-020 - Top-level uro package getattr is submodule-first
Date: 2026-10-29
Status: Accepted
Completes the ADR-009 rollout: uro/__init__.py __getattr__ now attempts importlib submodule resolution before serving _CompatStub, so attribute-form imports (from uro import interchange) bind real modules. Genuinely absent names still receive the legacy stub for dock compatibility. All three package levels (top, core, synapse) are now submodule-first; remaining per-package inits follow in the import-hygiene consolidation pass.

## ADR-021 - Open/proprietary boundary for learning and cognition
Date: 2026-10-29
Status: Accepted
Owner directive: generic learning mechanics live in the open URO library; revenue-bearing cognitive internals remain in the cognitive dock. uro/learning/ (new, open) owns RFC 90-93/98/100 primitives: cause-effect ledger, experimentation gate, feedback loops, observation, sequencing, gap-segmented pattern analysis, differentiate/correlate, dicho registry, action URO costing, attention/daydream overrides, aloneness propagator, VTA-CAS loop. uro/cognition/ (open) retains the fuzzy matrix, verdict dynamics, myelination, and CognitiveCore as the reference learner. docks/cognitive/ (proprietary) retains the 48 capabilities, CNS hypernodes, domain graphs, AGI engines, and LLM orchestration; those capabilities SHOULD delegate to uro.learning primitives in a future consolidation pass rather than re-implement them. uro/cognition/__init__ getattr made submodule-first (ADR-009).

## ADR-022 - Canonical OPAR package and grounding resolution order
Date: 2026-10-29
Status: Accepted
uro/opar.py (auto-generated CRUD OPAREngine, zero importers verified by grep) is retired to uro/opar_operations_legacy.py via git mv; the canonical uro/opar/ package (stages, protocol, base, grounding, compliance) now owns the RFC 10-17 OPAR-24 contract per the Module Map. Legacy operations names are re-exported from the package root for compatibility. uro/phases/opar.py and uro/base.OPARPhase remain as legacy cycle implementations until a consolidation pass. Grounding resolution order: dock capabilities.cap_37_grounded_emission first (proprietary per ADR-021), open LocalGroundingEngine heuristic fallback. nte24 imports AXES_24 from uro.nte.axes (ADR-011); no local axis tuples exist in the canonical package.

## ADR-023 - Quad-Capability and CROATE modules (RFC 45-48)
Date: 2026-10-29
Status: Accepted
uro/quad/ owns the four-dimension evaluation (quad_capability.py), character-vs-condition equilibrium math (character_condition.py), and the six-trait CROATE model with canonical NTE axis mappings (croate.py). Conventions: SD_UNIT = 10 trait points; trait scores are means of mapped axis levels; character drift is bounded by the condition value and monotonic per sustained period; innovation affinity derives from creativity and analogical_transfer per RFC 45.4. Psychological parallels (RFC 48) map to genesis trust and cold-boot baseline shock already implemented in uro/genesis_trust.py and NTEStateURO baselines; no separate module required.

## ADR-024 - Phase 13 security full stack scope
Date: 2026-10-29
Status: Accepted
Net-new uro/security modules: ldap.py (RFC 58 schema + six-step uPass chain), circle_security.py (RFC 57 five rings), field_encryption.py (RFC 60 dual-header wraps and dynamic grants), user_keys.py (RFC 53.1 wraps), custody.py (RFC 63 send chain and 2-way exchange over keyed INAHASH MACs; PKI signature binding deferred to a signature-consolidation pass because pki.sign_uro semantics were not dumped). Patches: policy.py group-override evaluation (RFC 55.1), acl.py override_check OR semantics (RFC 59.1), pki.py ROOT_CA_REGIONS (RFC 51.2), identity.py bind_time_uro (RFC 54.4). Section 52 signatures remain in pki.py; no separate signature.py module.

## ADR-025 - Boot package and lifecycle semantics (RFC 107-109)
Date: 2026-10-29
Status: Accepted
uro/boot/ owns the 16-step boot sequence as an ordered, handler-driven runner (docks supply real handlers; absent handlers are permissive noops so the sequence is testable in isolation), child boot with ACK-gated response queues and seal verification, and the generic four-step self-check with quarantine flag. The runner halts on the first False handler and reports the completed prefix, matching RFC 107 failure semantics. A uro/boot.py shadow, if present, is retired to boot_legacy.py per the opar/quad precedent.

## ADR-026 - Economy layer: currency precision, tax, ledger consolidation
Date: 2026-10-29
Status: Accepted
Net-new uro/economy modules: currency.py (InSPativo 2dp / InSPaneda 4dp, 1:1000 ratio with ROUND_HALF_UP), token_transfer.py (atomic transfers with 10% network tax burned to network account), social_pricing.py (trust/reputation discounts), supply_chain.py (cost roll-up through production stages). Existing ledger.py retained as canonical (imported by GLOBAL_LEDGER and Marketplace); the other three ledger.py files (pipeline, licm, root) are domain-specific or legacy and will be audited in a consolidation pass. price_good and marketplace.purchase already wire through the canonical ledger, preserving money conservation.
