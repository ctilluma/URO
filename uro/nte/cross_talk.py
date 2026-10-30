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
MODULE: NTE Cross-Talk URO
INTENT: Canonical multidimensional cross-talk field for all 24 NTE axes.
STANDARD: URO-STD-0001 S10 / Option A 24-axis canonical migration
"""
from __future__ import annotations

import math
from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, Field, ConfigDict

from uro.core.urid import URID
from uro.security.hashing import inahash
from uro.nte.axes import NTEAxis

__all__ = [
    "CrossTalkWhen",
    "CrossTalkEdgeURO",
    "CrossTalkPolicyURO",
    "NTECrossTalkURO",
    "apply_cross_talk_uro",
    "default_cross_talk_uro",
]


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, float(v)))


class CrossTalkWhen(str, Enum):
    HIGH = "high"
    LOW = "low"
    ALWAYS = "always"


class CrossTalkEdgeURO(BaseModel):
    """
    One directed cross-talk influence.

    Source axis affects target axis.
    """
    source: NTEAxis
    target: NTEAxis
    sign: float = Field(1.0, ge=-1.0, le=1.0)
    gain: float = Field(0.05, ge=0.0)
    threshold: float = Field(50.0, ge=0.0, le=100.0)
    log_k: float = Field(1.0, ge=0.0)
    when: CrossTalkWhen = CrossTalkWhen.HIGH
    note: str = ""

    model_config = ConfigDict(extra="allow")


class CrossTalkPolicyURO(BaseModel):
    """
    Compact category-level rule.

    This lets the cross-talk URO remain succinct while still expanding
    into a full multidimensional axis-to-axis field.
    """
    source_category: str
    target_category: str
    sign: float = Field(1.0, ge=-1.0, le=1.0)
    gain: float = Field(0.05, ge=0.0)
    threshold: float = Field(50.0, ge=0.0, le=100.0)
    log_k: float = Field(1.0, ge=0.0)
    when: CrossTalkWhen = CrossTalkWhen.HIGH
    note: str = ""

    model_config = ConfigDict(extra="allow")


class NTECrossTalkURO(BaseModel):
    """
    Canonical multidimensional cross-talk field for all 24 NTE axes.

    The field is represented succinctly by:
      1. axis -> category mapping
      2. category -> category policies
      3. explicit axis -> axis overrides

    This expands to a full 24x24 interaction surface without manually
    storing every dense edge.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    urid1: URID = Field(..., description="Source/owner URO")
    urid2: URID = Field(..., description="This cross-talk URO identity")

    version: str = Field("24.0.0", description="Cross-talk policy version")
    baseline: float = Field(50.0, description="Homeostatic baseline")
    max_pass_delta: float = Field(15.0, description="Maximum effect per pass per edge")

    categories: Dict[NTEAxis, str] = Field(
        default_factory=dict,
        description="Functional category for each axis"
    )

    policies: List[CrossTalkPolicyURO] = Field(
        default_factory=list,
        description="Compact category-to-category policies"
    )

    overrides: List[CrossTalkEdgeURO] = Field(
        default_factory=list,
        description="Explicit axis-to-axis overrides"
    )

    inahash: str = Field(default="", description="INAHASH seal")

    def compute_inahash(self) -> str:
        data = self.model_dump(exclude={"inahash"})
        msg = str(data).encode()
        return inahash(msg).hex()

    def seal(self) -> None:
        self.inahash = self.compute_inahash()

    def expanded_edges(self) -> List[CrossTalkEdgeURO]:
        """
        Expand compact policies into explicit directed edges.

        Overrides are appended after policy-generated edges and may be used
        to reinforce, weaken, or contradict category-level behavior.
        """
        policy_lookup = {}

        for policy in self.policies:
            key = (policy.source_category, policy.target_category)
            policy_lookup[key] = policy

        edges: List[CrossTalkEdgeURO] = []

        for source in NTEAxis:
            source_category = self.categories.get(source, "uncategorized")

            for target in NTEAxis:
                if source == target:
                    continue

                target_category = self.categories.get(target, "uncategorized")
                policy = policy_lookup.get((source_category, target_category))

                if policy is None:
                    continue

                edges.append(
                    CrossTalkEdgeURO(
                        source=source,
                        target=target,
                        sign=policy.sign,
                        gain=policy.gain,
                        threshold=policy.threshold,
                        log_k=policy.log_k,
                        when=policy.when,
                        note=policy.note or f"{source_category}->{target_category}",
                    )
                )

        edges.extend(self.overrides)
        return edges


def _log_effect(excess: float, edge: CrossTalkEdgeURO) -> float:
    """
    Logarithmic cross-talk effect.

    Excess is measured relative to threshold.
    The denominator normalizes against a 50-point excess, so an axis at
    100 with threshold 50 produces approximately the configured gain.
    """
    if excess == 0.0:
        return 0.0

    denom = math.log1p(edge.log_k * 50.0)

    if denom == 0.0:
        return edge.sign * edge.gain

    return (
        edge.sign
        * edge.gain
        * math.log1p(edge.log_k * abs(excess))
        / denom
    )


def apply_cross_talk_uro(
    levels: Dict[NTEAxis, float],
    cross_talk: NTECrossTalkURO,
) -> Dict[NTEAxis, float]:
    """
    Apply one full multidimensional cross-talk pass.

    Uses a snapshot of the input levels so edge order does not create
    path-dependent cascades inside a single pass.
    """
    snapshot = dict(levels)
    updates: Dict[NTEAxis, float] = {axis: 0.0 for axis in levels}

    for edge in cross_talk.expanded_edges():
        source_level = snapshot.get(edge.source, cross_talk.baseline)

        if edge.when == CrossTalkWhen.HIGH:
            excess = max(0.0, source_level - edge.threshold)
        elif edge.when == CrossTalkWhen.LOW:
            excess = max(0.0, edge.threshold - source_level)
        else:
            excess = source_level - edge.threshold

        if abs(excess) <= 1e-9:
            continue

        effect = _log_effect(excess, edge)
        effect = max(-cross_talk.max_pass_delta, min(cross_talk.max_pass_delta, effect))

        updates[edge.target] = updates.get(edge.target, 0.0) + effect

    out: Dict[NTEAxis, float] = dict(levels)

    for axis, delta in updates.items():
        out[axis] = _clamp(out.get(axis, 50.0) + delta)

    return out


def default_cross_talk_uro() -> NTECrossTalkURO:
    """
    Canonical default 24-axis cross-talk field.

    This is intentionally succinct but expands to a full multidimensional
    surface via category policies.
    """
    categories = {
        # Biological
        NTEAxis.GLUTAMATE: "excitation",
        NTEAxis.GABA: "inhibition",
        NTEAxis.DOPAMINE: "reward",
        NTEAxis.SEROTONIN: "control",
        NTEAxis.ACETYLCHOLINE: "plasticity",
        NTEAxis.NOREPINEPHRINE: "arousal",
        NTEAxis.EPINEPHRINE: "acute_stress",
        NTEAxis.CORTISOL: "chronic_stress",
        NTEAxis.OXYTOCIN: "trust",
        NTEAxis.CANNABINOID: "forgetting",
        NTEAxis.MELATONIN: "consolidation",
        NTEAxis.ADENOSINE: "fatigue",

        # Cognitive
        NTEAxis.FOCUS: "control",
        NTEAxis.CREATIVITY: "exploration",
        NTEAxis.ANALYSIS_DEPTH: "reasoning",
        NTEAxis.PATTERN_RECOGNITION: "reasoning",
        NTEAxis.ABSTRACTION_LEVEL: "exploration",
        NTEAxis.INFERENCE_SPEED: "reasoning",
        NTEAxis.UNCERTAINTY_TOLERANCE: "resilience",
        NTEAxis.COGNITIVE_FLEXIBILITY: "exploration",
        NTEAxis.METACOGNITION: "control",
        NTEAxis.ANALOGICAL_TRANSFER: "exploration",
        NTEAxis.DIALECTICAL_BALANCE: "control",
        NTEAxis.INSIGHT_READINESS: "insight",
    }

    policies = [
        CrossTalkPolicyURO(
            source_category="excitation",
            target_category="inhibition",
            sign=1.0,
            gain=8.0,
            threshold=70.0,
            note="E/I balance: high excitation recruits inhibition",
        ),
        CrossTalkPolicyURO(
            source_category="inhibition",
            target_category="excitation",
            sign=-1.0,
            gain=4.0,
            threshold=60.0,
            note="Inhibition dampens excitation",
        ),
        CrossTalkPolicyURO(
            source_category="chronic_stress",
            target_category="trust",
            sign=-1.0,
            gain=10.0,
            threshold=50.0,
            note="Sustained stress erodes bonding",
        ),
        CrossTalkPolicyURO(
            source_category="chronic_stress",
            target_category="exploration",
            sign=-1.0,
            gain=4.0,
            threshold=50.0,
            note="Chronic stress suppresses exploration",
        ),
        CrossTalkPolicyURO(
            source_category="chronic_stress",
            target_category="insight",
            sign=-1.0,
            gain=2.5,
            threshold=50.0,
            note="Chronic stress suppresses insight readiness",
        ),
        CrossTalkPolicyURO(
            source_category="consolidation",
            target_category="chronic_stress",
            sign=-1.0,
            gain=3.0,
            threshold=50.0,
            note="Recovery opposes chronic stress",
        ),
        CrossTalkPolicyURO(
            source_category="consolidation",
            target_category="insight",
            sign=1.0,
            gain=2.5,
            threshold=50.0,
            note="Consolidation supports insight readiness",
        ),
        CrossTalkPolicyURO(
            source_category="fatigue",
            target_category="reward",
            sign=-1.0,
            gain=5.0,
            threshold=50.0,
            note="Fatigue inhibits reward learning",
        ),
        CrossTalkPolicyURO(
            source_category="fatigue",
            target_category="reasoning",
            sign=-1.0,
            gain=2.5,
            threshold=50.0,
            note="Fatigue degrades reasoning",
        ),
        CrossTalkPolicyURO(
            source_category="fatigue",
            target_category="exploration",
            sign=-1.0,
            gain=2.5,
            threshold=50.0,
            note="Fatigue reduces exploration",
        ),
        CrossTalkPolicyURO(
            source_category="control",
            target_category="reward",
            sign=1.0,
            gain=1.5,
            threshold=60.0,
            note="Control gates reward translation",
        ),
        CrossTalkPolicyURO(
            source_category="control",
            target_category="acute_stress",
            sign=-1.0,
            gain=2.5,
            threshold=60.0,
            note="Cognitive control calms urgency",
        ),
        CrossTalkPolicyURO(
            source_category="control",
            target_category="exploration",
            sign=-1.0,
            gain=2.0,
            threshold=70.0,
            note="High control narrows exploration",
        ),
        CrossTalkPolicyURO(
            source_category="trust",
            target_category="acute_stress",
            sign=-1.0,
            gain=5.0,
            threshold=50.0,
            note="Social buffering calms acute urgency",
        ),
        CrossTalkPolicyURO(
            source_category="inhibition",
            target_category="acute_stress",
            sign=-1.0,
            gain=2.5,
            threshold=50.0,
            note="Inhibition calms acute urgency",
        ),
        CrossTalkPolicyURO(
            source_category="resilience",
            target_category="acute_stress",
            sign=-1.0,
            gain=2.5,
            threshold=50.0,
            note="Uncertainty tolerance buffers acute stress",
        ),
        CrossTalkPolicyURO(
            source_category="resilience",
            target_category="chronic_stress",
            sign=-1.0,
            gain=2.5,
            threshold=50.0,
            note="Uncertainty tolerance buffers chronic stress",
        ),
        CrossTalkPolicyURO(
            source_category="reward",
            target_category="exploration",
            sign=1.0,
            gain=2.5,
            threshold=50.0,
            note="Reward encourages exploration",
        ),
        CrossTalkPolicyURO(
            source_category="exploration",
            target_category="plasticity",
            sign=1.0,
            gain=2.5,
            threshold=50.0,
            note="Exploration increases plasticity pressure",
        ),
        CrossTalkPolicyURO(
            source_category="exploration",
            target_category="control",
            sign=1.0,
            gain=1.0,
            threshold=70.0,
            note="Exploration broadens control",
        ),
        CrossTalkPolicyURO(
            source_category="plasticity",
            target_category="reward",
            sign=1.0,
            gain=2.0,
            threshold=50.0,
            note="Plasticity supports reward learning",
        ),
        CrossTalkPolicyURO(
            source_category="reasoning",
            target_category="control",
            sign=1.0,
            gain=2.5,
            threshold=50.0,
            note="Reasoning strengthens cognitive control",
        ),
        CrossTalkPolicyURO(
            source_category="insight",
            target_category="reward",
            sign=1.0,
            gain=2.5,
            threshold=50.0,
            note="Insight readiness amplifies reward learning",
        ),
    ]

    overrides: List[CrossTalkEdgeURO] = []

    ct = NTECrossTalkURO(
        urid1=URID(),
        urid2=URID(),
        version="24.0.0",
        baseline=50.0,
        max_pass_delta=20.0,
        categories=categories,
        policies=policies,
        overrides=overrides,
    )

    ct.seal()
    return ct
