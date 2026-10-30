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


# =====================================================================
# MODULE START : uro.learning.primitives
# ---------------------------------------------------------------------
# FILE         : uro/learning/primitives.py
# PURPOSE      : Learning primitives: cause/effect, experimentation,
#                feedback, observation, sequencing, gap-segmented pattern
#                analysis, differentiate/correlate (RFC 90).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"Learning primitives (RFC 90)."

from __future__ import annotations

import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List

__all__ = ["CauseEffectLedger", "ExperimentLog", "FeedbackLoop",
           "ObservationRecord", "SequenceTracker", "segment_by_gaps",
           "correlate_gaps", "differentiate", "correlate"]


class CauseEffectLedger:
    "PURPOSE: Record and query cause-effect relations (RFC 90.1)."

    def __init__(self) -> None:
        self._effects: Dict[Any, Counter] = defaultdict(Counter)
        self._causes: Dict[Any, Counter] = defaultdict(Counter)

    def record(self, cause: Any, effect: Any, weight: float = 1.0) -> None:
        "PURPOSE: Add one cause-effect observation."
        self._effects[cause][effect] += weight
        self._causes[effect][cause] += weight

    def effects_of(self, cause: Any) -> Dict[Any, float]:
        "PURPOSE: Ranked effects observed for a cause."
        return dict(self._effects.get(cause, Counter()))

    def causes_of(self, effect: Any) -> Dict[Any, float]:
        "PURPOSE: Ranked causes observed for an effect."
        return dict(self._causes.get(effect, Counter()))


class ExperimentLog:
    "PURPOSE: Try action UROs on other UROs when not busy (RFC 90.2)."

    def __init__(self) -> None:
        self.trials: List[Dict[str, Any]] = []

    def schedule(self, action: Any, target: Any, busy: bool):
        "PURPOSE: Queue an experiment only when the object is not busy."
        if busy:
            return None
        self.trials.append({"id": len(self.trials), "action": action,
                            "target": target, "result": None})
        return len(self.trials) - 1

    def record_result(self, trial_id: int, result: Any) -> None:
        "PURPOSE: Map the outcome of one experiment (RFC 90.2)."
        self.trials[trial_id]["result"] = result


class FeedbackLoop:
    "PURPOSE: Proportional feedback adjustment toward a target (RFC 90.3)."

    def __init__(self, gain: float = 0.5) -> None:
        self.gain = gain

    def step(self, current: float, target: float) -> float:
        "PURPOSE: Return the adjustment moving current toward target."
        return self.gain * (target - current)


@dataclass
class ObservationRecord:
    "PURPOSE: Timestamped snapshot of what the object is seeing (RFC 90.4)."
    stream: str
    payload: Any
    t: float = field(default_factory=time.time)


class SequenceTracker:
    "PURPOSE: Track X-followed-by-Y ordering and predict successors (RFC 90.5)."

    def __init__(self) -> None:
        self._next: Dict[Any, Counter] = defaultdict(Counter)
        self._last: Any = None

    def observe(self, event: Any) -> None:
        "PURPOSE: Append one event to the sequence history."
        if self._last is not None:
            self._next[self._last][event] += 1
        self._last = event

    def predict_next(self, event: Any) -> Any:
        "PURPOSE: Most frequent successor of event."
        counts = self._next.get(event)
        if not counts:
            return None
        return counts.most_common(1)[0][0]


def segment_by_gaps(series: List[float], threshold: float) -> List[List[float]]:
    "PURPOSE: RFC 90.6: gaps segment data into patterns."
    segments: List[List[float]] = []
    current: List[float] = []
    prev = None
    for value in series:
        if prev is not None and abs(value - prev) > threshold:
            segments.append(current)
            current = []
        current.append(value)
        prev = value
    if current:
        segments.append(current)
    return segments


def _bounds(segments: List[List[float]]) -> List[int]:
    "PURPOSE: Cumulative boundary indices of segments."
    out = []
    acc = 0
    for seg in segments:
        acc += len(seg)
        out.append(acc)
    return out


def correlate_gaps(segs_a, segs_b, tolerance: int = 1) -> int:
    "PURPOSE: RFC 90.6: correlate gap boundaries across two streams."
    bounds_b = _bounds(segs_b)
    matches = 0
    for a in _bounds(segs_a):
        if any(abs(a - b) <= tolerance for b in bounds_b):
            matches += 1
    return matches


def differentiate(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    "PURPOSE: RFC 90.7: break a URO payload into components (make smaller)."
    return [{"kind": "component", "key": k, "value": v}
            for k, v in payload.items()]


def correlate(components: List[Dict[str, Any]]) -> Dict[str, Any]:
    "PURPOSE: RFC 90.8: group components into a larger system (make bigger)."
    return {c["key"]: c["value"] for c in components}
# =====================================================================
# MODULE END   : uro.learning.primitives
# =====================================================================
