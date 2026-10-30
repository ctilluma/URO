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
MODULE: Cognitive Fuzzy Layer
INTENT: Maps context rates to a distribution over cognitive strategies, with
        NTE modulation and metacognitive re-evaluation. Makes cognition a
        self-aware, uncertainty-tracking reasoner.
STANDARD: URO-STD-0001 S27
"""
from __future__ import annotations
from typing import Dict, Tuple

from uro.cognition.matrix import FuzzyMatrixURO
from uro.nte.axes import NTEAxis

__all__ = ["COGNITIVE_OUTCOMES", "new_cognitive_matrix", "cognitive_inputs",
           "decide_strategy"]

COGNITIVE_OUTCOMES = [
    "answer_directly", "reason_deeply", "defer_specialist",
    "request_evidence", "abstain",
]

# Ideal input prototypes per strategy (values 0-100)
COGNITIVE_PROTOTYPES = {
    "answer_directly":  {"source_trust": 80, "coherence": 85, "novelty": 20, "urgency": 30, "plasticity": 40, "confidence": 80},
    "reason_deeply":    {"source_trust": 60, "coherence": 70, "novelty": 80, "urgency": 20, "plasticity": 80, "confidence": 50},
    "defer_specialist": {"source_trust": 20, "coherence": 60, "novelty": 70, "urgency": 30, "plasticity": 50, "confidence": 30},
    "request_evidence": {"source_trust": 50, "coherence": 20, "novelty": 50, "urgency": 20, "plasticity": 60, "confidence": 30},
    "abstain":          {"source_trust": 10, "coherence": 10, "novelty": 60, "urgency": 20, "plasticity": 30, "confidence": 10},
}


def new_cognitive_matrix() -> FuzzyMatrixURO:
    m = FuzzyMatrixURO.new()
    m.prototypes = dict(COGNITIVE_PROTOTYPES)
    m.seal()
    return m


def cognitive_inputs(source_trust: float, coherence: float, novelty: float, nte) -> Dict[str, float]:
    """Build the parallel input-rate vector, folding NTE modulation in."""
    return {
        "source_trust": source_trust,
        "coherence": coherence,
        "novelty": novelty,
        "urgency": nte.get_level(NTEAxis.EPINEPHRINE),      # fast-path pressure
        "plasticity": nte.get_level(NTEAxis.ACETYLCHOLINE), # openness to deep/novel
        "confidence": nte.get_level(NTEAxis.SEROTONIN),     # bar for answering
    }


def decide_strategy(matrix: FuzzyMatrixURO, inputs: Dict[str, float]) -> Tuple[str, Dict[str, float], bool]:
    """Return (strategy, distribution, should_reevaluate)."""
    dist = matrix.evaluate(inputs)
    return matrix.verdict.top(), dist, matrix.verdict.should_reevaluate()
