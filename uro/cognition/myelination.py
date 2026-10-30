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
MODULE: Myelination & Homeostatic Scaling
INTENT: Detect hot synapses, myelinate them, and scale infrastructure by NTE.
STANDARD: URO-STD-0001 S32
"""
from __future__ import annotations

import time
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

from uro.cognition.matrix import FuzzyMatrixURO
from uro.nte.axes import NTEAxis

__all__ = [
    "MyelinationLevel", "SynapseUsageStats", "SynapseUsageTracker",
    "detect_hot_synapses", "myelinate_synapse", "homeostatic_scale_decision",
    "GLOBAL_TRACKER", "record_synapse_use", "run_myelination_pass",
]


class MyelinationLevel:
    NONE = 0
    THIN = 1
    MODERATE = 2
    HEAVY = 3
    DEDICATED = 4


@dataclass
class SynapseUsageStats:
    synapse_id: str
    use_count: int
    last_used: float
    success_count: int
    failure_count: int
    myelination_level: int = MyelinationLevel.NONE
    total_latency_ms: float = 0.0

    @property
    def success_rate(self) -> float:
        t = self.success_count + self.failure_count
        return (self.success_count / t) if t > 0 else 0.0

    @property
    def avg_latency_ms(self) -> float:
        t = self.success_count + self.failure_count
        return (self.total_latency_ms / t) if t > 0 else 0.0


class SynapseUsageTracker:
    def __init__(self):
        self.usage: Dict[str, SynapseUsageStats] = {}

    def record_use(self, synapse_id: str, success: bool, latency_ms: float = 0.0):
        if synapse_id not in self.usage:
            self.usage[synapse_id] = SynapseUsageStats(
                synapse_id=synapse_id, use_count=0,
                last_used=time.time(), success_count=0, failure_count=0)
        s = self.usage[synapse_id]
        s.use_count += 1
        s.last_used = time.time()
        s.total_latency_ms += latency_ms
        if success:
            s.success_count += 1
        else:
            s.failure_count += 1

    def get_stats(self, synapse_id: str):
        return self.usage.get(synapse_id)

    def get_hot_synapses(self, min_uses=10, min_success_rate=0.8):
        hot = [s for s in self.usage.values()
               if s.use_count >= min_uses and s.success_rate >= min_success_rate]
        return sorted(hot, key=lambda s: s.use_count, reverse=True)


def detect_hot_synapses(tracker, min_uses=10, min_success_rate=0.8):
    now = time.time()
    out = []
    for s in tracker.get_hot_synapses(min_uses, min_success_rate):
        if (now - s.last_used) > 3600:
            continue
        level = _compute_myelination_level(s)
        out.append({
            "synapse_id": s.synapse_id, "use_count": s.use_count,
            "success_rate": round(s.success_rate, 3),
            "avg_latency_ms": round(s.avg_latency_ms, 2),
            "myelination_level": level,
            "recommendation": _myelination_recommendation(level),
        })
    return out


def _compute_myelination_level(s):
    if s.use_count >= 100 and s.success_rate >= 0.95:
        return MyelinationLevel.DEDICATED
    if s.use_count >= 50 and s.success_rate >= 0.90:
        return MyelinationLevel.HEAVY
    if s.use_count >= 20 and s.success_rate >= 0.85:
        return MyelinationLevel.MODERATE
    if s.use_count >= 10 and s.success_rate >= 0.80:
        return MyelinationLevel.THIN
    return MyelinationLevel.NONE


def _myelination_recommendation(level):
    return {
        MyelinationLevel.DEDICATED: "Spin up dedicated dock for this relationship",
        MyelinationLevel.HEAVY: "Cache responses, optimize routing",
        MyelinationLevel.MODERATE: "Increase timeout, prefetch related data",
        MyelinationLevel.THIN: "Monitor for increased use",
        MyelinationLevel.NONE: "No optimization needed",
    }[level]


def myelinate_synapse(synapse_id, level, registry):
    """Mark a synapse for optimization (registry side-table is source of truth)."""
    synapse = registry.resolve(synapse_id)
    if not synapse:
        return {"status": "error", "error": "Synapse not found"}

    rec = _myelination_recommendation(level)

    if not hasattr(registry, "myelination"):
        registry.myelination = {}
    registry.myelination[synapse_id] = {
        "level": level, "myelinated_at": time.time(), "recommendation": rec}

    if "metadata" in getattr(synapse, "model_fields", {}):
        synapse.metadata["myelination_level"] = level
        synapse.metadata["myelinated_at"] = time.time()
        if hasattr(synapse, "seal"):
            synapse.seal()

    return {"status": "success", "synapse_id": synapse_id,
            "myelination_level": level, "recommendation": rec}


def homeostatic_scale_decision(nte):
    m = FuzzyMatrixURO.new()
    m.prototypes = {
        "scale_up": {"epinephrine": 70, "cortisol": 60, "norepinephrine": 70,
                     "dopamine": 30, "serotonin": 40, "oxytocin": 30},
        "scale_down": {"epinephrine": 20, "cortisol": 20, "norepinephrine": 20,
                       "dopamine": 60, "serotonin": 70, "oxytocin": 70},
        "maintain": {"epinephrine": 40, "cortisol": 40, "norepinephrine": 40,
                     "dopamine": 50, "serotonin": 50, "oxytocin": 50},
        "emergency_scale": {"epinephrine": 95, "cortisol": 85, "norepinephrine": 90,
                            "dopamine": 10, "serotonin": 10, "oxytocin": 10},
    }
    inputs = {
        "epinephrine": nte.get_level(NTEAxis.EPINEPHRINE),
        "cortisol": nte.get_level(NTEAxis.CORTISOL),
        "norepinephrine": nte.get_level(NTEAxis.NOREPINEPHRINE),
        "dopamine": nte.get_level(NTEAxis.DOPAMINE),
        "serotonin": nte.get_level(NTEAxis.SEROTONIN),
        "oxytocin": nte.get_level(NTEAxis.OXYTOCIN),
    }
    dist = m.evaluate(inputs, agg="arithmetic")
    decision = m.verdict.top()
    if decision == "emergency_scale":
        reason = f"Critical stress: epi={inputs['epinephrine']:.0f}, cortisol={inputs['cortisol']:.0f}"
    elif decision == "scale_up":
        reason = f"High arousal: epi={inputs['epinephrine']:.0f}, nor={inputs['norepinephrine']:.0f}"
    elif decision == "scale_down":
        reason = f"Calm: serotonin={inputs['serotonin']:.0f}, oxytocin={inputs['oxytocin']:.0f}"
    else:
        reason = "Balanced state, maintain current scale"
    return decision, dist, reason


GLOBAL_TRACKER = SynapseUsageTracker()


def record_synapse_use(synapse_hex, success, latency_ms=0.0):
    GLOBAL_TRACKER.record_use(synapse_hex, success, latency_ms)


def run_myelination_pass(registry, tracker=None, min_uses=10, min_success_rate=0.8):
    tracker = tracker or GLOBAL_TRACKER
    return [myelinate_synapse(h["synapse_id"], h["myelination_level"], registry)
            for h in detect_hot_synapses(tracker, min_uses, min_success_rate)]
