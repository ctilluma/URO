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


"""
MODULE: Memory Fuzzy Layer (homeostatic memory)
INTENT: Fuzzy retrieval scoring + homeostatic lifecycle decisions
        (keep/promote/consolidate/prune), modulated by NTE
        (melatonin=consolidate drive, cannabinoid=prune pressure) and source
        trust. Replaces hardcoded thresholds in the memory dock.
STANDARD: URO-STD-0001 S28

DESIGN:
  * Lifecycle matrix uses ARITHMETIC aggregation (soft, additive) EXCEPT
    'prune', which uses GEOMETRIC (strict conjunction): every sign must
    agree before a memory is deleted. Critical/high-trust memories
    therefore survive pruning pressure; true junk does not.
  * Decisions are argmax-based (relative), not absolute thresholds.
"""
from __future__ import annotations

import time
from typing import Dict, List, Tuple, Any

from uro.cognition.matrix import FuzzyMatrixURO
from uro.nte.axes import NTEAxis

__all__ = [
    "MEMORY_OUTCOMES", "LIFECYCLE_OUTCOMES", "new_memory_matrix",
    "new_lifecycle_matrix", "memory_inputs", "memory_decision",
    "should_promote_fuzzy", "should_decay_fuzzy",
    "rank_memories_for_retrieval", "cosine_similarity",
]

MEMORY_OUTCOMES = ["retrieve_strong", "retrieve_weak"]
LIFECYCLE_OUTCOMES = ["keep", "promote", "consolidate", "prune"]

RETRIEVAL_PROTOTYPES = {
    "retrieve_strong": {"similarity": 85, "recency": 70, "frequency": 70, "salience": 60, "source_trust": 80, "consolidation": 70, "prune_pressure": 10, "consolidate_pressure": 30},
    "retrieve_weak":   {"similarity": 50, "recency": 40, "frequency": 30, "salience": 30, "source_trust": 50, "consolidation": 40, "prune_pressure": 30, "consolidate_pressure": 30},
}

LIFECYCLE_PROTOTYPES = {
    "keep":        {"frequency": 50, "recency": 60, "salience": 50, "source_trust": 50, "consolidation": 40, "prune_pressure": 30, "consolidate_pressure": 30},
    "promote":     {"frequency": 80, "recency": 70, "salience": 70, "source_trust": 60, "consolidation": 40, "prune_pressure": 10, "consolidate_pressure": 50},
    "consolidate": {"frequency": 70, "recency": 20, "salience": 60, "source_trust": 70, "consolidation": 60, "prune_pressure": 20, "consolidate_pressure": 85},
    "prune":       {"frequency": 10, "recency": 10, "salience": 20, "source_trust": 20, "consolidation": 20, "prune_pressure": 85, "consolidate_pressure": 20},
}


def new_memory_matrix() -> FuzzyMatrixURO:
    m = FuzzyMatrixURO.new()
    m.prototypes = dict(RETRIEVAL_PROTOTYPES)
    m.seal()
    return m


def new_lifecycle_matrix() -> FuzzyMatrixURO:
    m = FuzzyMatrixURO.new()
    m.prototypes = dict(LIFECYCLE_PROTOTYPES)
    m.seal()
    return m


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    n1 = sum(a * a for a in v1) ** 0.5
    n2 = sum(b * b for b in v2) ** 0.5
    return (dot / (n1 * n2)) if n1 and n2 else 0.0


# ── duck-typed entry readers ────────────────────────────────────────────────
def _g(obj, name, default):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _entry_rates(entry, query_embedding=None, trust=None) -> Dict[str, float]:
    emb = _g(entry, "vector_embedding", None)
    sim = (cosine_similarity(query_embedding, emb) * 100) if (query_embedding and emb) else 50.0
    last = _g(entry, "last_accessed", time.time())
    age = max(0.0, time.time() - last)
    recency = max(0.0, 100.0 - age / 36.0)
    frequency = min(100.0, _g(entry, "access_count", 0) * 10.0)
    tags = list(_g(entry, "tags", []) or [])
    meta = _g(entry, "metadata", {}) or {}
    sal = 50.0
    if "critical" in tags or meta.get("priority") == "critical":
        sal = 90.0
    elif "high" in tags or meta.get("priority") == "high":
        sal = 70.0
    elif "low" in tags or meta.get("priority") == "low":
        sal = 30.0
    src = trust if trust is not None else meta.get("source_trust", 50.0)
    cons = meta.get("consolidation", 40.0)
    return {"similarity": sim, "recency": recency, "frequency": frequency,
            "salience": sal, "source_trust": src, "consolidation": cons}


def _lifecycle_inputs(rates, nte, tier_load: float) -> Dict[str, float]:
    return {
        "frequency": rates["frequency"],
        "recency": rates["recency"],
        "salience": rates["salience"],
        "source_trust": rates["source_trust"],
        "consolidation": rates["consolidation"],
        "prune_pressure": max(nte.get_level(NTEAxis.CANNABINOID), tier_load * 100),
        "consolidate_pressure": nte.get_level(NTEAxis.MELATONIN),
    }


def should_promote_fuzzy(entry, nte, tier_load: float = 0.5) -> Tuple[bool, str]:
    """Fuzzy replacement for hardcoded should_promote()."""
    m = new_lifecycle_matrix()
    rates = _entry_rates(entry)
    dist = m.evaluate(_lifecycle_inputs(rates, nte, tier_load),
                      agg="arithmetic", strict_outcomes={"prune"})
    pc = dist.get("promote", 0) + dist.get("consolidate", 0)
    top = m.verdict.top()
    ok = (top in ("promote", "consolidate")) and pc > dist.get("prune", 0)
    return ok, f"top={top} promote+cons={pc:.2f} prune={dist.get('prune', 0):.2f}"


def should_decay_fuzzy(entry, nte, tier_load: float = 0.5) -> Tuple[bool, str]:
    """Fuzzy replacement for hardcoded should_decay()."""
    m = new_lifecycle_matrix()
    rates = _entry_rates(entry)
    dist = m.evaluate(_lifecycle_inputs(rates, nte, tier_load),
                      agg="arithmetic", strict_outcomes={"prune"})
    p = dist.get("prune", 0)
    ok = (m.verdict.top() == "prune") and p > 0.3
    return ok, f"top={m.verdict.top()} prune={p:.2f}"


def memory_inputs(similarity, recency, frequency, salience,
                  source_trust, consolidation, nte) -> Dict[str, float]:
    return {
        "similarity": similarity, "recency": recency, "frequency": frequency,
        "salience": salience, "source_trust": source_trust,
        "consolidation": consolidation,
        "prune_pressure": nte.get_level(NTEAxis.CANNABINOID),
        "consolidate_pressure": nte.get_level(NTEAxis.MELATONIN),
    }


def memory_decision(matrix, inputs) -> Tuple[str, Dict[str, float], float]:
    dist = matrix.evaluate(inputs, agg="arithmetic")
    strength = dist.get("retrieve_strong", 0) + 0.5 * dist.get("retrieve_weak", 0)
    return matrix.verdict.top(), dist, strength


def rank_memories_for_retrieval(entries, query_embedding=None,
                                trust_map=None, nte=None) -> List[Tuple[Any, float]]:
    """Rank entries by fuzzy retrieval strength (trust-weighted)."""
    m = new_memory_matrix()
    trust_map = trust_map or {}
    out = []
    for e in entries:
        src = _g(e, "urid1_source", "")
        rates = _entry_rates(e, query_embedding, trust_map.get(src))
        if nte is not None:
            inputs = memory_inputs(rates["similarity"], rates["recency"], rates["frequency"],
                                   rates["salience"], rates["source_trust"], rates["consolidation"], nte)
        else:
            inputs = dict(rates)
            inputs["prune_pressure"] = 20.0
            inputs["consolidate_pressure"] = 30.0
        action, dist, strength = memory_decision(m, inputs)
        out.append((e, strength))
    return sorted(out, key=lambda t: -t[1])
