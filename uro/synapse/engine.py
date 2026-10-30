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
MODULE: Synapse Modulation Engine
INTENT: Bidirectional, 24-axis neurochemical modulation of the relationship
        (R) object between two UROs. Every interaction outcome updates all
        axes per the governance roles and cross-talk rules in uro.nte.axes.
STANDARD: URO-STD-0001 S10.4
"""
from __future__ import annotations

import math
from typing import Dict

from uro.nte.axes import normalize_nte_state, NTEAxis

__all__ = ["InteractionOutcome", "modulate_synapse", "decay_synapse", "apply_cross_talk", "BASELINE"]

BASELINE = 50.0
CLAMP_MIN = 0.0
CLAMP_MAX = 100.0


# === START: Normalization Helpers ===
def _clamp(v: float) -> float:
    return max(CLAMP_MIN, min(CLAMP_MAX, v))


def _log_signed(x: float, gain: float = 1.0, k: float = 1.0) -> float:
    """
    Signed logarithmic shaping.

    Maps approximately:
        0  -> 0
        1  -> gain
       -1  -> -gain

    Values with magnitude greater than 1 are compressed logarithmically.
    """
    x = float(x)

    if x == 0.0:
        return 0.0

    sign = 1.0 if x > 0.0 else -1.0
    denom = math.log1p(k)

    if denom == 0.0:
        return gain * sign

    return gain * sign * (math.log1p(k * abs(x)) / denom)


def _normalize_levels(levels: Dict[NTEAxis, float]) -> Dict[NTEAxis, float]:
    """
    Return a clamped level map containing all 24 canonical axes.

    Backward compatibility:
        - missing axes become baseline
        - string-ish keys are tolerated where possible
        - values are clamped to [0, 100]
    """
    out = {}

    for axis in NTEAxis:
        value = None

        if isinstance(levels, dict):
            value = levels.get(axis)

            if value is None:
                value = levels.get(axis.value)

            if value is None:
                value = levels.get(axis.name)

        try:
            out[axis] = _clamp(float(value))
        except Exception:
            out[axis] = BASELINE

    return out


def InteractionOutcome(success: bool = True, latency_ms: float = 0.0,
                       novelty: float = 0.0, load: float = 0.0,
                       trust_signal: float = 0.0) -> dict:
    """Normalized outcome vector for one URO-to-URO interaction."""
    return {
        "success": bool(success),
        "latency_ms": float(latency_ms),
        "novelty": max(0.0, min(1.0, float(novelty))),
        "load": max(0.0, min(1.0, float(load))),
        "trust_signal": max(-1.0, min(1.0, float(trust_signal))),
    }
# === END: Normalization Helpers ===


# === START: Primary Axis Deltas (governance roles) ===
def _primary_deltas(o: dict) -> Dict[NTEAxis, float]:
    """
    Tolerant of partial outcome dicts.

    Produces deltas for all 24 canonical axes.
    Deltas are logarithmically shaped to compress extreme signals.
    """
    s = 1.0 if o.get("success", False) else -1.0
    nov = max(0.0, min(1.0, float(o.get("novelty", 0.0))))
    load = max(0.0, min(1.0, float(o.get("load", 0.0))))
    ts = max(-1.0, min(1.0, float(o.get("trust_signal", 0.0))))
    slow = 1.0 if float(o.get("latency_ms", 0.0)) > 2000.0 else 0.0

    d: Dict[NTEAxis, float] = {axis: 0.0 for axis in NTEAxis}

    # Biological axes
    d.update({
        NTEAxis.GLUTAMATE: _log_signed(
            s * (0.5 + nov),
            gain=2.0
        ),

        NTEAxis.GABA: _log_signed(
            -s,
            gain=1.5
        ),

        NTEAxis.DOPAMINE: _log_signed(
            s * (0.5 + nov),
            gain=3.0
        ),

        NTEAxis.SEROTONIN: _log_signed(
            s,
            gain=1.0
        ),

        NTEAxis.ACETYLCHOLINE: _log_signed(
            nov,
            gain=2.5
        ),

        NTEAxis.NOREPINEPHRINE: _log_signed(
            min(1.0, nov + 0.5 * slow),
            gain=2.0
        ),

        NTEAxis.EPINEPHRINE: _log_signed(
            -s + 0.67 * slow,
            gain=3.0
        ),

        NTEAxis.CORTISOL: _log_signed(
            -s + load + 0.5 * slow,
            gain=2.5
        ),

        NTEAxis.OXYTOCIN: _log_signed(
            0.5 * s + 0.5 * ts,
            gain=2.0
        ),

        NTEAxis.CANNABINOID: _log_signed(
            1.0 - nov,
            gain=0.5
        ),

        NTEAxis.MELATONIN: _log_signed(
            1.0 - load,
            gain=0.5
        ),

        NTEAxis.ADENOSINE: _log_signed(
            load + 0.25 * slow,
            gain=2.0
        ),
    })

    # Cognitive axes
    d.update({
        NTEAxis.FOCUS: _log_signed(
            0.6 * s - 0.7 * load + 0.2 * (1.0 - nov),
            gain=1.5
        ),

        NTEAxis.CREATIVITY: _log_signed(
            0.7 * nov + 0.2 * s - 0.1 * load,
            gain=2.0
        ),

        NTEAxis.ANALYSIS_DEPTH: _log_signed(
            0.5 * s + 0.4 * load - 0.2 * nov,
            gain=1.2
        ),

        NTEAxis.PATTERN_RECOGNITION: _log_signed(
            0.5 * s + 0.4 * nov - 0.3 * load,
            gain=1.5
        ),

        NTEAxis.ABSTRACTION_LEVEL: _log_signed(
            0.7 * nov + 0.2 * s - 0.1 * slow,
            gain=1.0
        ),

        NTEAxis.INFERENCE_SPEED: _log_signed(
            0.6 * s - 0.7 * slow - 0.3 * load,
            gain=1.5
        ),

        NTEAxis.UNCERTAINTY_TOLERANCE: _log_signed(
            0.5 * ts + 0.4 * nov - 0.3 * load,
            gain=1.2
        ),

        NTEAxis.COGNITIVE_FLEXIBILITY: _log_signed(
            0.7 * nov + 0.2 * s - 0.2 * load,
            gain=1.5
        ),

        NTEAxis.METACOGNITION: _log_signed(
            0.3 * s + 0.4 * load + 0.1 * (1.0 - nov),
            gain=1.0
        ),

        NTEAxis.ANALOGICAL_TRANSFER: _log_signed(
            0.6 * nov + 0.3 * ts,
            gain=1.0
        ),

        NTEAxis.DIALECTICAL_BALANCE: _log_signed(
            0.3 * s + 0.5 * ts - 0.2 * slow,
            gain=1.0
        ),

        NTEAxis.INSIGHT_READINESS: _log_signed(
            0.6 * nov + 0.2 * s + 0.2 * (1.0 - load),
            gain=1.25
        ),
    })

    return d
# === END: Primary Axis Deltas (governance roles) ===


# === START: Cross-Talk Resolution (second pass) ===
def _apply_cross_talk(levels: Dict[NTEAxis, float]) -> Dict[NTEAxis, float]:
    # RFC 38 / 28.2: engine-owned 24x24 second pass, single source of truth.
    normalized = _normalize_levels(levels)
    lv = dict(normalized)
    ex = lv[NTEAxis.GLUTAMATE] - lv[NTEAxis.GABA] - 20.0
    if ex > 0.0:
        d = 0.10 * ex
        lv[NTEAxis.GLUTAMATE] -= d
        lv[NTEAxis.GABA] += d
    lv[NTEAxis.OXYTOCIN] -= 0.15 * max(0.0, lv[NTEAxis.CORTISOL] - 50.0)
    lv[NTEAxis.CORTISOL] -= 0.10 * max(0.0, lv[NTEAxis.MELATONIN] - 50.0)
    lv[NTEAxis.DOPAMINE] -= 0.10 * max(0.0, lv[NTEAxis.ADENOSINE] - 50.0)
    lv[NTEAxis.DOPAMINE] *= (0.9 + 0.2 * lv[NTEAxis.SEROTONIN] / 100.0)
    lv[NTEAxis.EPINEPHRINE] -= 0.10 * max(0.0, lv[NTEAxis.OXYTOCIN] - 50.0) + 0.05 * max(0.0, lv[NTEAxis.GABA] - 50.0)
    lv[NTEAxis.CREATIVITY] -= 0.05 * max(0.0, lv[NTEAxis.FOCUS] - 70.0)
    lv[NTEAxis.INFERENCE_SPEED] -= 0.03 * max(0.0, lv[NTEAxis.ANALYSIS_DEPTH] - 60.0)
    lv[NTEAxis.COGNITIVE_FLEXIBILITY] += 0.05 * max(0.0, lv[NTEAxis.UNCERTAINTY_TOLERANCE] - 50.0)
    lv[NTEAxis.DIALECTICAL_BALANCE] += 0.04 * max(0.0, lv[NTEAxis.METACOGNITION] - 50.0)
    lv[NTEAxis.FOCUS] -= 0.10 * max(0.0, lv[NTEAxis.ADENOSINE] - 50.0)
    lv[NTEAxis.COGNITIVE_FLEXIBILITY] -= 0.08 * max(0.0, lv[NTEAxis.CORTISOL] - 60.0)
    lv[NTEAxis.METACOGNITION] += 0.05 * max(0.0, lv[NTEAxis.MELATONIN] - 50.0)
    lv[NTEAxis.ANALYSIS_DEPTH] -= 0.06 * max(0.0, lv[NTEAxis.EPINEPHRINE] - 60.0)
    lv[NTEAxis.ANALOGICAL_TRANSFER] += 0.04 * max(0.0, lv[NTEAxis.OXYTOCIN] - 50.0)
    lv[NTEAxis.PATTERN_RECOGNITION] -= 0.05 * max(0.0, lv[NTEAxis.CANNABINOID] - 60.0)
    lv[NTEAxis.INSIGHT_READINESS] += 0.06 * max(0.0, lv[NTEAxis.DOPAMINE] - 55.0)
    lv[NTEAxis.FOCUS] += 0.04 * max(0.0, lv[NTEAxis.GLUTAMATE] - 50.0)
    return {a: _clamp(v) for a, v in lv.items()}
def apply_cross_talk(levels):
    # RFC 38: public engine-owned cross-talk pass; string-key tolerant in and out.
    norm = _normalize_levels(levels)
    out = _apply_cross_talk(norm)
    return {a.value: v for a, v in out.items()}

# === END: Cross-Talk Resolution (second pass) ===


# === START: Modulation Entry Point ===
def modulate_synapse(synapse, outcome: dict) -> Dict[NTEAxis, float]:
    """Apply one interaction outcome to all 24 canonical axes."""
    levels = _normalize_levels(synapse.nte_state.levels)

    for axis, delta in _primary_deltas(outcome).items():
        levels[axis] = _clamp(levels[axis] + delta)

    levels = _apply_cross_talk(levels)
    synapse.nte_state.levels = levels
    return levels


def decay_synapse(synapse, rate: float = 0.02) -> Dict[NTEAxis, float]:
    """Homeostatic decay of all 24 canonical axes toward baseline."""
    levels = _normalize_levels(synapse.nte_state.levels)

    levels = {
        axis: _clamp(value + (BASELINE - value) * rate)
        for axis, value in levels.items()
    }

    synapse.nte_state.levels = levels
    return levels
# === END: Modulation Entry Point ===
