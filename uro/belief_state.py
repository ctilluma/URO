# V.A.U.R.O.S. Core Library - URO (Universal Resource Orchestrator)
# Copyright (C) 2026 V.A.U.R.O.S. Swarm Collective
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""V.A.U.R.O.S. Belief State Ledger (Phase 3b.1).

Stateful, evolving beta-posterior beliefs. Composes the pure functions in
belief_engine.py into a persistent ledger keyed by claim hash.

Design laws:
- New belief = Beta(1,1) = maximum ignorance (mean 0.5, nonzero variance).
- Each origin contributes AT MOST ONCE per stance (repetition is not evidence).
- Below-trust-floor origins are recorded but contribute zero weight.
- Evidence history is capped (bounded memory, no runaway growth).
- Immutable updates: apply_evidence returns a new belief dict.
"""
from typing import Dict, Any, Optional
from uro.belief_engine import beta_update, beta_posterior, TRUST_FLOOR

EVIDENCE_LOG_CAP = 100


def new_belief(claim_hash: str, now: Optional[float] = None) -> Dict[str, Any]:
    """Create a fresh belief state at maximum ignorance."""
    return {
        "claim_hash": claim_hash,
        "alpha": 1.0,
        "beta": 1.0,
        "origins": {},          # "origin:stance" -> {"trust", "stance", "ignored"}
        "first_seen_at": now,
        "last_updated": now,
        "status": "active",     # active | superseded | refuted | retracted
        "superseded_by": None,
        "evidence_log": [],
    }


def apply_evidence(belief: Dict[str, Any], origin: str, trust: float,
                   stance: str, now: Optional[float] = None) -> Dict[str, Any]:
    """Apply one piece of evidence. stance is 'confirm' or 'counter'.

    Repetition from the same origin+stance is a no-op (saturation).
    Below-floor trust is recorded but contributes zero weight.
    Returns a NEW belief dict (input is not mutated).
    """
    if stance not in ("confirm", "counter"):
        raise ValueError(f"stance must be 'confirm' or 'counter', got {stance!r}")

    key = f"{origin}:{stance}"
    # Saturation: this origin already gave this stance -> no-op
    if key in belief["origins"]:
        return belief

    # Copy immutably
    b = dict(belief)
    b["origins"] = dict(belief["origins"])
    b["evidence_log"] = list(belief["evidence_log"])

    below_floor = trust < TRUST_FLOOR
    weight = 0.0 if below_floor else float(trust)

    if stance == "confirm":
        b["alpha"], b["beta"] = beta_update(b["alpha"], b["beta"], confirm_weight=weight)
    else:
        b["alpha"], b["beta"] = beta_update(b["alpha"], b["beta"], counter_weight=weight)

    b["origins"][key] = {"trust": float(trust), "stance": stance, "ignored": below_floor}
    b["last_updated"] = now if now is not None else b["last_updated"]
    b["evidence_log"].append({"origin": origin, "trust": float(trust),
                              "stance": stance, "at": now, "ignored": below_floor})
    if len(b["evidence_log"]) > EVIDENCE_LOG_CAP:
        b["evidence_log"] = b["evidence_log"][-EVIDENCE_LOG_CAP:]
    return b


def posterior_mean(belief: Dict[str, Any]) -> float:
    mean, _ = beta_posterior(belief["alpha"], belief["beta"])
    return mean


def posterior_variance(belief: Dict[str, Any]) -> float:
    _, var = beta_posterior(belief["alpha"], belief["beta"])
    return var


def belief_strength(belief: Dict[str, Any]) -> float:
    """Signed strength in [-1, 1]: how strongly the belief leans true/false.

    0 = maximum ignorance (mean 0.5). Positive = leans true, negative = leans false.
    """
    return (posterior_mean(belief) - 0.5) * 2.0


NUDGE_CAP = 1.0


def nudge_belief(belief, source_tag, signed_weight, now=None):
    """Apply a derived (entangled) nudge to a belief state.

    Saturates per source_tag so one origin's propagated signal is counted once.
    signed_weight > 0 confirms, < 0 counters; magnitude capped at NUDGE_CAP.
    Returns a NEW belief dict (input not mutated).
    """
    key = f"entangled:{source_tag}"
    if key in belief["origins"]:
        return belief
    capped = max(-NUDGE_CAP, min(NUDGE_CAP, float(signed_weight)))
    if capped == 0:
        return belief
    b = dict(belief)
    b["origins"] = dict(belief["origins"])
    b["evidence_log"] = list(belief["evidence_log"])
    if capped > 0:
        b["alpha"], b["beta"] = beta_update(b["alpha"], b["beta"], confirm_weight=capped)
    else:
        b["alpha"], b["beta"] = beta_update(b["alpha"], b["beta"], counter_weight=-capped)
    b["origins"][key] = {"trust": None, "stance": "entangled", "ignored": False, "weight": capped}
    b["last_updated"] = now if now is not None else b["last_updated"]
    b["evidence_log"].append({"origin": key, "weight": capped, "at": now})
    if len(b["evidence_log"]) > EVIDENCE_LOG_CAP:
        b["evidence_log"] = b["evidence_log"][-EVIDENCE_LOG_CAP:]
    return b
