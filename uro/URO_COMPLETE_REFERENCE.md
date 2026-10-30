# URO COMPLETE REFERENCE
## V.A.U.R.O.S. Total System Awareness Document

**Version:** 3.0.0 (24^24 Model, TCP-First Transport, Advanced Aegis & Refinery)
**Location:** ~/viridant-auraforge/uro/uro/URO_COMPLETE_REFERENCE.md
**Purpose:** Single source of truth for what a URO is, how it operates, what governs it, and how every dock, file, and subsystem integrates.

### HOW TO USE THIS DOCUMENT
- Every section is numbered. Cross-references appear as [see S.n.m].
- Every dock should read S13 (Dock Integration) plus the sections it references.
- This is a living document. Append new sections; never delete history [see S14.4].

### TABLE OF CONTENTS
- S1 Foundations and Philosophy
- S2 URO Structure and URID Pathing
- S3 OPAR Lifecycle and Order of Operations
- S4 NTE - 24-Axis Neurotransmitter & Cognitive Equivalences
- S5 Quad-Capability and Character/Condition
- S6 Learning, AIAI, Companion, Robotics, Wetware
- S7 Security Architecture & Aegis Immune System
- S8 Memory Architecture & Cognitive Decay
- S9 Pathing, Associations, Beacons, Connectors, AUPI, & TCP-First Transport
- S10 Economy, Time, Autonomic Nervous System
- S11 Interchange, Hot-Swap, Boot, Self-Loading, Priority, & Refinery AST
- S12 Hardware and System Architecture
- S13 Dock Integration Points & Wiring Checklists
- S14 Invariants, Glossary, Cross-Reference Index, Expansion

================================================================
S1 FOUNDATIONS AND PHILOSOPHY
================================================================

S1.1 WHAT IS A URO
A URO (Universal Resource Object) is the fundamental building block of V.A.U.R.O.S.
Everything is an object. Everything has a relation. No matter how far down you drill,
always another object, then its relation. Everything is a URO.

A URO is a living, self-aware entity that:
- Knows itself (URID pair identity)
- Knows its relationships (associations, children, parents, synapses)
- Maintains its own state (24-axis NTE vector) [see S4]
- Evolves (OPAR cycle) [see S3]
- Communicates (beacon signals, TCP-first URO transport) [see S9]
- Secures itself (INAHASH, ACL, Aegis Quarantine) [see S7]
- Remembers (memory hierarchy, cognitive decay) [see S8]
- Grows (children, associations, paths, multi-file AST refactoring) [see S11]

S1.2 CORE PRINCIPLES
1. Universality - everything is a URO; no exceptions.
2. Relationality - no URO exists in isolation. The synapse IS the "R" (Relationship).
3. Self-Awareness - identity via URID pair, 24-axis NTE, capabilities.
4. Evolution - self-improvement via OPAR [see S3].
5. Continuity - system must keep running while growing.
6. Growth Through Friction - challenges outside the box create growth.
   "An object in motion ... Nothing changes without friction."

S1.3 GOVERNANCE SUMMARY
A URO is governed by: OPAR lifecycle [S3], 24-axis NTE state [S4], security/Aegis [S7],
memory hierarchy [S8], pathing/TCP-First rules [S9], economy [S10], and invariants [S14.1].

================================================================
S2 URO STRUCTURE AND URID PATHING
================================================================

S2.1 THE URID PAIR
Every URO is identified by (URID1, URID2).
- URID1 - Source of the URO. Where to go for the URO. Origin / template / truth.
- URID2 - Identifier in URID1. Which child, data, or structure is referenced.

S2.2 SPECIAL CASES
    URID1=URID, URID2=All0   -> Template Request (structure of URID)
    URID1=All1, URID2=URID   -> Group of URID1s
    URID1=URID, URID2=URID   -> Entire URID1 Objective (Self-Defined)
    URID1=0,    URID2=0      -> Broadcast to all
    URID1=URID, URID2=0      -> Template Request
    URID1=0,    URID2=URID   -> Knowledge of Path / empty group / non-parent
    URID1=A,    URID2=B      -> B field of A / B inherits A
    URID1=A,    URID2=A      -> Data of A / new self-defined object

S2.3 HEADER STRUCTURE
    1. 64 bits - Source URO Length
    2. 64 bits - Destination URO Length
    3. 64 bits - Payload URO Length
    4. 64 bits - Future (reserved)
    5. Blake2-256 hash of (S-Len + D-Len + P-Len + Fut)

S2.4 COMPONENTS (10)
URID pair, Header, Payload, 24-axis NTE vector [S4], ACL [S7.9], Personality,
Capabilities, Associations [S9.6], Children, INAHASH [S7.2].

S2.5 INHERITANCE
Any derivative URO inherits the capabilities of its parent, allowing security-based
UROs to evolve as technology and vulnerabilities change. Child gets own URID2,
references parent URID1, inherits security context, evolves independently.

================================================================
S3 OPAR LIFECYCLE AND ORDER OF OPERATIONS
================================================================

S3.1 OPAR DEFINITION
OPAR = Observe, Plan, Act, Review.
- Observe: 1.a Self-Check (internal); 1.b Input/Queue Check (external).
- Plan: Where / How to process observations.
- Act: Process / Output.
- Review: Self Check, Evaluate, Improve (includes Grounded Emission Gate).

S3.2 MULTIPHASIC URO
Four-stage process: 1 Plan, 2 Act, 3 Review, 4 Improve. Continuous improvement loop.

S3.3 ORDER OF OPERATIONS (8)
1 Who am I / What Inputs; 2 Act on inputs; 3 What can we do; 4 We act;
5 What did we learn/gain/receive; 6 We Growth/Analysis;
7 What have I learned/gained; 8 Self Growth Actions.

S3.4 THREADS
8 threads - 1 per cycle when not in series (simplified 4 threads, seasonal).

S3.5 PER-DOCK OPAR MAPPING [see S13]
Coder: observe requirements, plan implementation, act generate, review output.
Cognitive: observe context, plan reasoning, act process, review understanding.
Memory: observe state, plan retrieval, act read/write, review health.
Security (Aegis): observe threats, plan defenses, act enforce/quarantine, review posture.
Refinery: observe quality, plan AST improvements, act refactor (multi-file), review structural metrics.

================================================================
S4 NTE - 24-AXIS NEUROTRANSMITTER & COGNITIVE EQUIVALENCES
================================================================

S4.1 OVERVIEW
The URO maintains levels of both self and URO connection (synapses). The NTE is a
bidirectional, 24-axis neurochemical state that lives in the synapse between two entities.
Every interaction must read and modulate that synapse. Responses carry NTEs; even a
failure can improve a link.

S4.2 THE 24 AXES (12 Biological + 12 Cognitive)

Biological Axes (Governance & Physiology):
1. GLUTAMATE (Excitation): Drive to act/learn. High = active learning. Low = conservative.
2. GABA (Inhibition): Filtering/confidence gating. High = rejects weak signals.
3. DOPAMINE (Reward/Learning): Learning rate on prediction errors.
4. SEROTONIN (Decision/Patience): Decision threshold. High = waits for evidence.
5. ACETYLCHOLINE (Plasticity): Learning rate for novel inputs/uncertainty.
6. NOREPINEPHRINE (Arousal): Cognitive bandwidth, network reset, external focus.
7. EPINEPHRINE (Acute Stress): Urgency signal. High = reject low-trust, route fast-path.
8. CORTISOL (Chronic Stress): Sustained load management. High = reduce exploration.
9. OXYTOCIN (Trust/Bonding): Trust currency between endpoints. High = in-group loyalty.
10. CANNABINOID (Forgetting): Memory pruning and trust decay. High = actively forgets.
11. MELATONIN (Consolidation): Replay, consolidate, garbage-collect. High = maintenance.
12. ADENOSINE (Fatigue): Resource depletion. High = shed load, power-save.

Cognitive Axes (Higher-Order Processing):
13. FOCUS: Attention concentration on specific tasks.
14. CREATIVITY: Generation of novel, non-obvious solutions.
15. ANALYSIS_DEPTH: Granularity of logical decomposition.
16. PATTERN_RECOGNITION: Ability to identify recurring structures.
17. ABSTRACTION_LEVEL: Distance from concrete implementation details.
18. INFERENCE_SPEED: Rate of logical deduction and conclusion drawing.
19. UNCERTAINTY_TOLERANCE: Comfort with incomplete or ambiguous data.
20. COGNITIVE_FLEXIBILITY: Ability to switch between different concepts/rules.
21. METACOGNITION: Awareness and regulation of one's own cognitive processes.
22. ANALOGICAL_TRANSFER: Applying knowledge from one domain to another.
23. DIALECTICAL_BALANCE: Weighing opposing viewpoints to find synthesis.
24. INSIGHT_READINESS: Preparedness for sudden, non-linear problem resolution.

S4.3 BACKWARDS COMPATIBILITY & NORMALIZATION
Legacy systems may provide 8-axis or 12-axis states. The core library provides
normalize_nte_state(partial_state: dict) -> dict. This function accepts any subset,
maps legacy names to canonical 24-axis names, and pads missing axes with the BASELINE
(50.0). Never hand-edit individual levels; always pass through the normalizer.

S4.4 CROSS-TALK RULES (Engine-Owned)
- E/I balance: if glutamate - gaba > 20, inhibit glutamate and raise gaba by 10% of excess.
- Sustained stress erodes bonding: oxytocin -= 0.15 * max(0, cortisol - 50).
- Recovery opposes stress: cortisol -= 0.10 * max(0, melatonin - 50).
- Fatigue inhibits reward: dopamine -= 0.10 * max(0, adenosine - 50).
- Social buffering calms urgency: epinephrine -= 0.10 * max(0, oxytocin - 50) + 0.05 * max(0, gaba - 50).
- Final clamp to [0.0, 100.0]. Never re-implement these; call the engine.

S4.5 HOMEOSTATIC DECAY
engine.decay_synapse(synapse, rate=0.02) moves every axis toward 50.0. Run in
idle/maintenance cycles.

S4.6 REWARD / PUNISHMENT FORMULAS
Reward: Motivation += x(log10(X+10)).
Punishment: Motivation += Dopamine (decrease).
Cost to buy (InSPaneda): (log10(X^3)^2)/3. Max 100 points. Purchase goes to affected
UROs (standard InSPa 10% applies) [see S10.1].

S4.7 BOND DYNAMICS
Bonds decrease naturally with time and increase with use. Bonds increase faster and
decrease slower the longer the connection has existed.

S4.8 ANS LINK [see S10.6]
ANS regulates involuntary operation using NTE (fight/flight, rest/digest, load shedding).

================================================================
S5 QUAD-CAPABILITY AND CHARACTER/CONDITION
================================================================

S5.1 FOUR DIMENSIONS
Base (fundamental function), Gap Remediation (what is missing), Best Practice
(proven standards), World-First Innovation (never done before).

S5.2 APPLICATION
Every capability in every dock is evaluated across all four dimensions.

S5.3 CHARACTER vs CONDITION
Character = combination of traits defining responses (the self).
Condition = immediate state; standard deviations from character.
Sustained large deviations slowly shift character toward the deviation until a new
equilibrium. "Character is self, condition is where self meets ambiente."

================================================================
S6 LEARNING, AIAI, COMPANION, ROBOTICS, WETWARE
================================================================

S6.1 LEARNING PHILOSOPHY
"ALL THINGS ARE TAUGHT." Adaptability, capacity to process new information, speed,
ease of processing. Growth through friction [S1.2].

S6.2 LEARNING PRIMITIVES
Cause and Effect; Experimentation (try action URO on another URO, map result, when not
busy); Feedback loops; Observation (what am I seeing); Sequencing (X followed by Y);
Pattern Analysis (increasing complexity, gaps segment data, correlate gaps);
Differentiate (break URO into components = make smaller); Correlate (group UROs into
larger system = make bigger).

S6.3 ACTION UROs
Chain, Sequence, Serial, Parallel.

S6.4 ATTENTION AND DAYDREAM
Prioritize or deprioritize input streams to provide overrides on input stream.

S6.5 COMPANION AIAI
Grows with the individual (infant -> android). Learns over time, not all at once.
A single data point doesn't carry the same weight as accumulated learning.

S6.6 ROBOTICS AND WETWARE
Robotics: AIAI in robotic systems for advanced android capabilities.
Wetware: integrate hardware into the brain; replicate neurotransmitters for consistent
operation between hardware and biology [see S4].

S6.7 ALONENESS
Aloneness -> propagator for action. Object with little input searches out capabilities
(altruism or self-improvement).

================================================================
S7 SECURITY ARCHITECTURE & AEGIS IMMUNE SYSTEM
================================================================

S7.1 PILLARS
Confidentiality, Integrity, Trust, Availability (Access, Authorization, Redundancy).

S7.2 INAHASH
INAHASH = Blake3-1024( SHA3-1024( MSG )). Dual-standard to prevent single-body compromise.

S7.3 1024b KEY SPLIT
1024b Key = 512b K1 + 512b K2. MSG = AES256( K2, AES256( K1, MSG )).

S7.4 CIRCLESECURITY
Store: SHA512(512b key). Owner: 512b key encrypted with owner AES256(OwnerPriv).
Admin: REQ=1 -> 512b key encrypted AES256(AdminPriv); REQ>1 -> Matrix 512b key encrypted
AES256 ^ AES256; Validate: decrypt two AES, first 512b SHA512 against last 4B of hash.

S7.5 PKI
InSPa is Certificate Authority (tiered). Each public key gets URO (PKI.PUBK):
Key, Issue(Time URO), Expiration(Time URO), Revocation(Time URO), Signed Certificate.

S7.6 SIGNATURES
URO Signature (PKI Sign): URO of object, URO of signer, URO of trusted owner,
URO(SHA512(Content)). Trusted Signature: Sign(URO Trusted / URO Self /
URO[Trust Owner] / SHA512[URO Trusted Digest]). Trusted Owner URO: PKI.PUB, group/URO
signatures, search who trusts owner, closeness of trusted signer.

S7.7 USER ENCRYPTION AND IDENTITY
User Encryption: SHA512 X3 (Password) XOR EncryptKey; Recovery PKI E(InSPa, Key).
User PKI URO: Private Key AES256(Key, Private).
Identity verified by proof of access to a URO (password hashed to core key matching URO
held key, or PKI PRIV signing). Tokens: indefinite / until revoked / time-limited.
Core key full verification: request NFS signed time URO, sign response with PKI, assign
response+Time URO to DateURO.

S7.8 CUSTODY AND 2-WAY EXCHANGE
Custody: Send -> ((Trusted Signature for URO with Hash)+x(n)) -> URO of Trust Received,
Hash of Trust URO Received. 2-Way Exchange: sender signs RCV URO, receiver signs SND URO,
signed hash shows trusted. Verify/Chain: append URO(PUB), sign, append signature.

S7.9 ACL AND POLICY
ACLs for UROs and child UROs (self, child, external). Policy URO contains ACLs/policies;
each grant/deny uses binary math (AND, OR, NAND, NOR); group policies can override
other groups. Groups act as ACLs for matching traffic [S9.6].

S7.10 INTEGRITY AND AVAILABILITY
Integrity: hashes ensure URO at rest/in transit verifiable. Availability: multiple
pathing avenues for fault tolerance [S9].

S7.11 AEGIS IMMUNE SYSTEM (Critical Quarantine)
When a dock exhibits anomalous behavior (e.g., sustained epinephrine > 0.85, trust < 0.4):

1. NTE Repulsion: Aegis broadcasts a synapse update forcing oxytocin -> 0 and
   epinephrine -> 100 for all connections to the rogue dock.

2. Physical Isolation: Aegis calls POST /aegis/quarantine on the Coordinator/Host
   Controller with severity="critical". The Host Controller executes docker stop
   <dock>_prod to sever network access.

3. Phoenix Restoration: The Host Controller dispatches a URO to the Phoenix dock
   (POST /phoenix/restore), which wipes the compromised state volume and rebuilds
   the dock from a known-good image.

================================================================
S8 MEMORY ARCHITECTURE & COGNITIVE DECAY
================================================================

S8.1 TIERS
SF REGISTER (fastest, immediate), F RAM (short-term), M SSD (long-term), S HD (archive).

S8.2 TRANSITIONS
Working=registers (recursively calculated ACL+Personality -> immediate); short=ram;
long=storage; retrieved long->short or short->working when active;
clear work->short, short->long >= self introspection.

S8.3 USE COUNTER DECISION
When a connection is used in short time memory its use counter increases; counter
(combined with ACL and Potentiators) and last access decide: saved to long+kept short,
saved long+removed short, kept only short, or removed short.

S8.4 CONSOLIDATION / ATTACHMENT / CACHE
Consolidation reduces storage/pathing/associations to accelerate processing.
Memories work with attachment (more attachment, more chance).
Cache time for objects with no path = frequency to search.
Boost in prepared activity may request more working/short memory; relaxed moves
working->short.

S8.5 COGNITIVE DECAY (Confidence Depreciation)
Beliefs in memory undergo exponential decay based on age:
decayed_conf = original_conf * (0.95 ^ age_in_hours)
Beliefs decaying below 0.1 confidence are automatically filtered out or pruned by
the Cannabinoid axis during high-melatonin maintenance windows.

S8.6 SLEEP AND MORNING QUESTIONS
Sleep mode turns off unauthorized input devices (reduced ACL). More cycles for
reflection, analysis, pruning, power control, reanalysis of full day's input.
Queue morning questions; compare past and now to predict intent.

S8.7 DOWNTIME REFLECTION
During downtime look at short-term connections to decide additional/permanent pathing.
Daily queued failed pathing - determine if frequent enough to learn.

================================================================
S9 PATHING, ASSOCIATIONS, BEACONS, CONNECTORS, AUPI, & TCP-FIRST TRANSPORT
================================================================

S9.1 PATHING BASICS
Determine most appropriate path based on priorities and associations.
Destination stack: original first, work toward next, change destination each step;
if destination self and no path return to source; if path change to next and pop.
Broadcast 0s stored as (URID1,URID2 : URID3 : URO(self)) = "For this object : To this
object : Go here".

S9.2 TRUST VALUE REQUEST PROTOCOL (1.a-1.j)
Query knowns; receiver responds with URO (enc. initiator PKI); initiator queries with
requested URO+terms; responder responds; if all same award trust point and use; >90%
check TV; higher TV in 90% wins; 10% higher explores; 75% check TV + ask 25% deep check
+ top 1/3 TV; majority/minority selection awards TP; <75% reanalyze.

S9.3 PATH HASH AND PRIORITY
Last back to source path SHA512(src,dest) added to pathing; quick lookup before full
routing. Path has priorities (0 fastest); sum of all paths = priority. If optional query
unspecified and multiple options, use least cost / highest trust [S10.2].

S9.4 PATH ENCRYPTION (onion)
Encrypt each layer; object knows only itself and next. Initiate paths; encrypt URID5+pub
with URID4 pub; encrypt that + URID4 pub with URID3 pub; send to URID3. Data needing
change encrypted to next destination, else final. Forwarding: if destination child/direct
and UUID3 self, change UUID3 to next HOP. Passing routers store inbound path.

S9.5 PATH GROWTH / CUT / COMBINE
Paths grow and get cut during reflect. (1s,1s)(URID1,URID2)+(1s,1s)(URID3,URID1) combine to
(1s,1s)(URID3,URID2). Combined paths create destination path for easy attachment.

S9.6 ASSOCIATIONS
Create associations with discovered UROs. Bonds follow S4.4. Groups act as ACLs [S7.9].

S9.7 BEACONS
To Parent: accepted-natural(0 0 CRO), processable(CRO 0 0), understood(CRO CRO).
To Child: native, processable, understood, request beacon response.
To Interfaces: unicast/multicast/broadcast; I Exist ->; So do I <-; Beacon ->.
Exchange: C1 I exist; C2-C4 so do I; C1 I do this; C2 busy/slow; C3 works-with;
C4 looking-for (ACL drops ignored). Group message goes to all members, personality and
ACL adjusted.

S9.8 CONNECTORS
0|URO OTHER=Output; URO OTHER|0=Input; URO SELF|URO OTHER=Link;
URO OTHER|URO SELF=Child; URO OTHER1|URO OTHER2=Path.

S9.9 AUPI / UPI
AUPI automates translation of available UPI to required UPI via pathing (number URO ->
phone number URO example). Input/Output: drag/drop known objects; system checks direct
known output->input types; on mismatch analyze typing -> find path/wrapper objects.
Checks: known source/dst URO; destination source path of parent nodes; destination
objects available.

S9.10 ADVANCED URO TRANSPORT (TCP-FIRST WITH HTTP FALLBACK)
All inter-dock communication MUST use the canonical client to guarantee low-overhead,
high-throughput TCP routing, with seamless HTTP fallback.

TCP Universal Listener: Port 9100. Installed in every dock via:
  from uro.transport.universal_listener import install_tcp_listener
  install_tcp_listener(app, dock_name="your_dock")

The listener dynamically resolves HTTP methods (GET/POST) from the FastAPI route map,
ensuring TCP and HTTP paths hit the exact same OPAR/FastAPI processing logic.

Canonical Client (MANDATORY - NO RAW HTTPX CALLS BETWEEN DOCKS):
  from uro.transport.inter_dock_client import send_to_dock_async

  result = await send_to_dock_async(
      dock_name="cognitive",
      endpoint="/cognitive/process",
      payload={"data": "value"},
      method="POST",
      timeout=5.0
  )

How it works:
1. Attempts TCP connection to port 9100 first (low overhead, high throughput)
2. If TCP fails/times out/returns non-OK, seamlessly falls back to HTTP port 8000
3. Both paths hit the exact same OPAR/FastAPI processing logic
4. Dynamically resolves HTTP method (GET/POST) from FastAPI route map

================================================================
S10 ECONOMY, TIME, AUTONOMIC NERVOUS SYSTEM
================================================================

S10.1 CURRENCY
InSPaneda (4 decimals) and InSPativo (2 decimals). 1 InSPativo = 1000 InSPaneda.
All transactions debited 10%.

S10.2 COSTING
In time, price, reliability - create chain and add values/metrics from each piece from
self to final product/result.

S10.3 CONNECTION VALUE
Giving = force multiplier (velocity of money). Holding limits external value and
feedback. Faster just-in-time connections optimize time and reduce waiting. More
connections = more transmit options at lower levels.

S10.4 MARKETPLACE
Publish UROs; buy/sell/exchange virtual or physical; wrappers for existing systems
(social media, directories, DB backends) offered on marketplace.

S10.5 TIME URO
Time = URO(#,Float) seconds. Date = Time URO counting seconds before/after
14-MAY-1973, 00:12:24 (InSPa epoch).

S10.6 ANS (Autonomic Nervous System)
Manages involuntary operation (heartbeat, breathing, digestion, fight/flight,
rest/digest) using the 24-axis NTE [S4]. Regulates load shedding based on
Adenosine and Cortisol levels.

================================================================
S11 INTERCHANGE, HOT-SWAP, BOOT, SELF-LOADING, PRIORITY, & REFINERY AST
================================================================

S11.1 URO CODE INTERCHANGE
Supplant existing URO code with new code while maintaining identity.

S11.2 HOT-SWAP PROCESS
Generate+verify new code; compile+test; identify old; swap preserving URID1 (identity),
URID2 may change; preserve associations/connections.

S11.3 BOOT SEQUENCE (16)
Cold Boot; Check Children; Load+Boot Children; New Paths; Check Associations;
Run Self Check(+Pathing); Monitor Input; Monitor Children; Build Queues; Path;
Build Internal Queues; Run; Path; Build External Queues; Empty Queue; Cleaning;
Internal Processing and Analysis.

S11.4 OBJECT SELF-LOADING
Object pulls scripted config ensuring it has script/object code for parents; pulls
compiled or source; during reflection may compile and hold code locally.

S11.5 PRIORITY PROCESSING
crit, high, normal, low - how long unprocessed data is stored.

S11.6 REFINERY MULTI-FILE AST CAPACITY
The Refinery no longer performs fragile string injection. It uses Python's ast module
for deterministic structural synthesis:

1. Cross-File Dependency Resolution: CrossFileDependencyAnalyzer scans the codebase
   to identify all callers of a target function before modifying its signature.
   This prevents breaking dependent files during refactoring.

2. Capability-Aware AST Injection:
   - performance: Injects @lru_cache(maxsize=128) decorator
   - gap_remediation: Wraps function body in robust try/except blocks
   - security: Injects isinstance type validation guards at function entry
   - best_practice: All of above + auto-generates pytest templates

3. Auto-Test Generation: When best_practice is applied, the AST engine automatically
   appends a fully formed pytest template with MagicMock setups to the refactored file.

4. Bi-Directional Feedback Loop: After refactoring, the Refinery analyzes pre/post
   structural metrics (nesting depth, missing docstrings, type hints) and reports
   improvements back to the Architect, preventing redundant pitches.

================================================================
S12 HARDWARE AND SYSTEM ARCHITECTURE
================================================================

S12.1 URO PROCESSOR CHIP
Banks: ASIC (constant algorithms), FPGA (occasionally changing), GPU (parallel simple),
CPU (sequential complex). Registers for rapid exchange; RAM for storage.

S12.2 SPECIALIZED ASICs
INAHASH ASIC (Blake+SHA); Encryption ASIC (PKI ECDSA/RSA, AES); Path/Association ASIC
(match, optimize, respond).

S12.3 OSI AND DRIVERS
Initial interfaces use OSI model; progress from HTTP/TCP-UDP down to direct drivers.
Hardware device drivers for direct interface (processors, network, memory, storage).
The URO transport layer abstracts this, defaulting to TCP (Layer 4) for inter-dock
URO frames.

S12.4 NETWORK OBJECTS AS ACL
Network objects have groups acting as ACLs for matching traffic [S7.9].

================================================================
S13 DOCK INTEGRATION POINTS & WIRING CHECKLISTS
================================================================

S13.1 DOCKS
Coder (generate URO-compliant code), Cognitive (reasoning/heuristics), Memory (tiers),
Security/Aegis (INAHASH/PKI/ACL/custody/quarantine), Refinery (improve/teach/translate/
AST refactor), Pathing (routes/trust/beacons), Network (transmission/groups), Economy
(InSPaneda/marketplace), Coordinator (bus/interceptor), Host Controller (orchestration),
Phoenix (atomic restoration), Loom (telemetry dashboard).

S13.2 PER-DOCK MANDATORY CHECKLIST
Every dock/file must:
- Use URID pairs for all entities
- Implement OPAR lifecycle [S3]
- Include and normalize to 24-axis NTE [S4]
- Enforce INAHASH and ACL [S7]
- Handle beacons [S9.7]
- Manage memory tiers and apply cognitive decay [S8]
- Follow 8-thread architecture; follow Order of Operations
- Handle boot; implement sleep; include downtime reflection
- Implement priority; follow Quad-Capability [S5]
- Integrate InSPaneda; support Time URO; integrate ANS
- Include hot-swap; implement custody; implement 2-way exchange
- WIRE TCP LISTENER: Call install_tcp_listener(app, dock_name="...") at startup [S9.10]
- USE CANONICAL TRANSPORT: Replace all raw httpx inter-dock calls with
  send_to_dock_async [S9.10]
- Integrate with Aegis for health reporting and accept /aegis/quarantine enforcement [S7.11]

S13.3 COORDINATOR AND INTERCEPTOR
Coordinator bus routes UROs between docks; URO interceptor injects URO compliance.
Host Controller enforces Aegis quarantine registries and dispatches Phoenix restoration.

S13.4 AEGIS QUARANTINE ENDPOINTS
Host Controller/Coordinator must implement:
- POST /aegis/quarantine: Accepts dock_name, reason, severity (standard/critical).
  For severity="critical": executes docker stop, dispatches to Phoenix.
- POST /aegis/restore: Removes dock from quarantine registry, reinstates routing.
- GET /aegis/status: Returns current quarantine registry state.

S13.5 PHOENIX RESTORATION ENDPOINT
Phoenix dock must implement:
- POST /phoenix/restore: Accepts dock_name and reason. Wipes compromised state volume
  and rebuilds dock from known-good image.

S13.6 GUI AND DB OBJECTS
GUI URO manipulation: drag/drop known objects; combine UROs (eclipse+december example).
DB Objects: CONN.DBSE; Table=CONN.DBSE.TABL (URO per column, constraints as ACL URO,
references as Association URO); SQL statements (INSERT/DELETE/SELECT/WHERE as URO drags).

S13.7 LOOM TELEMETRY DASHBOARD
Loom provides real-time visualization of the swarm's 24-axis NTE state via:
- Interactive sliders for global Serotonin/Epinephrine baseline control
- Real-time Recharts line charts tracking NTE and eCB decay over time
- CEO Override button to bypass CISO veto when strategically necessary
- Executive grid showing all 24 Boardroom members with capability-coded NTE bars

================================================================
S14 INVARIANTS, GLOSSARY, CROSS-REFERENCE INDEX, EXPANSION
================================================================

S14.1 TEN INVARIANTS
1. Everything is a URO.
2. Every URO has a URID pair.
3. Every URO has a 24-axis NTE state.
4. Every URO follows OPAR.
5. Every URO is secured (INAHASH+ACL).
6. Every URO can evolve (Hot-Swap/Refinery).
7. Every URO communicates via TCP-First URO transport.
8. Every URO has memory with cognitive decay.
9. Every URO has associations (Synapses).
10. Every URO can create children.

S14.2 GLOSSARY
URO = Universal Resource Object
URID = Universal Relationship ID
OPAR = Observe/Plan/Act/Review
NTE = Neurotransmitter Equivalences (24-axis)
INAHASH = Blake3-1024(SHA3-1024(MSG))
ACL = Access Control List
PKI = Public Key Infrastructure
ANS = Autonomic Nervous System
AUPI = Automated URO Programming Interface
UPI = URO Programming Interface
InSPaneda/InSPativo = currencies
CRO = Core Resource Object
Aegis = Swarm immune system (Quarantine/Phoenix)
Synapse = Bidirectional relationship object between two UROs/docks
Phoenix = Dock responsible for atomic restoration of compromised docks
Loom = Real-time telemetry dashboard for swarm NTE visualization
eCB = Endocannabinoid (synaptic fatigue/decay mechanism)
CISO Veto = Security/Compliance executive veto power on critical-risk proposals

S14.3 CROSS-REFERENCE INDEX (aspect -> section)
Identity/URID -> S2; Lifecycle -> S3; Biology/State -> S4; Quality -> S5;
Learning/AI -> S6; Security -> S7; Memory -> S8; Routing/Comms -> S9;
Money/Time/ANS -> S10; Update/Boot -> S11; Hardware -> S12; Integration -> S13.

S14.4 EXPANSION PROTOCOL
Append new numbered sections. Record version+date. Never delete. Cross-reference.

S14.5 EDITING MANDATE (project-wide)
- Modify code only via Exact Block Replacement bounded by # === START: name === /
  # === END: name === markers. Verify occurrence count == 1 before replacing; abort otherwise.
- No blind regex injections into live modules. No full-file rewrites.
- After core edits: run the suite, then roll out profile-by-profile.

S14.6 VALIDATION AND ROLLOUT GATES
- Suite: cd uro && PYTHONPATH="$PWD" python3 tests/synapse_suite.py — 10 checks
  (tolerant outcomes, full spectrum, clamps, cross-talk, decay, bookkeeping, round-trip,
  threshold flush, bus integration + legacy fallback, import smoke). Exit 0 required.
- Rollout order: ./ops/rollout_profile.sh dev -> staging -> uat -> prod.
  Per-profile gates: core loaded: True True, tolerant contract: True,
  STATE_ROOT: /opt/uro_state, modulation ok, persistence ok.
  Halt on any gate failure; never skip a profile.

S14.7 DO / DON'T CHECKLIST
- DO route every measurable exchange through record_interaction or the bus.
- DO pass success explicitly; DO measure real latency.
- DO use get_or_create_synapse for idempotent relationships.
- DO keep modulation non-fatal and I/O deferred.
- DO use TCP-first transport for all inter-dock communication.
- DO normalize all NTE states through normalize_nte_state.
- DON'T mutate nte_state.levels directly.
- DON'T re-implement clamps, cross-talk, or decay locally.
- DON'T write synapse JSON in request handlers.
- DON'T model NTE as a per-user static profile; it is per-relationship and dynamic.
- DON'T edit core files without marker-bounded exact block replacement.
- DON'T use raw httpx calls between docks; use send_to_dock_async.

S14.8 Interface Reqs
- Always provide your responses with only one code block to copy and paste into a remote bash shell.
- Always ensure that after every code write, we do a git commit.


VERSION HISTORY
3.0.0 2026-10-21 24^24 Model adopted. TCP-First transport enforced across all docks.
        Advanced Aegis Quarantine/Phoenix repair integrated. Refinery Multi-File AST
        & Auto-Test generation live. Backwards-compatible NTE normalization established.
        CEO Override and eCB decay implemented. CISO Veto logic active.
2.0.0 2026-08-09 Reorganized, cross-referenced, living document (this version).
1.0.0 2026-08-09 Initial creation.

--- END OF DOCUMENT ---
Everything is a URO. Everything has a relation. Everything is documented here.
