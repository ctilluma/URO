# PHOENIX REMEDIATION PLAN (Addressing Pass 1 S13.2/S13.5 Gaps)

## Critical Gap 1: S13.5 `/phoenix/restore` Endpoint MISSING
**Status:** Pass 1 found 0 references to `/phoenix/restore` in `routes.py` or `api.py`.
**Impact:** The Aegis critical-quarantine chain (S7.11 step 3) cannot complete.
**Plan (S14.5 Exact-Block Replacement):**
1. Add `POST /phoenix/restore` to `routes.py` accepting `{dock_name, reason}`.
2. Wire it to `engine.py` or `phoenix_master.py` to execute the "Phoenix Restoration" logic:
   - Wipe the compromised state volume (via Host Controller).
   - Rebuild the dock from a known-good image (via Host Controller).
3. Update `main.py` to ensure the router is mounted.

## Critical Gap 2: S4.3 NTE Normalizer (0 call sites, 20 direct mutations)
**Status:** 20 files mutate `nte_state.levels` directly, violating S14.7.
**Plan:**
1. Find all 20 `.levels[...]` mutation sites.
2. Wrap each in `# === START: nte_normalize ===` / `# === END: nte_normalize ===`.
3. Replace with `engine.modulate_synapse(synapse, delta)` or `normalize_nte_state()`.

## Critical Gap 3: S13.2 Missing Mandates (ACL, Time URO)
**Status:** 0 files enforce ACL (S7.9), 0 files use Time URO (S10.5).
**Plan:**
1. **ACL:** Inject `from uro.security.acl import check_acl` into `routes.py` middleware or decorator for all `/phoenix/*` endpoints.
2. **Time URO:** Replace `time.time()` calls in `phoenix_master.py` and `engine.py` with `create_time_uro()`.

## Critical Gap 4: Package Hygiene (`__init__.py` missing)
**Status:** `capabilities/`, `domains/`, `docks/` are not importable packages.
**Plan:**
1. Add empty `__init__.py` to `capabilities/`, `domains/`, and `docks/`.
2. Add `__all__ = []` to prevent wildcard import pollution.

## Critical Gap 5: Quad-Capability Dimensions (0 GAP/BEST_PRACTICE/WORLD_FIRST)
**Status:** Only "CORE" is implemented in the 24 capabilities.
**Plan:**
1. For each `cap_*.py`, append 3 new classes/methods bounded by markers:
   - `class GapRemediation:...`
   - `class BestPractice:...`
   - `class WorldFirst:...`
2. This fulfills S5.2 ("Every capability in every dock is evaluated across all four dimensions").

## Execution Order (S14.6 Rollout Gates)
1. **Pass 3 (ACT):** Fix S13.5 `/phoenix/restore` (Critical for Aegis).
2. **Pass 4 (ACT):** Fix S4.3 NTE normalizer mutations.
3. **Pass 5 (ACT):** Add `__init__.py` + ACL middleware + Time URO.
4. **Pass 6 (REVIEW):** Run `pytest` in `docks/phoenix/` + core `synapse_suite.py`.
5. **Pass 7 (ROLLOUT):** `./ops/rollout_profile.sh dev -> staging -> uat -> prod`.
