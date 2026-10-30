# URO Library - Capabilities Primer (Prompt Onboarding)

PURPOSE: Prepend this document to any LLM session that must write, review, or
extend code against the URO library. It teaches what the library CAN DO, the
canonical vocabulary, and the hard rules every generated artifact must obey.
Status: aligned to uro-build/phase-16-done (16 suites, 160 checks green).

## 1. Core Thesis
- Everything is a URO: a URO is a RELATIONSHIP (URID1, URID2), not a thing.
  The relationship between source and identifier is the carrier of value.
- Fractal Mandate: every URO carries identity (URID pair), integrity (INAHASH
  seal), custody lineage, and NTE state.
- Relationships are first-class: a Synapse Vector URO holds the emotional and
  trust state between exactly two UROs.
- Trust is earned: genesis rule - children of trusted parents start at 100%,
  new objects start at 0%.

## 2. Identity Geometry (RFC 1.2)
- UUID 128b; URID 256b = UUID1 || UUID2; URO 512b Link = URID1 XOR URID2
  plus SHA128 cross-terms.
- INAHASH 1024b = Blake3-1024( SHA3-family-1024( MSG ) ). Header = four
  64-bit length fields plus Blake2-256 checksum.
- Epoch: 14-MAY-1973 00:12:24 UTC. Currency: 1 InSPativo = 1000 InSPaneda;
  network tax 10%; InSPativo 2dp, InSPaneda 4dp.

## 3. The 24-Axis NTE System (RFC 21-34)
- One canonical NTEAxis enum: 12 biological + 12 cognitive axes; baseline 50.0;
  clamp [0, 100]; homeostatic decay toward baseline.
- Cross-talk is engine-owned (uro.synapse.engine.apply_cross_talk): the 24x24
  second pass is NEVER re-implemented elsewhere.
- Available: polarity descriptors, weighting curves (x*log10(x+10) dominating),
  firing decisions, receptor min/max bounds, D1/D2 reward-punishment, habit
  formation, bi-directional R/P fault tracing, ANS branch classification,
  VTA-CAS context-reward prediction.

## 4. Synapses (RFC 35-44)
- SynapseVectorURO carries all twelve RFC 36.1 fields: endpoints, synapse_urid,
  nte_state, topic_trusts, overall_trust, use/success counters, last_used,
  inahash, created_at, last_updated.
- record_interaction books usage AND modulates all 24 axes; modulation is
  wrapped non-fatal (failures never break message flow).
- Durable persistence with deterministic pair-index identity round-trips.
- genesis_trust_level delegates to the canonical GenesisTrustEnforcer.

## 5. OPAR-24 Capabilities (RFC 10-17)
- Every capability implements observe/plan/act/review. Each stage runs in
  isolation; failures produce INCAPABLE stages, never raised exceptions.
- Receipt honesty contract: FULFILLED / DEFERRED (grounding gate blocked) /
  INCAPABLE, with full opar_trace, 24-key NTE, grounding details, provenance.
- Grounding gate verifies claims (verified/refuted/unverifiable) and routes
  passed / emit_with_flags / blocked.
- Compliance harness: RFC 16 checklist + RFC 17 five-point conformance test.

## 6. Memory and Learning (RFC 64-69, 89-100)
- Tiers: SF registers (working), F RAM (short), M SSD / S HD (long/archive).
  Retrieval promotes long->short->working; introspection clears back down.
- Connection pass: four outcomes (save-long+keep-short, save-long+drop-short,
  keep-short-only, drop-short) from use counter + ACL + potentiators + recency.
- Sleep mode (reduced ACL, pruning, consolidation, melatonin rise), morning
  question queue, downtime reflection, epinephrine-triggered consolidation.
- Open learning primitives: cause-effect ledgers, busy-gated experimentation,
  feedback loops, observation records, sequencing/prediction, gap-segmented
  pattern analysis, differentiate/correlate, dicho (idiom) registries, action
  URO costing (chain/sequence/serial/parallel), attention/daydream overrides,
  aloneness propagator, VTA-CAS loop.

## 7. Pathing and Routing (RFC 70-82)
- Paths are UROs. Priority 0 = fastest; sum of all paths = priority;
  path hash = SHA512(src, dest).
- Connector matrix: OUTPUT / INPUT / LINK / CHILD / PATH with self-awareness.
- Onion routing (each hop knows only itself and next), CRO resolution matrix,
  TV consensus ladder (100/90/75/reanalyze), beacon sequences (parent/child/
  interface), stack processing, swarm routing tuples, path combine rule:
  (U1,U2) + (U3,U1) -> (U3,U2).

## 8. Security (RFC 49-63)
- INAHASH sealing for every URO; nested AES-256 with 1024-bit keys split into
  512b halves and full-entropy SHA-512 derivation per half.
- uPass six-step alternating BLAKE3/SHA512 chain; LDAP eight-field schema.
- Concentric circle rings (Store/Owner/Admin/Access/End-User); field-level
  encryption with dual headers and dynamic grants; user keyring wraps;
  custody chains and two-way exchanges; ACL AND/OR/NAND/NOR combinators;
  policy override groups; six air-gapped PKI root regions.

## 9. Economy (RFC 110-114)
- InSPativo (2dp) / InSPaneda (4dp), 1:1000, ROUND_HALF_UP.
- The ledger is the ONLY money mover (conservation invariant); 10% network tax
  is burned to the network account on every transfer.
- Marketplace: goods are UROs (synapse templates, trust bundles, emotional
  history, audit trails, capability gaps) with purchase/reuse and royalties.
- Social pricing (trust/reputation discounts) and supply-chain cost roll-ups.

## 10. Boot and Lifecycle (RFC 107-109)
- Sixteen-step boot; halts on first failure preserving the completed prefix.
- Child boot with ACK-gated response queues and seal verification.
- Four-step self-check (INAHASH, URID integrity, NTE bounds, custody head)
  with quarantine semantics.

## 11. Canonical Import Map
| Need | Import |
|---|---|
| Identity | from uro.core.urid import URID |
| Relationship object | from uro.core.uro import URO |
| Header build/verify | from uro.core.header import build_header, parse_header |
| NTE axes/state | from uro.nte.axes import NTEAxis, AXES_24 ; from uro.nte.state import NTEStateURO |
| Synapse | from uro.synapse.vector import SynapseVectorURO ; from uro.synapse.engine import modulate_synapse |
| Persistence | from uro.synapse.persistence import get_or_create_synapse |
| Sealing/hashing | from uro.security.hashing import inahash |
| Encryption | from uro.security.encryption import double_encrypt, double_decrypt |
| OPAR base | from uro.opar import OPARBase, StageResult, nte24 |
| Memory | from uro.memory import MemoryEngine, MemoryItem, MemoryTier |
| Pathing | from uro.pathing.path_ops import combine_paths, path_hash |
| Translation | from uro.aupi import AUPI, typed_uro |
| Learning | from uro.learning import CauseEffectLedger, CASLoop, DichoRegistry |
| Economy | from uro.economy.marketplace import Marketplace ; from uro.economy.token_transfer import transfer_tokens |
| Genesis trust | from uro.genesis_trust import GenesisTrustEnforcer |

## 12. Hard Rules for Generated Code
1. Canonical imports only. Never re-derive axis tables, cross-talk rules,
   hash compositions, or epoch constants - import them.
2. No stubs. Functions have behavior or raise typed exceptions from
   uro.exceptions. No silent pass-throughs, no _CompatStub returns.
3. Non-fatal mandate: modulation and persistence failures must never break
   message flow (wrap, log, continue).
4. Receipts are honest: never report FULFILLED after an internal failure.
5. Seal every state URO (INAHASH) before it crosses a trust boundary.
6. Money moves only through the ledger; never mint or burn outside it.
7. 24-axis invariance: axes are defined ONLY in uro.nte.axes.
8. Patches are count-verified exact block replacements; never full-file
   rewrites of live modules.
9. Attribute-form package imports are avoided in new code; use full-path
   from-imports (from uro.core.header import ...) until the stub-getattr
   hygiene pass completes.

## 13. Worked Recipes
Create and seal a URO:
    from uro.core.uro import URO
    obj = URO.new(payload={"kind": "note", "text": "hello"})
Compute a 512-bit link:
    obj.link()  # 64 bytes
Establish a synapse and record an interaction:
    from uro.synapse.persistence import get_or_create_synapse
    from uro.synapse.engine import InteractionOutcome
    syn = get_or_create_synapse("a" * 64, "b" * 64)
    syn.record_interaction(InteractionOutcome(success=True, novelty=0.7))
Run a capability through OPAR:
    from uro.opar import OPARBase, StageResult
    class MyCap(OPARBase):
        capability_id = "my.cap"
        async def observe(self, stimulus, nte):
            return StageResult(stage="observe", data={"seen": stimulus})
        async def plan(self, observation, nte):
            return StageResult(stage="plan", data={"plan": "echo"})
        async def act(self, plan, nte):
            return StageResult(stage="act", data={"artifact": {"claims": [{"grounded": True}]}})
        async def review(self, observation, plan, action, nte):
            return StageResult(stage="review", data={"ok": True})
    import asyncio
    receipt = asyncio.run(MyCap().execute({"input": 1}))
Transfer value with tax:
    from uro.economy.token_transfer import transfer_tokens
    result = transfer_tokens("alice", "bob", 10.0)  # 10% to network
Ground a claim in a receipt:
    receipt["_gate"] in ("passed", "emit_with_flags", "blocked", "skipped")
Self-check any sealed URO-like object:
    from uro.boot import self_check
    report = self_check(syn)  # quarantined flag when any check fails

## 14. Verification
The single-entry gate proves the library state at any time:
    python3 tests/run_all_suites.py
Expected output: 16 PASS lines and "16/16 suites green", exit code 0.
Regenerate the API reference after any API change:
    python3 _BUILD/tools/generate_api_reference.py
