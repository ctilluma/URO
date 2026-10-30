# URO Library API Reference

Generated from source by _BUILD/tools/generate_api_reference.py.
Covers the measured canonical surface (16 suites, 160 checks, uro-build/phase-16-done).
Legacy shim, vauros_*, and dock-internal layers are excluded by ADR.

## primitives

### uro.constants

Global constants for the URO reference implementation.

### uro.exceptions

Exception hierarchy for the URO reference implementation.

#### class UROError

Base class for all URO-related errors.

#### class URIDError

Malformed or out-of-range URID.

#### class UROStructureError

Structural invariant violation.

#### class PathingError

Path cannot be resolved or is invalid.

#### class AssociationError

Association cannot be formed or is invalid.

#### class SecurityError

Base class for security subsystem errors.

#### class HashError

Hashing operation failed.

#### class EncryptionError

Encryption/decryption failed.

#### class IdentityError

Identity verification failed.

#### class ACLError

ACL evaluation is invalid.

#### class PolicyError

Policy URO cannot be evaluated.

#### class InterchangeError

Serialization/deserialization failed.

#### class ConnectorError

Database / connector fault.

#### class SchedulerError

Scheduler fault.

#### class TranslationError

AUPI translation fault.

#### class PaymentError

InSPaneda payment fault.

#### class OPARError

OPAR lifecycle fault (observe/plan/act/review).

#### class SynapseError

Synapse vector or modulation fault.

#### class UROMemoryError

Memory hierarchy or consolidation fault.

#### class BootError

System boot or self-check fault.

#### class CustodyError

Custody chain or 2-way exchange fault.

#### class HeaderIntegrityError

Header integrity (Blake2-256) verification failed.

### uro.types

Shared type aliases and Protocols for the URO reference implementation.

#### class UROCapable

PURPOSE: Protocol for objects satisfying the Fractal URO Mandate.

- `to_dict(self) -> 'Dict[str, Any]'`

- `__init__(self, *args, **kwargs)`

#### class OPARCapable

PURPOSE: Protocol for OPAR-24 compliant capabilities (RFC 13).

- `execute(self, stimulus: 'Any', nte: 'Optional[NTELevels]' = None) -> 'Dict[str, Any]'`

- `__init__(self, *args, **kwargs)`

### uro.genesis_trust

MODULE: Genesis Trust Enforcement INTENT: Enforce the Genesis Rule: child UROs start at 100% trust to parent,

#### class GenesisTrustEnforcer

Enforces the Genesis Trust Rule. Child UROs (with parent_inahash) start at 100% trust.

## core

### uro.core.urid

URID - Universal Relationship IDentifier (256-bit identity).

#### new_uuid() -> '_uuid.UUID'

Generate a new random (UUIDv4) 128-bit UUID.

#### class URID

A 256-bit Universal Relationship IDentifier (UUID1||UUID2).

- `__init__(self, uuid1: '_uuid.UUID' = None, uuid2: '_uuid.UUID' = None) -> 'None'` - Construct a URID from two UUID halves.

- `to_int(self) -> 'int'` - Return the URID as a 256-bit integer.

- `to_bytes(self) -> 'bytes'` - Return the URID as 32 big-endian bytes.

- `to_hex(self) -> 'str'` - Return a zero-padded 64-character hex string.

- `is_zero(self) -> 'bool'` - True if all-zero (nothing/structure).

- `is_ones(self) -> 'bool'` - True if all-ones (everything/group).

#### new_urid() -> 'URID'

Convenience: create a fresh random URID.

### uro.core.uro

The core URO class - the universal relationship object.

#### sha128(data: 'bytes') -> 'bytes'

128-bit digest (SHA-256 truncated to 16 bytes).

#### class URO

A Universal Relationship Object: (source URID, identifier URID).

- `__init__(self, urid1: 'URID' = None, urid2: 'URID' = None, payload: 'Any' = None, parent: "Optional['URO']" = None, **kwargs) -> 'None'` - Construct a URO from two URIDs (auto-generated if omitted). Absorbs genesis kwargs.

- `link(self) -> 'bytes'` - Compute the 512-bit relationship link.

- `add_child(self, child: "'URO'") -> 'None'` - Attach a child URO.

- `get_child(self, urid: 'URID') -> "Optional['URO']"` - Return a child URO by URID, or None.

- `children_of(self) -> "Iterable['URO']"` - Yield all child UROs.

- `associate(self, association: 'Any') -> 'None'` - Attach an Association URO.

- `add_path(self, path: 'Any') -> 'None'` - Attach a Path URO.

### uro.core.header

URO header construction and integrity verification (RFC 7).

#### build_header(src_len: 'int', dst_len: 'int', pay_len: 'int', future: 'int' = 0) -> 'bytes'

PURPOSE: Pack the four 64-bit length fields and append their Blake2-256.

#### parse_header(blob: 'bytes') -> 'dict'

PURPOSE: Unpack and integrity-check a header blob; raise on mismatch.

#### verify_header(blob: 'bytes') -> 'bool'

PURPOSE: Boolean header integrity probe (non-raising).

### uro.core.components

Enforcement of the ten mandatory URO components (RFC 8).

#### missing_components(obj: 'Any') -> 'List[str]'

PURPOSE: List the RFC 8 components absent from obj.

#### enforce_components(obj: 'Any') -> 'None'

PURPOSE: Raise UROStructureError when any mandatory component is missing.

### uro.core.inheritance

Capability inheritance and abstraction helpers (RFC 9, RFC 2.4).

#### inherit_capabilities(child: 'Any', parent: 'Any') -> 'dict'

PURPOSE: Merge parent capabilities into child; child entries win (RFC 9.1).

#### resolve_capability(obj: 'Any', name: 'str') -> 'Any'

PURPOSE: Walk the parent chain upward to find a capability by name.

#### inherit_security_context(child: 'Any', parent: 'Any') -> 'Any'

PURPOSE: Child inherits the parent ACL/security context (RFC 2.4).

### uro.core.datetime_uro

Time and Date UROs anchored to the InSPa epoch (RFC 6).

#### class TimeURO

PURPOSE: Time as a URO wrapping a float seconds value (RFC 6.1).

- `__init__(self, seconds: 'float') -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `to_date_uro(self) -> "'DateURO'"` - PURPOSE: Convert absolute seconds to epoch-relative DateURO (RFC 6.2).

- `greater(self, other)` - PURPOSE: RFC 6.4 condition: greater.

- `less(self, other)` - PURPOSE: RFC 6.4 condition: less.

- `equal(self, other)` - PURPOSE: RFC 6.4 condition: equal.

- `between(self, lo, hi)` - PURPOSE: RFC 6.4 condition: between.

- `before(self, other)` - PURPOSE: RFC 6.4 condition: before.

- `after(self, other)` - PURPOSE: RFC 6.4 condition: after.

#### class DateURO

PURPOSE: Date as seconds before/after 14-MAY-1973 00:12:24 UTC (RFC 6.2).

- `__init__(self, offset_seconds: 'float', expires_at: 'float' = None, renew: 'bool' = False) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `to_datetime(self) -> '_dt.datetime'` - PURPOSE: Render the offset back as an aware UTC datetime.

- `expiration_action(self, now_seconds: 'float' = None) -> 'str'` - PURPOSE: RFC 6.5: renew when flagged, else delete (temp objects).

### uro.core.space

UROSpace - the communal registry/graph of all UROs and relationships.

#### class UROSpace

A shared space holding UROs and the relationships between them.

- `__init__(self, name: 'str' = 'root') -> 'None'` - Create a new UROSpace.

- `register(self, uro: 'URO') -> 'URO'` - Register an object URO.

- `register_relationship(self, relationship_uro: 'URO') -> 'URO'` - Register a relationship URO by its 512-bit link.

- `get(self, urid1: 'URID', urid2: 'URID') -> 'Optional[URO]'` - Look up an object URO by its two URIDs.

- `relationship(self, link: 'bytes') -> 'Optional[URO]'` - Look up a relationship URO by its link bytes.

- `objects(self) -> 'Iterable[URO]'` - Yield all object UROs.

- `relationships(self) -> 'Iterable[URO]'` - Yield all relationship UROs.

- `neighbors(self, uro: 'URO') -> 'List[URO]'` - Return UROs directly associated with the given URO.

## nte

### uro.nte.axes

MODULE: NTE Axes (24-Axis Canonical System) INTENT: Define the 24 neurotransmitter/cognitive axes that form the swarm's governance

#### class NTEAxis

The 24 neurotransmitter/cognitive equivalences.

#### class NTEAxisGovernance

Governance role and cross-talk for each NTE axis.

Fields:

- axis: <enum 'NTEAxis'>
- niche: <class 'str'>
- governance_role: <class 'str'>
- cross_talk: typing.Dict[str, str]

#### class CognitiveAxis

Deprecated compatibility enum for the 12 cognitive axes. Canonical state uses NTEAxis, which now contains all 24 axes.

#### nte24(state=None, baseline=50.0)

Full 24-axis state as {axis_value: level}, baseline-filled.

### uro.nte.state

MODULE: NTE State URO (Collection of Levels, 24-Axis Canonical) INTENT: A URO representing the complete NTE state (all 24 axes). This is the

#### class NTEStateURO

A URO representing the complete NTE state (all 24 axes). This is the fast-path reference for checking emotional state.

Fields:

- urid1: <class 'uro.core.urid.URID'>
- urid2: <class 'uro.core.urid.URID'>
- levels: typing.Dict[uro.nte.axes.NTEAxis, float]
- axis_refs: typing.Dict[uro.nte.axes.NTEAxis, uro.core.urid.URID]
- inahash: <class 'str'>
- parent_inahash: str | None
- timestamp: <class 'float'>

- `compute_inahash(self) -> 'str'` - Compute the INAHASH seal.

- `seal(self) -> 'None'` - Seal this URO.

- `get_level(self, axis: 'NTEAxis') -> 'float'` - Get the level for a specific axis.

- `set_level(self, axis: 'NTEAxis', level: 'float') -> 'None'` - Set the level for a specific axis.

- `apply_delta(self, axis: 'NTEAxis', delta: 'float') -> 'None'` - Apply a delta to a specific axis.

- `get_dominant_axis(self) -> 'NTEAxis'` - Get the axis with the highest level.

- `is_balanced(self, threshold: 'float' = 15.0) -> 'bool'` - Check if all axes are within threshold of baseline (50).

### uro.nte.level

MODULE: NTE Level URO (Per-Axis State) INTENT: A URO representing the level of a single NTE axis. Each level is its

#### class NTELevelURO

A URO representing the level of a single NTE axis. This is a first-class URO with its own identity, lineage, and custody.

Fields:

- urid1: <class 'uro.core.urid.URID'>
- urid2: <class 'uro.core.urid.URID'>
- axis: <enum 'NTEAxis'>
- level: <class 'float'>
- baseline: <class 'float'>
- inahash: <class 'str'>
- parent_inahash: str | None
- timestamp: <class 'float'>

- `compute_inahash(self) -> 'str'` - Compute the INAHASH seal.

- `seal(self) -> 'None'` - Seal this URO.

- `set_level(self, new_level: 'float') -> 'None'` - Set the level and update timestamp.

- `apply_delta(self, delta: 'float') -> 'None'` - Apply a delta to the level.

### uro.nte.cross_talk

MODULE: NTE Cross-Talk URO INTENT: Canonical multidimensional cross-talk field for all 24 NTE axes.

#### class CrossTalkWhen

str(object='') -> str str(bytes_or_buffer[, encoding[, errors]]) -> str

#### class CrossTalkEdgeURO

One directed cross-talk influence. Source axis affects target axis.

Fields:

- source: <enum 'NTEAxis'>
- target: <enum 'NTEAxis'>
- sign: <class 'float'>
- gain: <class 'float'>
- threshold: <class 'float'>
- log_k: <class 'float'>
- when: <enum 'CrossTalkWhen'>
- note: <class 'str'>

#### class CrossTalkPolicyURO

Compact category-level rule. This lets the cross-talk URO remain succinct while still expanding

Fields:

- source_category: <class 'str'>
- target_category: <class 'str'>
- sign: <class 'float'>
- gain: <class 'float'>
- threshold: <class 'float'>
- log_k: <class 'float'>
- when: <enum 'CrossTalkWhen'>
- note: <class 'str'>

#### class NTECrossTalkURO

Canonical multidimensional cross-talk field for all 24 NTE axes. The field is represented succinctly by:

Fields:

- urid1: <class 'uro.core.urid.URID'>
- urid2: <class 'uro.core.urid.URID'>
- version: <class 'str'>
- baseline: <class 'float'>
- max_pass_delta: <class 'float'>
- categories: typing.Dict[uro.nte.axes.NTEAxis, str]
- policies: typing.List[uro.nte.cross_talk.CrossTalkPolicyURO]
- overrides: typing.List[uro.nte.cross_talk.CrossTalkEdgeURO]
- inahash: <class 'str'>

- `compute_inahash(self) -> 'str'`

- `seal(self) -> 'None'`

- `expanded_edges(self) -> 'List[CrossTalkEdgeURO]'` - Expand compact policies into explicit directed edges.

#### apply_cross_talk_uro(levels: 'Dict[NTEAxis, float]', cross_talk: 'NTECrossTalkURO') -> 'Dict[NTEAxis, float]'

Apply one full multidimensional cross-talk pass. Uses a snapshot of the input levels so edge order does not create

#### default_cross_talk_uro() -> 'NTECrossTalkURO'

Canonical default 24-axis cross-talk field. This is intentionally succinct but expands to a full multidimensional

### uro.nte.polarity

Polarity table for all 24 NTE axes (RFC 25).

#### polarity_for(axis: 'NTEAxis') -> 'Tuple[str, str]'

PURPOSE: Return (negative/antagonist, positive/protagonist) descriptors (RFC 25).

### uro.nte.math_influence

Weighting curves and reward/punishment formulas (RFC 27).

#### class InfluenceType

PURPOSE: The seven canonical influence curves (RFC 27).

#### apply_influence(kind: 'InfluenceType', x: 'float') -> 'float'

PURPOSE: Evaluate the canonical weighting curve delta for x (RFC 27).

#### reward_motivation(motivation: 'float', x: 'float') -> 'float'

PURPOSE: RFC 27.1 reward: Motivation += x*log10(X+10).

#### punish_motivation(motivation: 'float', dopamine: 'float') -> 'float'

PURPOSE: RFC 27.1 punishment: Motivation += dopamine (decrease).

#### cost_to_buy(points: 'float') -> 'float'

PURPOSE: RFC 27.1 marketplace cost (log10(X^3)^2)/3 capped at 100 points.

### uro.nte.firing

Firing calculation and potentiator/receptor mechanics (RFC 29/30).

#### fire_decision(chance_pct: 'float', rand_1_100: 'float') -> 'bool'

PURPOSE: RFC 29.1: fire when the random draw is at or below the chance.

#### transmit_signal(fires_fraction: 'float') -> 'float'

PURPOSE: RFC 29.2: transmit signal in the 0-2 range (fires fraction x 2).

#### fire_multiplier(fired: 'bool') -> 'float'

PURPOSE: RFC 29.2: 1.06 when fired else 0.40.

#### activity(antagonists: 'float', protagonists: 'float') -> 'float'

PURPOSE: RFC 30.2: Activity = antagonists - protagonists.

#### min_fire_chance(antagonists: 'float', receptors: 'float') -> 'float'

PURPOSE: RFC 30.3 min bound percent; 0 when antags exceed receptors.

#### max_fire_chance(protagonists: 'float', receptors: 'float') -> 'float'

PURPOSE: RFC 30.3 max bound percent; 100 when protags exceed receptors.

### uro.nte.reward

D1/D2 reward-punishment, habit formation, bi-directional R/P (RFC 31/32).

#### class RewardOutcome

PURPOSE: Typed D1/D2 result (RFC 31.1).

Fields:

- kind: str
- stimulation_factor: float
- trust_delta: float
- action_directive: str

- `__init__(self, kind: 'str', stimulation_factor: 'float', trust_delta: 'float', action_directive: 'str') -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### reward_event(success: 'bool', trust_weight: 'float' = 1.0) -> 'RewardOutcome'

PURPOSE: D1 reward vs D2 punishment, trust-weighted (RFC 31.2.4).

#### is_habit(trust: 'float', threshold: 'float' = 90.0) -> 'bool'

PURPOSE: RFC 32.1: trust so high it becomes the go-to firing mechanism.

#### habit_broken(habit_strength: 'float', new_rp_magnitude: 'float') -> 'bool'

PURPOSE: RFC 32.2: habit breaks only when new R/P outweighs the old.

#### propagate_rp(chain: 'List[str]', fault_index: 'Optional[int]', reward: 'bool') -> 'dict'

PURPOSE: RFC 32.3 bi-directional R/P; punishment stops at fault else cascades.

### uro.nte.ans

Autonomic Nervous System branch mapping and thresholds (RFC 34).

#### dominant_branch(levels: 'Dict') -> 'str'

PURPOSE: Classify fight/flight vs rest/digest from levels (RFC 34.3).

#### regulation_actions(levels: 'Dict') -> 'List[str]'

PURPOSE: Threshold-driven involuntary actions (RFC 34.3 items 3-4).

### uro.nte.neurotransmitters

Neurotransmitter Equivalences and synapse firing model.

#### class NTEState

NTEState(levels=None, **kwargs)

Fields:

- levels: Dict[NTE, float]

- `__init__(self, levels=None, **kwargs)` - Accept kwargs like epinephrine=0.5, dopamine=0.5 for dock compatibility.

- `to_canonical(self) -> 'dict'` - PURPOSE: Bridge legacy [0,1] levels to canonical 24-axis [0,100] state (ADR-012).

- `set(self, nte: 'NTE', value: 'float') -> 'None'` - Set the level of an NTE.

- `get(self, nte: 'NTE') -> 'float'` - Return the level of an NTE.

#### class Receptor

A receptor that binds protagonist and antagonist signals.

Fields:

- receptor_count: int
- potentiators: float
- antagonists: float

- `activity_ratio(self) -> 'float'` - Compute the activation ratio per the NTE firing model.

- `__init__(self, receptor_count: 'int' = 10, potentiators: 'float' = 0.0, antagonists: 'float' = 0.0) -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class Synapse

A junction that decides (non-binary) whether to transmit.

- `__init__(self, receptor: 'Receptor', nte: 'NTEState | None' = None) -> 'None'` - Create a synapse.

- `fire(self) -> 'bool'` - Decide whether the synapse fires.

### uro.nte.nte_state

Legacy-module 24-axis NTE state (ADR-011/013); canonical model is uro.nte.state.NTEStateURO.

#### class NTEState

PURPOSE: 24-axis neuro-chemical state on the legacy [0,1] scale (ADR-013).

- `__init__(self, **kwargs)` - PURPOSE: Accept canonical axis kwargs plus legacy extras; default 0.5.

- `as_dict(self) -> dict` - PURPOSE: All 24 canonical axes on the legacy [0,1] scale.

- `to_canonical(self) -> dict` - PURPOSE: Bridge legacy [0,1] levels to canonical 24-axis [0,100] state.

## synapse

### uro.synapse.engine

MODULE: Synapse Modulation Engine INTENT: Bidirectional, 24-axis neurochemical modulation of the relationship

#### InteractionOutcome(success: 'bool' = True, latency_ms: 'float' = 0.0, novelty: 'float' = 0.0, load: 'float' = 0.0, trust_signal: 'float' = 0.0) -> 'dict'

Normalized outcome vector for one URO-to-URO interaction.

#### apply_cross_talk(levels)

#### modulate_synapse(synapse, outcome: 'dict') -> 'Dict[NTEAxis, float]'

Apply one interaction outcome to all 24 canonical axes.

#### decay_synapse(synapse, rate: 'float' = 0.02) -> 'Dict[NTEAxis, float]'

Homeostatic decay of all 24 canonical axes toward baseline.

### uro.synapse.vector

MODULE: Synapse Vector URO INTENT: The emotional state between two UROs. NTE state is relational, not

#### class SynapseVectorURO

The emotional state between two UROs (a synapse). NTE state is relational: the Aegis↔Chaos synapse has its own state,

Fields:

- urid1: <class 'uro.core.urid.URID'>
- urid2: <class 'uro.core.urid.URID'>
- synapse_urid: <class 'uro.core.urid.URID'>
- nte_state: <class 'uro.nte.state.NTEStateURO'>
- topic_trusts: typing.Dict[str, uro.synapse.topic_trust.TopicTrustURO]
- overall_trust: <class 'float'>
- use_count: <class 'int'>
- success_count: <class 'int'>
- last_used: <class 'float'>
- inahash: <class 'str'>
- parent_inahash: str | None
- created_at: <class 'float'>
- last_updated: <class 'float'>

- `compute_inahash(self) -> 'str'` - Compute the INAHASH seal.

- `seal(self) -> 'None'` - Seal this synapse.

- `get_topic_trust(self, topic: 'str') -> 'Optional[TopicTrustURO]'` - Get trust URO for a specific topic.

- `add_topic_trust(self, topic: 'str', initial_trust: 'float' = 0.0) -> 'TopicTrustURO'` - Add a new topic trust URO.

- `update_topic_trust(self, topic: 'str', delta: 'float', nte_context: 'dict') -> 'None'` - Update trust on a specific topic.

- `record_use(self, success: 'bool') -> 'None'` - Record a use of this synapse.

- `record_interaction(self, outcome: 'dict') -> 'None'` - Record one URO-to-URO interaction and modulate all 24 NTE axes.

- `get_success_rate(self) -> 'float'` - Get the success rate for this synapse.

- `genesis_trust_level(self) -> 'float'` - Get the initial trust level based on the Genesis Rule.

- `is_child(self) -> 'bool'` - PURPOSE: Lineage probe - true when this synapse carries a parent seal.

### uro.synapse.persistence

MODULE: Synapse Durable Persistence INTENT: Disk-backed storage for SynapseVectorURO objects so the relationship

#### save_synapse(synapse: 'SynapseVectorURO') -> 'Path'

Seal and write one synapse to disk; update the pair index.

#### load_synapse(synapse_urid) -> 'Optional[SynapseVectorURO]'

Load one synapse from disk by its synapse URID.

#### list_synapse_ids() -> 'List[str]'

#### get_or_create_synapse(urid1, urid2) -> 'SynapseVectorURO'

Return the existing synapse for an endpoint pair, or create and save it.

#### modulate_and_persist(synapse: 'SynapseVectorURO', outcome: 'dict') -> 'dict'

Modulate all 24 axes for one interaction, then persist immediately.

### uro.synapse.topic_trust

MODULE: Per-Topic Trust URO INTENT: Trust is per-relationship AND per-topic. Two UROs may have high trust

#### class TopicTrustURO

Trust on a specific topic within a synapse. Example: Aegis↔Chaos synapse has high trust on "security_analysis" topic

Fields:

- urid1: <class 'uro.core.urid.URID'>
- urid2: <class 'uro.core.urid.URID'>
- topic: <class 'str'>
- trust_level: <class 'float'>
- confidence: <class 'float'>
- openness: <class 'float'>
- nte_modulation: <class 'dict'>
- inahash: <class 'str'>
- parent_inahash: str | None
- timestamp: <class 'float'>

- `compute_inahash(self) -> 'str'` - Compute the INAHASH seal.

- `seal(self) -> 'None'` - Seal this URO.

- `update_trust(self, delta: 'float', nte_context: 'dict') -> 'None'` - Update trust based on outcome and NTE context.

## security

### uro.security.hashing

Multi-standard hashing primitives (INAHASH and helpers).

#### sha3_1024(data: 'bytes') -> 'bytes'

1024-bit SHA-3 family digest via SHAKE-256 (FIPS 202).

#### blake3_1024(data: 'bytes') -> 'bytes'

1024-bit BLAKE-family digest (native BLAKE3 or BLAKE2b profile).

#### inahash(message: 'bytes') -> 'bytes'

INAHASH = Blake3-1024( SHA3-1024( MSG ) ).

#### sha512(data: 'bytes') -> 'bytes'

SHA-512 digest.

#### sha512x3(data: 'bytes') -> 'bytes'

Triple-iterated SHA-512 (core-key derivation).

#### blake2b_256(data: 'bytes') -> 'bytes'

256-bit BLAKE2b digest (header checksum).

#### sha128(data: 'bytes') -> 'bytes'

128-bit digest (SHA-256 truncated).

### uro.security.encryption

Symmetric encryption primitives for URO data and keys.

#### xor_bytes(a: 'bytes', b: 'bytes') -> 'bytes'

XOR two equal-length byte strings.

#### derive_key_from_password(password: 'bytes', encrypt_key: 'bytes') -> 'bytes'

key = SHA512x3(password) XOR encrypt_key.

#### split_1024_key(key: 'bytes') -> 'Tuple[bytes, bytes]'

Split a 128-byte key into (K1, K2).

#### encrypt(key: 'bytes', plaintext: 'bytes') -> 'bytes'

Single-layer encrypt.

#### decrypt(key: 'bytes', blob: 'bytes') -> 'bytes'

Single-layer decrypt.

#### double_encrypt(key_1024: 'bytes', plaintext: 'bytes') -> 'bytes'

Double-layer encrypt using a 1024-bit key (K1 then K2).

#### double_decrypt(key_1024: 'bytes', blob: 'bytes') -> 'bytes'

Reverse double_encrypt.

### uro.security.pki

PKI public-key UROs and URO signatures.

#### class PublicKeyURO

A URO representing a public key and its lifecycle instants.

- `__init__(self, public_key: 'bytes') -> 'None'` - Create a public-key URO issued now.

- `set_expiration(self, when: 'DateURO') -> 'None'` - Set the expiration instant.

- `revoke(self) -> 'None'` - Mark this key as revoked as of now.

- `is_valid(self) -> 'bool'` - Return True if the key is not revoked.

#### class UROSignature

A signature binding an object, signer, owner, and content digest.

- `__init__(self, signed_object: 'URO', signer: 'URO', trust_owner: 'URO', digest: 'bytes', signature: 'bytes') -> 'None'` - Create a signature URO.

#### sign_uro(signed_object: 'URO', signer: 'URO', trust_owner: 'URO', private_key: 'bytes') -> 'UROSignature'

Sign a URO, producing a UROSignature.

#### verify_signature(sig: 'UROSignature', private_key: 'bytes') -> 'bool'

Verify a UROSignature against the claimed content and keys.

### uro.security.identity

Identity verification and tokens.

#### class IdentityToken

A token maintaining verified identity.

Fields:

- token: str
- subject: str
- indefinite: bool
- revoked: bool

- `__init__(self, token: 'str', subject: 'str', indefinite: 'bool' = False, revoked: 'bool' = False) -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class Identity

Represents a verified identity bound to a URO.

- `__init__(self, subject: 'str', password: 'bytes') -> 'None'` - Create and register an identity from a password.

- `verify_password(self, password: 'bytes') -> 'bool'` - Verify a candidate password against the stored verifier.

- `bind_time_uro(self, time_uro) -> 'None'` - PURPOSE: RFC 54.4: assign the response-and-time URO to a DateURO.

- `issue_token(self, indefinite: 'bool' = False) -> 'IdentityToken'` - Issue a new identity token.

- `validate_token(self, token: 'str') -> 'bool'` - Check whether a token is currently valid.

- `revoke_token(self, token: 'str') -> 'None'` - Revoke an issued token.

### uro.security.policy

Policy UROs composing multiple ACLs.

#### class PolicyURO

A URO that carries and evaluates a set of ACLs.

- `__init__(self, name: 'str') -> 'None'` - Create a named Policy URO.

- `add_acl(self, scope: 'str', acl: 'ACL', override: 'bool' = False) -> "'PolicyURO'"` - PURPOSE: Attach an ACL to a named scope; override groups decide first (RFC 55.1).

- `evaluate(self, scope: 'str', subject: 'str', permission: 'str') -> 'bool'` - PURPOSE: Evaluate access; override-group entries decide first (RFC 55.1).

- `scopes(self) -> 'List[str]'` - Return the list of configured scopes.

### uro.security.acl

Access Control Lists with binary combinators.

#### class ACLCombinator

Binary combinators used to fold ACL entry results.

#### class ACLEntry

A single ACL rule.

Fields:

- subject: str
- permission: str
- allow: bool

- `__init__(self, subject: 'str', permission: 'str', allow: 'bool' = True) -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class ACL

An ACL that evaluates entries with a combinator.

- `__init__(self, combinator: 'ACLCombinator' = <ACLCombinator.AND: 1>) -> 'None'` - Create an ACL.

- `add(self, entry: 'ACLEntry') -> "'ACL'"` - Append an entry.

- `evaluate(self, subject: 'str', permission: 'str') -> 'bool'` - Evaluate access for a subject and permission (default-deny).

### uro.security.ldap

LDAP schema and uPass hash chain (RFC 58).

#### class UpassKeys

PURPOSE: The six-step uPass derivation outputs (RFC 58.2).

Fields:

- step1: bytes
- step2: bytes
- step3: bytes
- step4: bytes
- step5: bytes
- step6: bytes

- `__init__(self, step1: 'bytes', step2: 'bytes', step3: 'bytes', step4: 'bytes', step5: 'bytes', step6: 'bytes') -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### upass_chain(upass: 'bytes') -> 'UpassKeys'

PURPOSE: RFC 58.2 alternating BLAKE3/SHA512 six-step chain.

#### class LDAPRecord

PURPOSE: LDAP schema fields per RFC 58.1.

Fields:

- username: str
- password: bytes
- encryption_key: bytes
- recovery_key: bytes
- public_cert: bytes
- private_key: bytes
- uuid: str
- active: bool

- `__init__(self, username: 'str', password: 'bytes', encryption_key: 'bytes' = b'', recovery_key: 'bytes' = b'', public_cert: 'bytes' = b'', private_key: 'bytes' = b'', uuid: 'str' = '', active: 'bool' = True) -> None` - Initialize self.  See help(type(self)) for accurate signature.

### uro.security.circle_security

Concentric ring access control (RFC 57).

#### class CircleEndUser

PURPOSE: Circle 32B entity with social lists (RFC 57.5).

Fields:

- entity: bytes
- friends: List[str]
- following: List[str]
- groups: List[str]
- acquaintance: List[str]
- blocked: List[str]

- `__init__(self, entity: 'bytes', friends: 'List[str]' = <factory>, following: 'List[str]' = <factory>, groups: 'List[str]' = <factory>, acquaintance: 'List[str]' = <factory>, blocked: 'List[str]' = <factory>) -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class CircleSecurity

PURPOSE: Five concentric rings of key protection (RFC 57).

- `__init__(self, key_512: 'bytes', owner_priv: 'bytes', admin_priv: 'bytes', access_priv: 'bytes') -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `store_digest(self) -> 'bytes'` - PURPOSE: Ring 1 Store: SHA512(512b key).

- `wrap_owner(self) -> 'bytes'` - PURPOSE: Ring 2 Owner: key encrypted under owner private material.

- `unwrap_owner(self, blob: 'bytes') -> 'bytes'` - PURPOSE: Reverse ring 2.

- `wrap_admin(self, req: 'int' = 1) -> 'bytes'` - PURPOSE: Ring 3 Admin: REQ=1 single wrap; REQ>1 matrix double wrap.

- `unwrap_admin(self, blob: 'bytes', req: 'int' = 1) -> 'bytes'` - PURPOSE: Reverse ring 3 for the given request depth.

- `wrap_access(self) -> 'bytes'` - PURPOSE: Ring 4 Access: PKI priv encrypted with AES256(512b key).

- `unwrap_access(self, blob: 'bytes') -> 'bytes'` - PURPOSE: Reverse ring 4.

- `end_user(self, user_priv: 'bytes') -> 'CircleEndUser'` - PURPOSE: Ring 5: AES256(SHA512(UserPriv), PKI(Priv)) 32B entity.

### uro.security.field_encryption

Field-level encryption and dynamic permission granting (RFC 60).

#### class EncryptedField

PURPOSE: Data plus two wrapped-key headers (RFC 60).

Fields:

- data: bytes
- header1: bytes
- header2: bytes

- `__init__(self, data: 'bytes', header1: 'bytes', header2: 'bytes') -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class FieldCipher

PURPOSE: Per-field 512b AES key with user and marketing wraps.

- `__init__(self, field_key: 'bytes', user_priv: 'bytes', marketing_pki: 'bytes') -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `encrypt_field(self, plaintext: 'bytes') -> 'EncryptedField'` - PURPOSE: AES256 data with the 512b key; wrap key for user and marketing.

- `decrypt_field(self, ef: 'EncryptedField', wrapped_key: 'bytes', key_material: 'bytes') -> 'bytes'` - PURPOSE: Unwrap the field key with holder material, then decrypt data.

- `grant_access(self, grantee_key: 'bytes') -> 'Dict[str, bytes]'` - PURPOSE: RFC 60.4 dynamic grant: Req -> PKI(what URO, random 512b -> id).

### uro.security.user_keys

User encryption and keying wraps (RFC 53).

#### class UserKeyring

PURPOSE: Wraps for private key and recovery per RFC 53.1.

Fields:

- core_key: bytes
- standard_wrap: bytes
- recovery_wrap: bytes
- user_pki_wrap: bytes

- `unlock(self, password: 'bytes') -> 'bytes'` - PURPOSE: Recover the private key via the standard wrap (RFC 53.1 step 4).

- `recovery_proof(self, inspa_enc: 'bytes') -> 'bytes'` - PURPOSE: Recover SHA512(password) via the recovery wrap (RFC 53.1 step 5).

- `__init__(self, core_key: 'bytes', standard_wrap: 'bytes', recovery_wrap: 'bytes', user_pki_wrap: 'bytes') -> None` - Initialize self.  See help(type(self)) for accurate signature.

### uro.security.custody

Custody send chain and 2-way exchange protocol (RFC 63).

#### send_custody(chain: 'List[Dict[str, Any]]', signer_key: 'bytes', obj_bytes: 'bytes') -> 'Dict[str, Any]'

PURPOSE: RFC 63.1: append trusted signature with hash; return trust receipt.

#### two_way_exchange(sender_key: 'bytes', receiver_key: 'bytes', snd_bytes: 'bytes', rcv_bytes: 'bytes') -> 'Dict[str, Any]'

PURPOSE: RFC 63.2: sender signs RCV, receiver signs SND.

#### verify_two_way(sender_key: 'bytes', receiver_key: 'bytes', snd_bytes: 'bytes', rcv_bytes: 'bytes', sigs: 'Dict[str, str]') -> 'bool'

PURPOSE: Recompute both cross-signatures to establish trusted exchange.

## memory

### uro.memory.engine

#### class MemoryTier

str(object='') -> str str(bytes_or_buffer[, encoding[, errors]]) -> str

#### class MemoryItem

MemoryItem(urid_pair: 'Dict[str, str]', payload: 'Any', confidence: 'float' = 1.0, tier: 'MemoryTier' = <MemoryTier.SHORT: 'F_RAM'>, created_at: 'float' = <factory>, last_accessed: 'float' = <factory>, use_count: 'int' = 0, attachment: 'float' = 0.0, saved_long: 'bool' = False)

Fields:

- urid_pair: Dict[str, str]
- payload: Any
- confidence: float
- tier: MemoryTier
- created_at: float
- last_accessed: float
- use_count: int
- attachment: float
- saved_long: bool

- `__init__(self, urid_pair: 'Dict[str, str]', payload: 'Any', confidence: 'float' = 1.0, tier: 'MemoryTier' = <MemoryTier.SHORT: 'F_RAM'>, created_at: 'float' = <factory>, last_accessed: 'float' = <factory>, use_count: 'int' = 0, attachment: 'float' = 0.0, saved_long: 'bool' = False) -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class MemoryEngine

URO S8 Memory Architecture. Manages tier transitions, cognitive decay, and consolidation.

- `__init__(self, decay_threshold: 'float' = 0.1, consolidation_threshold: 'int' = 5)` - Initialize self.  See help(type(self)) for accurate signature.

- `store(self, item: 'MemoryItem') -> 'None'`

- `retrieve(self, urid_pair: 'Dict[str, str]') -> 'Optional[MemoryItem]'`

- `decay_all(self) -> 'List[str]'` - S8.5: Apply cognitive decay to all items.

- `consolidate(self, epinephrine: 'float' = 0.0) -> 'int'` - S8.3 / S8.4: Move items from SHORT to LONG based on use_count and attachment.

- `connection_pass(self, item: 'MemoryItem', acl_permit: 'bool' = True, potentiator: 'float' = 0.5) -> 'str'` - PURPOSE: RFC 66 four-outcome per-pass decision from use counter, ACL, potentiators, last access.

- `apply_pass(self, item: 'MemoryItem', outcome: 'str') -> 'None'` - PURPOSE: Execute one RFC 66 outcome against the store.

- `introspect(self) -> 'Dict[str, int]'` - PURPOSE: RFC 65.2 clear work to short and short to long at introspection.

- `sleep_mode(self, authorized_inputs: 'Optional[List[str]]' = None, melatonin_rise: 'float' = 20.0) -> 'Dict[str, Any]'` - PURPOSE: RFC 68.1 reduced ACL set, pruning cycles, melatonin rise.

- `queue_morning_question(self, question: 'str') -> 'None'` - PURPOSE: RFC 68.2 queue morning questions comparing past and now.

- `drain_morning_questions(self) -> 'List[str]'` - PURPOSE: Return and clear the morning question queue.

- `downtime_reflection(self, failed_pathing_counts: 'Optional[Dict[str, int]]' = None, learn_threshold: 'int' = 3) -> 'Dict[str, List[str]]'` - PURPOSE: RFC 69 four reflection objectives over short-term connections.

- `cache_time(self, item: 'MemoryItem') -> 'float'` - PURPOSE: RFC 67.3 cache time for no-path objects equals search frequency.

- `get_tier_counts(self) -> 'Dict[str, int]'`

### uro.memory.decay

#### apply_cognitive_decay(original_conf: 'float', age_in_hours: 'float') -> 'float'

URO S8.5 Cognitive Decay (Confidence Depreciation). Beliefs in memory undergo exponential decay based on age:

#### hours_since(timestamp: 'float') -> 'float'

## pathing

### uro.pathing.beacons

#### class BeaconType

str(object='') -> str str(bytes_or_buffer[, encoding[, errors]]) -> str

#### class BeaconManager

URO S9.7 Beacons. Manages discovery and capability advertisement between UROs.

- `__init__(self)` - Initialize self.  See help(type(self)) for accurate signature.

- `broadcast(self, sender: 'str', beacon_type: 'BeaconType', payload: 'Dict[str, Any]' = None)`

- `get_beacons(self, beacon_type: 'BeaconType' = None) -> 'List[Dict[str, Any]]'`

### uro.pathing.connectors

#### class ConnectorType

str(object='') -> str str(bytes_or_buffer[, encoding[, errors]]) -> str

#### class Connector

URO S9.8 Connectors. Defines the directional relationship between UROs.

- `__init__(self, connector_type: 'ConnectorType', source: 'str', target: 'str' = None)` - Initialize self.  See help(type(self)) for accurate signature.

- `to_dict(self) -> 'Dict[str, Any]'`

### uro.pathing.onion

#### class OnionRouter

URO S9.4 Path Encryption (Onion Routing). Encrypts each layer so an object knows only itself and the next hop.

- `encrypt_path(self, hops: 'List[str]', payload: 'Dict[str, Any]') -> 'Dict[str, Any]'`

- `decrypt_layer(self, layer: 'Dict[str, Any]', current_hop: 'str') -> 'Dict[str, Any]'` - Decrypt the current layer and return its plaintext metadata.

### uro.pathing.trust

#### class TrustValueProtocol

URO S9.2 Trust Value Request Protocol. Evaluates responses from known UROs to determine path trust.

- `__init__(self, trust_threshold: 'float' = 75.0)` - Initialize self.  See help(type(self)) for accurate signature.

- `evaluate_responses(self, responses: 'List[Dict[str, Any]]') -> 'Dict[str, Any]'`

### uro.pathing.cro_matrix

CRO resolution matrix (RFC 72).

#### resolve_cro(urid1: 'bool', urid2: 'bool', urid3: 'bool', urid4: 'bool') -> 'str'

PURPOSE: Look up the RFC 72 significance for a CRO flag quadruple.

### uro.pathing.path_ops

Priority sums, path hash, and path combine operations (RFC 70/76/79).

#### combine_paths(p1: 'Tuple[str, str]', p2: 'Tuple[str, str]') -> 'Optional[Tuple[str, str]]'

PURPOSE: RFC 79: (U1,U2)+(U3,U1) -> (U3,U2); None on junction mismatch.

#### path_priority(priorities: 'List[int]') -> 'int'

PURPOSE: RFC 70.3: sum of all paths = priority.

#### fastest_first(priorities: 'List[int]') -> 'List[int]'

PURPOSE: RFC 70.3: 0 = fastest; order ascending.

#### path_hash(src: 'str', dest: 'str') -> 'str'

PURPOSE: RFC 76.4: SHA512(src, dest) for quick lookup before full routing.

### uro.pathing.stack_processing

Stack-based order of processing (RFC 77).

#### class ProcessingStack

PURPOSE: Stack semantics per RFC 77.1-77.3.

- `__init__(self) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `push(self, item: 'Any') -> 'None'` - PURPOSE: Add an item to the top of the stack.

- `add_result_item(self, item: 'Any') -> 'None'` - PURPOSE: RFC 77.3: a third item with new result goes to the bottom.

- `process_top(self, handler: 'Callable[[Any], Any]') -> 'Any'` - PURPOSE: RFC 77.1: process when the object can get to top of stack.

- `pop_as_far_as(self, can_reach: 'Callable[[Any], bool]') -> 'List[Any]'` - PURPOSE: RFC 77.2: pop from top while reachable; return popped for forwarding.

### uro.pathing.swarms

Swarm object and routing tuple semantics (RFC 81).

#### class SwarmObject

PURPOSE: Swarm comprises communications, potentiators, associations (RFC 81.1).

- `__init__(self) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

#### classify_routing(urid1: 'str', urid2: 'str') -> 'str'

PURPOSE: RFC 81.2 routing tuple semantics.

## relations

### uro.relations.association

Association UROs - first-class relationships between UROs.

#### class ConnectionType

The canonical relationship types between two UROs.

#### class Association

A relationship URO connecting URO a to URO b.

- `__init__(self, a: 'URO', b: 'URO', connection_type: 'ConnectionType' = <ConnectionType.LINK: 3>) -> 'None'` - Create an association between two UROs.

- `use(self) -> 'None'` - Mark the association as used, strengthening the bond.

- `decay(self, seconds: 'float') -> 'None'` - Apply natural bond decay over time.

- `reward(self, amount: 'float' = 0.1) -> 'None'` - Increase trust as a reward.

- `punish(self, amount: 'float' = 0.1) -> 'None'` - Decrease trust as punishment.

- `is_active(self) -> 'bool'` - Return True if the bond is still above zero.

### uro.relations.pathing

Path UROs and path resolution.

#### class PathURO

A URO representing an ordered route between UROs.

- `__init__(self, hops: 'Optional[List[URO]]' = None, priority: 'int' = 0, cost: 'float' = 0.0) -> 'None'` - Create a Path URO.

- `add_hop(self, uro: 'URO') -> "'PathURO'"` - Append a hop to the path.

#### resolve_path(source: 'URO', destination: 'URO', max_depth: 'int' = 16) -> 'Optional[PathURO]'

Resolve a path from source to destination via associations (BFS).

## interchange

### uro.aupi

AUPI - automated translation between available and required UPIs.

#### typed_uro(type_name: 'str', value: 'Any') -> 'URO'

Create a URO carrying a typed value. Typed UROs use a payload of {"type": str, "value": Any} so the AUPI

#### class Translator

A URO that converts one UPI type into another. Attributes:

- `__init__(self, source_type: 'str', target_type: 'str', func: 'Callable[[Any], Any]') -> 'None'` - Create a translator URO.

- `apply(self, value: 'Any') -> 'Any'` - Apply the conversion to a value.

#### class AUPI

The automated translation layer. AUPI maintains a directed graph of translators keyed by source type

- `__init__(self) -> 'None'` - Create an empty AUPI translation layer.

- `register(self, source_type: 'str', target_type: 'str', func: 'Callable[[Any], Any]') -> 'Translator'` - Register a translator between two types.

- `find_path(self, source_type: 'str', target_type: 'str') -> 'List[Translator]'` - Find a chain of translators from source to target (BFS).

- `translate_value(self, value: 'Any', source_type: 'str', target_type: 'str') -> 'Any'` - Translate a raw value between types.

- `translate(self, source_uro: 'URO', target_type: 'str') -> 'URO'` - Translate a typed URO into a new typed URO of target_type.

- `resolve_container(self, source_uro: 'URO', target_type: 'str') -> 'URO'` - PURPOSE: RFC 88 container resolution with cached localized wrapper paths.

### uro.interchange

Serialization/deserialization of UROs and the URO header.

#### build_header(src_len: 'int', dst_len: 'int', payload_len: 'int', future: 'int' = 0) -> 'bytes'

PURPOSE: Delegate to the canonical RFC 7 header builder (single source).

#### parse_header(header: 'bytes') -> 'Tuple[int, int, int, int]'

PURPOSE: Delegate verification to the canonical RFC 7 header parser.

#### encode_uro(uro: 'URO') -> 'bytes'

Serialize a URO to a canonical binary form.

#### decode_uro(data: 'bytes') -> 'URO'

Deserialize a URO from encode_uro output.

#### uro_to_json(uro: 'URO') -> 'str'

Serialize a URO to a JSON string.

#### uro_from_json(text: 'str') -> 'URO'

Deserialize a URO from uro_to_json output.

### uro.hot_swap

Hot-swap process preserving identity (RFC 85).

#### class HotSwapRecord

PURPOSE: Typed result of one hot-swap operation (RFC 85).

- `__init__(self, urid1, old_urid2, new_urid2, carried: 'List[Any]') -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

#### hot_swap(old: 'URO', new_code_factory: 'Callable[[], URO]', verify: 'Callable[[URO], bool]' = None) -> 'HotSwapRecord'

PURPOSE: Generate+verify, compile+test, identify old, swap preserving URID1.

### uro.self_loading

Object self-loading of scripted configuration and parent code (RFC 86).

#### class SelfLoader

PURPOSE: Pull config, assure parent code, optional local compile (RFC 86).

- `__init__(self) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `pull_config(self, config: 'Dict[str, Any]') -> 'Dict[str, Any]'` - PURPOSE: Pull scripted object configuration (RFC 86 step 1).

- `ensure_parent_code(self, parent_id: 'str', code: 'Any') -> 'Any'` - PURPOSE: Ensure script/object code for parents is present (RFC 86).

- `compile_local(self, parent_id: 'str') -> 'bool'` - PURPOSE: During reflection, compile and hold code locally (RFC 86).

### uro.priority

Priority processing: retention and queue precedence (RFC 87).

#### class PriorityQueue

PURPOSE: Queue precedence crit > high > normal > low (RFC 87).

- `__init__(self) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `push(self, level: 'str', item: 'Any') -> 'None'` - PURPOSE: Enqueue an item at its priority level.

- `pop(self) -> 'Any'` - PURPOSE: Dequeue by precedence order.

- `retention(self, level: 'str') -> 'float'` - PURPOSE: How long unprocessed data is stored per level (RFC 87).

## learning

### uro.learning.primitives

Learning primitives (RFC 90).

#### class CauseEffectLedger

PURPOSE: Record and query cause-effect relations (RFC 90.1).

- `__init__(self) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `record(self, cause: 'Any', effect: 'Any', weight: 'float' = 1.0) -> 'None'` - PURPOSE: Add one cause-effect observation.

- `effects_of(self, cause: 'Any') -> 'Dict[Any, float]'` - PURPOSE: Ranked effects observed for a cause.

- `causes_of(self, effect: 'Any') -> 'Dict[Any, float]'` - PURPOSE: Ranked causes observed for an effect.

#### class ExperimentLog

PURPOSE: Try action UROs on other UROs when not busy (RFC 90.2).

- `__init__(self) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `schedule(self, action: 'Any', target: 'Any', busy: 'bool')` - PURPOSE: Queue an experiment only when the object is not busy.

- `record_result(self, trial_id: 'int', result: 'Any') -> 'None'` - PURPOSE: Map the outcome of one experiment (RFC 90.2).

#### class FeedbackLoop

PURPOSE: Proportional feedback adjustment toward a target (RFC 90.3).

- `__init__(self, gain: 'float' = 0.5) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `step(self, current: 'float', target: 'float') -> 'float'` - PURPOSE: Return the adjustment moving current toward target.

#### class ObservationRecord

PURPOSE: Timestamped snapshot of what the object is seeing (RFC 90.4).

Fields:

- stream: str
- payload: Any
- t: float

- `__init__(self, stream: 'str', payload: 'Any', t: 'float' = <factory>) -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class SequenceTracker

PURPOSE: Track X-followed-by-Y ordering and predict successors (RFC 90.5).

- `__init__(self) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `observe(self, event: 'Any') -> 'None'` - PURPOSE: Append one event to the sequence history.

- `predict_next(self, event: 'Any') -> 'Any'` - PURPOSE: Most frequent successor of event.

#### segment_by_gaps(series: 'List[float]', threshold: 'float') -> 'List[List[float]]'

PURPOSE: RFC 90.6: gaps segment data into patterns.

#### correlate_gaps(segs_a, segs_b, tolerance: 'int' = 1) -> 'int'

PURPOSE: RFC 90.6: correlate gap boundaries across two streams.

#### differentiate(payload: 'Dict[str, Any]') -> 'List[Dict[str, Any]]'

PURPOSE: RFC 90.7: break a URO payload into components (make smaller).

#### correlate(components: 'List[Dict[str, Any]]') -> 'Dict[str, Any]'

PURPOSE: RFC 90.8: group components into a larger system (make bigger).

### uro.learning.dicho

Dicho (idiom) processing against core URO ideas (RFC 91.1).

#### class DichoRegistry

PURPOSE: Map dichos across languages to a shared core URO idea.

- `__init__(self) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `register(self, phrase: 'str', core_idea: 'str') -> 'None'` - PURPOSE: Bind a phrase to its core URO idea.

- `resolve(self, phrase: 'str') -> 'Optional[str]'` - PURPOSE: Commonality-first lookup of the core idea (RFC 91.1).

- `commonalities(self, phrase_a: 'str', phrase_b: 'str') -> 'Optional[str]'` - PURPOSE: Shared core idea between two dichos, else None.

- `structure_fallback(self, phrase_a: 'str', phrase_b: 'str') -> 'List[str]'` - PURPOSE: Sentence-structure comparison when no shared core exists.

### uro.learning.action_uro

Action URO types and cumulative costing (RFC 92).

#### class ActionType

PURPOSE: RFC 92.1 action composition types.

#### class ActionCost

PURPOSE: Cost triple for one action piece (RFC 92.2).

Fields:

- time: float
- price: float
- reliability: float

- `__init__(self, time: 'float' = 0.0, price: 'float' = 0.0, reliability: 'float' = 1.0) -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class ActionURO

PURPOSE: Composable action with cumulative cost roll-up (RFC 92).

Fields:

- kind: ActionType
- parts: List['ActionURO']
- cost: ActionCost

- `total_cost(self) -> 'ActionCost'` - PURPOSE: Roll up time/price/reliability from self to final product.

- `__init__(self, kind: 'ActionType', parts: "List['ActionURO']" = <factory>, cost: 'ActionCost' = <factory>) -> None` - Initialize self.  See help(type(self)) for accurate signature.

### uro.learning.attention

Attention and daydream input-stream overrides (RFC 93).

#### class AttentionManager

PURPOSE: Stream prioritization with forced overrides and daydream.

- `__init__(self, streams: 'List[str]') -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `prioritize(self, stream: 'str', delta: 'float' = 1.0) -> 'None'` - PURPOSE: Raise a stream priority (RFC 93 override).

- `deprioritize(self, stream: 'str', delta: 'float' = 1.0) -> 'None'` - PURPOSE: Lower a stream priority (RFC 93 override).

- `override(self, stream: 'str') -> 'None'` - PURPOSE: Force a stream to the top regardless of priority.

- `clear_override(self) -> 'None'` - PURPOSE: Remove the forced stream override.

- `active_order(self) -> 'List[str]'` - PURPOSE: Effective stream order honoring override then priority.

- `daydream(self, enabled: 'bool' = True) -> 'bool'` - PURPOSE: Daydream routes attention to the internal stream (RFC 93).

### uro.learning.aloneness

Aloneness as propagator for action (RFC 98).

#### class AlonenessPropagator

PURPOSE: Little input propagates seeking of capabilities (RFC 98).

- `__init__(self, input_threshold: 'int' = 1) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `observe_input(self, count: 'int' = 1) -> 'None'` - PURPOSE: Count incoming stimuli this window.

- `reset_window(self) -> 'None'` - PURPOSE: Begin a new observation window.

- `should_seek(self) -> 'bool'` - PURPOSE: True when input falls below the aloneness threshold.

- `seek_action(self, mode: 'str' = 'self_improvement') -> 'Dict[str, Any]'` - PURPOSE: Emit the propagator action object (RFC 98).

### uro.learning.cas_loop

VTA-CAS context-association-reward loop (RFC 33, 100).

#### class CASLoop

PURPOSE: Link contexts to rewards enabling predictive behavior.

- `__init__(self) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `associate(self, context: 'str', reward: 'float') -> 'None'` - PURPOSE: Record one context-reward pairing (VTA reward circuit).

- `predict(self, context: 'str') -> 'float'` - PURPOSE: Expected reward for a context (mean of associations).

- `prediction_error(self, context: 'str', actual: 'float') -> 'float'` - PURPOSE: VTA reward-prediction-error for novel/unexpected rewards.

## opar

### uro.opar.stages

Stage envelope types (RFC 12).

#### class StageResult

PURPOSE: Typed envelope exchanged between OPAR stages (RFC 12).

Fields:

- stage: str
- status: str
- data: Dict[str, Any]
- nte: Dict[str, float]
- latency_ms: float
- error: Optional[str]
- provenance: List[Dict[str, Any]]

- `__init__(self, stage: 'str', status: 'str' = 'FULFILLED', data: 'Dict[str, Any]' = <factory>, nte: 'Dict[str, float]' = <factory>, latency_ms: 'float' = 0.0, error: 'Optional[str]' = None, provenance: 'List[Dict[str, Any]]' = <factory>) -> None` - Initialize self.  See help(type(self)) for accurate signature.

### uro.opar.protocol

OPARCapability protocol (RFC 13).

#### class OPARCapability

PURPOSE: Interface every capability MUST satisfy (RFC 13).

- `observe(self, stimulus: 'Any', nte: 'Dict[str, float]') -> 'StageResult'`

- `plan(self, observation: 'StageResult', nte: 'Dict[str, float]') -> 'StageResult'`

- `act(self, plan: 'StageResult', nte: 'Dict[str, float]') -> 'StageResult'`

- `review(self, observation: 'StageResult', plan: 'StageResult', action: 'StageResult', nte: 'Dict[str, float]') -> 'StageResult'`

- `execute(self, stimulus: 'Any', nte: 'Optional[Dict[str, float]]' = None) -> 'Dict[str, Any]'`

- `__init__(self, *args, **kwargs)`

### uro.opar.base

Canonical OPAR-24 capability base class (RFC 10-15).

#### nte24(state: 'Optional[Dict[str, float]]') -> 'Dict[str, float]'

PURPOSE: Full 24-axis state from partial input; axes canonical (ADR-011).

#### class OPARBase

PURPOSE: Canonical OPAR capability; subclass and implement four stages.

- `__init__(self, bus=None, **kwargs) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `observe(self, stimulus: 'Any', nte: 'Dict[str, float]') -> 'StageResult'` - PURPOSE: Stage 1; subclasses override.

- `plan(self, observation: 'StageResult', nte: 'Dict[str, float]') -> 'StageResult'` - PURPOSE: Stage 2; subclasses override.

- `act(self, plan: 'StageResult', nte: 'Dict[str, float]') -> 'StageResult'` - PURPOSE: Stage 3; subclasses override.

- `review(self, observation: 'StageResult', plan: 'StageResult', action: 'StageResult', nte: 'Dict[str, float]') -> 'StageResult'` - PURPOSE: Stage 4; subclasses override.

- `execute(self, stimulus: 'Any', nte: 'Optional[Dict[str, float]]' = None) -> 'Dict[str, Any]'` - PURPOSE: Canonical driver and smart-loader entry point (RFC 13/14).

### uro.opar.grounding

Grounded emission gate engines (RFC 15, ADR-022).

#### class GroundingResult

PURPOSE: Typed grounding verdict for one artifact (RFC 15).

Fields:

- verified_count: int
- refuted_count: int
- unverifiable_count: int
- overall_grounding: float
- emit_with_flags: bool

- `__init__(self, verified_count: 'int' = 0, refuted_count: 'int' = 0, unverifiable_count: 'int' = 0, overall_grounding: 'float' = 1.0, emit_with_flags: 'bool' = False) -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class LocalGroundingEngine

PURPOSE: Open-library claim grounding heuristic (ADR-022 fallback).

- `ground_artifact(self, artifact: 'Dict[str, Any]') -> 'GroundingResult'` - PURPOSE: Count verified/refuted/unverifiable claims in an artifact.

#### get_grounding_engine()

PURPOSE: Resolve dock cap_37 engine first, else local heuristic (ADR-022).

### uro.opar.compliance

OPAR compliance checklist and conformance harness (RFC 16/17).

#### checklist(cap) -> 'Dict[str, bool]'

PURPOSE: RFC 16 seven-item compliance checklist as booleans.

#### source_has_no_op_stub(path) -> 'bool'

PURPOSE: RFC 17 point 5: detect a no-op class OPAR stub in a source file.

#### run_conformance(cap, valid: 'Any', fail_act: 'Any', false_claim: 'Any') -> 'Dict[str, bool]'

PURPOSE: RFC 17 five-point conformance test, measured per capability.

## quad

### uro.quad.quad_capability

Quad-Capability four-dimension evaluation (RFC 45).

#### class QuadDimension

PURPOSE: The four evaluation dimensions (RFC 45).

#### class QuadCapabilityRecord

PURPOSE: Scores across the four evaluation dimensions (RFC 45).

Fields:

- capability_id: str
- base: float
- gap_remediation: float
- best_practice: float
- world_first: float
- notes: List[str]

- `composite(self) -> 'float'` - PURPOSE: Mean of the four dimension scores.

- `remediation_required(self) -> 'bool'` - PURPOSE: Gap dimension below threshold flags self-correction work.

- `__init__(self, capability_id: 'str', base: 'float' = 0.0, gap_remediation: 'float' = 0.0, best_practice: 'float' = 0.0, world_first: 'float' = 0.0, notes: 'List[str]' = <factory>) -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### innovation_affinity(levels: 'Dict') -> 'float'

PURPOSE: RFC 45.4 world-first affinity from creativity and analogical_transfer.

### uro.quad.character_condition

Character vs Condition equilibrium math (RFC 46).

#### class CharacterCondition

PURPOSE: Near-fixed character equilibrium plus immediate condition (RFC 46).

Fields:

- character: Dict[str, float]
- condition: Dict[str, float]

- `set_condition(self, trait: 'str', value: 'float') -> 'None'` - PURPOSE: Record the immediate state of one trait.

- `deviation_sd(self, trait: 'str') -> 'float'` - PURPOSE: Condition deviation from character in SD units.

- `apply_period(self, trait: 'str', sustained_periods: 'int' = 1, drift_rate: 'float' = 0.01) -> 'float'` - PURPOSE: RFC 46.1/46.2 drift rule; bounded, monotonic toward condition.

- `equilibrium(self) -> 'Dict[str, float]'` - PURPOSE: The near-fixed character levels the object returns to.

- `__init__(self, character: 'Dict[str, float]' = <factory>, condition: 'Dict[str, float]' = <factory>) -> None` - Initialize self.  See help(type(self)) for accurate signature.

### uro.quad.croate

CROATE personality model and NTE mappings (RFC 47).

#### class CROATE

PURPOSE: The six personality traits (RFC 47).

#### trait_from_nte(levels: 'Dict') -> 'Dict[CROATE, float]'

PURPOSE: Derive six trait scores as means of mapped NTE axes (RFC 47).

## boot

### uro.boot.boot_sequence

The 16-step full boot sequence (RFC 107).

#### class BootContext

PURPOSE: Mutable artifacts and flags shared across boot steps.

Fields:

- artifacts: Dict[str, Any]
- flags: Dict[str, bool]

- `__init__(self, artifacts: 'Dict[str, Any]' = <factory>, flags: 'Dict[str, bool]' = <factory>) -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class BootRunner

PURPOSE: Execute the 16 steps in order; halt on first False handler.

- `__init__(self, handlers: 'Dict[str, Callable[[BootContext], bool]]' = None) -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `run(self) -> 'Dict[str, Any]'` - PURPOSE: Run all steps; READY on completion, HALTED on first failure.

### uro.boot.child_boot

Child boot with response queues and parent ACK (RFC 108).

#### class ChildBoot

PURPOSE: Model a child URO booting under a parent seal.

- `__init__(self, parent_seal: 'str', child: 'Any') -> 'None'` - Initialize self.  See help(type(self)) for accurate signature.

- `queue_response(self, response: 'Any') -> 'None'` - PURPOSE: Child queues responses until the parent ACKs.

- `drain_on_ack(self, ack: 'bool') -> 'List[Any]'` - PURPOSE: Release the queue only on parent ACK (RFC 108).

- `verify_child(self) -> 'bool'` - PURPOSE: Verify the child seal recomputes to its stored INAHASH.

- `boot(self, ack: 'bool' = True) -> 'Dict[str, Any]'` - PURPOSE: Child boot result: verification plus released responses.

### uro.boot.self_check

Four-step self-check with quarantine semantics (RFC 109).

#### self_check(obj: 'Any') -> 'Dict[str, Any]'

PURPOSE: Run the four checks; quarantine when any fails (RFC 109).

## economy

### uro.economy.goods

MODULE: Economic Goods (everything sellable is a URO) INTENT: Wrap swarm assets as sellable UROs with lineage, custody, and trust.

#### class GoodType

#### class EconomicGoodURO

A sellable asset, itself a URO with lineage and integrity.

Fields:

- urid1: <class 'uro.core.urid.URID'>
- urid2: <class 'uro.core.urid.URID'>
- good_type: <class 'str'>
- title: <class 'str'>
- description: <class 'str'>
- quadrant: <class 'str'>
- asset: typing.Dict[str, typing.Any]
- creator: <class 'str'>
- source_urids: typing.List[str]
- listed: <class 'bool'>
- price: <class 'float'>
- royalty_rate: <class 'float'>
- inahash: <class 'str'>

- `seal(self)`

#### class CapabilityGapURO

An unmet capability need with a bounty (the demand side).

Fields:

- urid1: <class 'uro.core.urid.URID'>
- urid2: <class 'uro.core.urid.URID'>
- gap_description: <class 'str'>
- quadrant: <class 'str'>
- bounty: <class 'float'>
- requester: <class 'str'>
- filled_by: str | None
- filled: <class 'bool'>
- inahash: <class 'str'>

- `seal(self)`

### uro.economy.ledger

MODULE: FinOps Ledger (micropayments + royalties) INTENT: Record every transaction and per-use royalty immutably.

#### class Ledger

- `__init__(self)` - Initialize self.  See help(type(self)) for accurate signature.

- `credit(self, account: 'str', amount: 'float')`

- `debit(self, account: 'str', amount: 'float') -> 'bool'`

- `record_purchase(self, buyer, seller, good_urid, amount)`

- `record_royalty(self, payer, creator, good_urid, amount)`

- `balance(self, account: 'str') -> 'float'`

### uro.economy.pricing

MODULE: Value-Based Pricing INTENT: Price economic goods from trust, myelination, usage, and quadrant.

#### price_good(good, trust: 'float' = 50.0, myelination: 'int' = 0, usage: 'int' = 0) -> 'float'

Compute a value-based price for a good. price = quadrant_base

### uro.economy.marketplace

MODULE: Marketplace INTENT: List/discover/purchase/reuse economic goods; pay royalties; post and

#### class Marketplace

- `__init__(self, ledger=None)` - Initialize self.  See help(type(self)) for accurate signature.

- `list_good(self, good, trust=50.0, myelination=0, usage=0)`

- `discover(self, good_type=None, quadrant=None, min_price=0.0)`

- `purchase(self, buyer: 'str', good_urid: 'str') -> 'Dict[str, Any]'`

- `reuse(self, user: 'str', good_urid: 'str') -> 'Dict[str, Any]'`

- `post_gap(self, gap: 'CapabilityGapURO')`

- `fill_gap(self, gap_urid: 'str', filler: 'str') -> 'Dict[str, Any]'`

### uro.economy.currency

Currency definitions and conversions (RFC 110).

#### class Currency

PURPOSE: The two canonical currencies (RFC 110).

#### convert(value: 'float', from_currency: 'Currency', to_currency: 'Currency') -> 'Decimal'

PURPOSE: Convert between InSPativo and InSPaneda with decimal precision.

### uro.economy.token_transfer

Atomic token transfers with network tax (RFC 110, 27.1).

#### transfer_tokens(from_account: 'str', to_account: 'str', amount: 'float', ledger=None) -> 'Dict[str, any]'

PURPOSE: Atomic transfer with 10% tax burned; insufficient funds returns error.

### uro.economy.social_pricing

Social pricing with trust weighting (RFC 111).

#### social_price(base_price: 'float', trust: 'float', reputation: 'float' = 50.0) -> 'float'

PURPOSE: Apply trust and reputation discounts to base price.

### uro.economy.supply_chain

Supply chain cost tracking (RFC 112).

#### class SupplyChainStage

PURPOSE: One production stage with cost and value-add.

Fields:

- stage_id: str
- cost: float
- value_add: float
- notes: str

- `__init__(self, stage_id: 'str', cost: 'float', value_add: 'float' = 0.0, notes: 'str' = '') -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class SupplyChainLedger

PURPOSE: Track cumulative cost through production stages.

Fields:

- stages: List[SupplyChainStage]

- `add_stage(self, stage: 'SupplyChainStage') -> 'None'` - PURPOSE: Append a production stage.

- `total_cost(self) -> 'float'` - PURPOSE: Sum of all stage costs.

- `total_value_add(self) -> 'float'` - PURPOSE: Sum of all value-add components.

- `final_price(self, margin: 'float' = 0.2) -> 'float'` - PURPOSE: Cost plus margin.

- `__init__(self, stages: 'List[SupplyChainStage]' = <factory>) -> None` - Initialize self.  See help(type(self)) for accurate signature.

## cognition

### uro.cognition.fuzzy

MODULE: Fuzzy Primitives INTENT: Membership functions and fuzzy aggregation for the neuro-fuzzy matrix.

#### trimf(x: 'float', a: 'float', b: 'float', c: 'float') -> 'float'

Triangular membership (LOW/MED/HIGH style linguistic terms).

#### gauss_close(x: 'float', prototype: 'float', sigma: 'float' = 25.0) -> 'float'

Fuzzy 'closeness' of a crisp value to a prototype (Gaussian).

#### linguistic(x: 'float') -> 'Dict[str, float]'

Map a crisp 0-100 value to LOW/MED/HIGH membership degrees.

#### fuzzy_and(degrees: 'List[float]') -> 'float'

Fuzzy AND across a set of membership degrees (geometric mean).

#### normalize(weights: 'Dict[str, float]') -> 'Dict[str, float]'

Normalize a weight dict into a probability distribution.

### uro.cognition.verdict

MODULE: Verdict Dynamics INTENT: Holds a verdict DISTRIBUTION over time (not a locked decision) plus

#### class VerdictDynamics

A verdict held as a living distribution with dynamics.

Fields:

- urid1: <class 'uro.core.urid.URID'>
- urid2: <class 'uro.core.urid.URID'>
- current: typing.Dict[str, float]
- history: typing.List[typing.Dict[str, float]]
- inahash: <class 'str'>

- `update(self, dist: 'Dict[str, float]') -> 'None'` - Record a new distribution snapshot.

- `entropy(self, dist: 'Optional[Dict[str, float]]' = None) -> 'float'`

- `delta_p(self) -> 'float'` - Total-variation distance between the last two snapshots (dP/dt).

- `entropy_rate(self) -> 'float'`

- `meta_verdict(self) -> 'str'` - Classify the current belief state.

- `should_reevaluate(self, orthogonal_evidence: 'bool' = False) -> 'bool'` - Trigger deeper re-examination when the belief state demands it.

- `top(self) -> 'Optional[str]'`

- `seal(self) -> 'None'`

### uro.cognition.matrix

MODULE: Fuzzy Matrix URO (the decision brain) INTENT: A URO that maps parallel input rates to a distribution over outcomes

#### class FuzzyMatrixURO

A fuzzy decision matrix, itself a first-class URO.

Fields:

- urid1: <class 'uro.core.urid.URID'>
- urid2: <class 'uro.core.urid.URID'>
- prototypes: typing.Dict[str, typing.Dict[str, float]]
- sigma: <class 'float'>
- verdict: <class 'uro.cognition.verdict.VerdictDynamics'>
- inahash: <class 'str'>

- `evaluate(self, inputs: 'Dict[str, float]', agg: 'str' = 'geometric', strict_outcomes=None) -> 'Dict[str, float]'` - Map parallel input rates to a distribution over outcomes.

- `seal(self) -> 'None'`

### uro.cognition.cognitive_fuzzy

MODULE: Cognitive Fuzzy Layer INTENT: Maps context rates to a distribution over cognitive strategies, with

#### new_cognitive_matrix() -> 'FuzzyMatrixURO'

#### cognitive_inputs(source_trust: 'float', coherence: 'float', novelty: 'float', nte) -> 'Dict[str, float]'

Build the parallel input-rate vector, folding NTE modulation in.

#### decide_strategy(matrix: 'FuzzyMatrixURO', inputs: 'Dict[str, float]') -> 'Tuple[str, Dict[str, float], bool]'

Return (strategy, distribution, should_reevaluate).

### uro.cognition.memory_fuzzy

MODULE: Memory Fuzzy Layer (homeostatic memory) INTENT: Fuzzy retrieval scoring + homeostatic lifecycle decisions

#### new_memory_matrix() -> 'FuzzyMatrixURO'

#### new_lifecycle_matrix() -> 'FuzzyMatrixURO'

#### cosine_similarity(v1: 'List[float]', v2: 'List[float]') -> 'float'

#### should_promote_fuzzy(entry, nte, tier_load: 'float' = 0.5) -> 'Tuple[bool, str]'

Fuzzy replacement for hardcoded should_promote().

#### should_decay_fuzzy(entry, nte, tier_load: 'float' = 0.5) -> 'Tuple[bool, str]'

Fuzzy replacement for hardcoded should_decay().

#### memory_inputs(similarity, recency, frequency, salience, source_trust, consolidation, nte) -> 'Dict[str, float]'

#### memory_decision(matrix, inputs) -> 'Tuple[str, Dict[str, float], float]'

#### rank_memories_for_retrieval(entries, query_embedding=None, trust_map=None, nte=None) -> 'List[Tuple[Any, float]]'

Rank entries by fuzzy retrieval strength (trust-weighted).

### uro.cognition.myelination

MODULE: Myelination & Homeostatic Scaling INTENT: Detect hot synapses, myelinate them, and scale infrastructure by NTE.

#### class MyelinationLevel

#### class SynapseUsageStats

SynapseUsageStats(synapse_id: 'str', use_count: 'int', last_used: 'float', success_count: 'int', failure_count: 'int', myelination_level: 'int' = 0, total_latency_ms: 'float' = 0.0)

Fields:

- synapse_id: str
- use_count: int
- last_used: float
- success_count: int
- failure_count: int
- myelination_level: int
- total_latency_ms: float

- `__init__(self, synapse_id: 'str', use_count: 'int', last_used: 'float', success_count: 'int', failure_count: 'int', myelination_level: 'int' = 0, total_latency_ms: 'float' = 0.0) -> None` - Initialize self.  See help(type(self)) for accurate signature.

#### class SynapseUsageTracker

- `__init__(self)` - Initialize self.  See help(type(self)) for accurate signature.

- `record_use(self, synapse_id: 'str', success: 'bool', latency_ms: 'float' = 0.0)`

- `get_stats(self, synapse_id: 'str')`

- `get_hot_synapses(self, min_uses=10, min_success_rate=0.8)`

#### detect_hot_synapses(tracker, min_uses=10, min_success_rate=0.8)

#### myelinate_synapse(synapse_id, level, registry)

Mark a synapse for optimization (registry side-table is source of truth).

#### homeostatic_scale_decision(nte)

#### record_synapse_use(synapse_hex, success, latency_ms=0.0)

#### run_myelination_pass(registry, tracker=None, min_uses=10, min_success_rate=0.8)

### uro.cognition.core

MODULE: Cognitive Core (the cumulative learner) INTENT: The LEAST stateless object in the swarm. Tracks every request, every

#### class CognitiveCore

Stateful, cumulative cognitive learner.

- `__init__(self, dock_name: 'str' = 'cognitive', k: 'float' = 5.0)` - Initialize self.  See help(type(self)) for accurate signature.

- `observe(self, inputs: 'Dict[str, float]', explore: 'bool' = True) -> 'Tuple[str, str, Dict[str, float], float]'`

- `record_outcome(self, rid: 'str', reward: 'float') -> 'None'`

- `recall_similar(self, inputs: 'Dict[str, float]', topn: 'int' = 3) -> 'List[Dict]'`

- `snapshot(self) -> 'Dict[str, Any]'`

- `intelligence(self) -> 'float'` - How much learned experience currently dominates the prior (w_p).

### uro.cognition.persistence

MODULE: Cognitive Persistence (Robust) INTENT: Saves/restores CognitiveCore state via memory dock's HTTP API

#### class CognitivePersistence

Saves/restores CognitiveCore to/from memory dock via HTTP.

- `__init__(self, dock_name: 'str' = 'cognitive')` - Initialize self.  See help(type(self)) for accurate signature.

- `save(self, core: 'CognitiveCore') -> 'bool'` - Save CognitiveCore snapshot to memory dock.

- `restore(self, core: 'CognitiveCore') -> 'bool'` - Restore CognitiveCore from memory dock.

- `close(self)`

## Generation Summary

modules: 87 | classes: 120 | functions: 114 | import failures: 0
