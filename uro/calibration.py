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


"""V.A.U.R.O.S. Metacognitive Calibration (Phase 3b.3).

Posterior means are probability forecasts. When beliefs resolve against ground
truth, we score calibration (Brier), detect systematic confidence bias (ECE),
and recalibrate future confidence to empirical accuracy.

Design laws:
- Brier score = mean squared error of forecasts; lower is better.
- ECE = weighted |confidence - accuracy| across bins; detects over/under-confidence.
- Recalibration maps raw confidence to the empirical accuracy of its bin,
  so a habitually overconfident system automatically lowers its stated confidence.
- Empty ledger falls back to raw confidence (no data, no adjustment).
"""
from typing import Dict, Any, Optional, List


def new_calibration_ledger() -> Dict[str, Any]:
    return {
        "observations": [],   # list of {"confidence": float, "outcome": 0|1, "at": float}
        "pending": {},        # claim_hash -> {"confidence": float, "at": float}
    }


def add_observation(ledger, confidence: float, outcome: int, now: Optional[float] = None):
    """Record a resolved (confidence, outcome) pair directly."""
    c = max(0.0, min(1.0, float(confidence)))
    o = 1 if outcome else 0
    ledger["observations"].append({"confidence": c, "outcome": o, "at": now})
    return ledger


def record_prediction(ledger, claim_hash: str, confidence: float, now: Optional[float] = None):
    """Register a pending forecast for a claim (resolved later)."""
    ledger["pending"][str(claim_hash)] = {
        "confidence": max(0.0, min(1.0, float(confidence))), "at": now,
    }
    return ledger


def resolve_prediction(ledger, claim_hash: str, outcome: int, now: Optional[float] = None):
    """Resolve a pending forecast; unknown claims are a no-op."""
    key = str(claim_hash)
    if key not in ledger["pending"]:
        return ledger
    pend = ledger["pending"].pop(key)
    add_observation(ledger, pend["confidence"], outcome, now=now)
    return ledger


def brier_score(ledger) -> Optional[float]:
    obs = ledger["observations"]
    if not obs:
        return None
    return sum((o["confidence"] - o["outcome"]) ** 2 for o in obs) / len(obs)


def calibration_bins(ledger, n_bins: int = 10) -> Dict[int, Dict[str, float]]:
    """Bucket observations by confidence. Returns {bin_idx: {count, mean_confidence, mean_accuracy}}."""
    bins: Dict[int, List[Dict[str, Any]]] = {i: [] for i in range(n_bins)}
    for o in ledger["observations"]:
        idx = min(int(o["confidence"] * n_bins), n_bins - 1)
        bins[idx].append(o)
    out = {}
    for idx, items in bins.items():
        if not items:
            out[idx] = {"count": 0, "mean_confidence": 0.0, "mean_accuracy": 0.0}
            continue
        out[idx] = {
            "count": len(items),
            "mean_confidence": sum(i["confidence"] for i in items) / len(items),
            "mean_accuracy": sum(i["outcome"] for i in items) / len(items),
        }
    return out


def expected_calibration_error(ledger, n_bins: int = 10) -> float:
    """ECE = sum over bins of (bin_count / total) * |mean_confidence - mean_accuracy|."""
    obs = ledger["observations"]
    if not obs:
        return 0.0
    bins = calibration_bins(ledger, n_bins)
    total = len(obs)
    ece = 0.0
    for b in bins.values():
        if b["count"] == 0:
            continue
        ece += (b["count"] / total) * abs(b["mean_confidence"] - b["mean_accuracy"])
    return ece


def confidence_bias(ledger) -> float:
    """Signed bias = mean_confidence - mean_accuracy.
    Positive = overconfident, negative = underconfident."""
    obs = ledger["observations"]
    if not obs:
        return 0.0
    mc = sum(o["confidence"] for o in obs) / len(obs)
    ma = sum(o["outcome"] for o in obs) / len(obs)
    return mc - ma


def recalibrate(ledger, raw_confidence: float, n_bins: int = 10) -> float:
    """Map raw confidence to empirical bin accuracy (bins empty -> raw)."""
    raw = max(0.0, min(1.0, float(raw_confidence)))
    if not ledger["observations"]:
        return raw
    bins = calibration_bins(ledger, n_bins)
    idx = min(int(raw * n_bins), n_bins - 1)
    b = bins[idx]
    if b["count"] == 0:
        return raw
    return b["mean_accuracy"]
