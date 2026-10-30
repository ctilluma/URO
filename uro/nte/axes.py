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
MODULE: NTE Axes (24-Axis Canonical System)
INTENT: Define the 24 neurotransmitter/cognitive axes that form the swarm's governance
        primitives. Each axis is a URO with its own lineage, custody, and state.
STANDARD: URO-STD-0001 S10
"""
from __future__ import annotations

from enum import Enum
from typing import Dict

from pydantic import BaseModel, Field

__all__ = ["NTEAxis", "NTEAxisGovernance", "NTE_AXES", "CognitiveAxis", "AXES_24", "nte24"]


from enum import EnumMeta as _ConstructibleEnumMeta

class _ConstructibleAxisMeta(_ConstructibleEnumMeta):
    """Legacy constructible-axis compatibility: NTEAxis(name=..., role=...).

    Only intercepts keyword-only calls (which previously raised TypeError); all
    normal Enum usage (member access, value/name lookup, iteration) is unchanged.
    """
    def __call__(cls, *args, **kwargs):
        if kwargs and not args:
            name = kwargs.get("name")
            if name is not None:
                target = str(name).lower()
                for member in cls:
                    if member.value == target or member.name.lower() == target:
                        return member
            return next(iter(cls))
        return super().__call__(*args, **kwargs)


class NTEAxis(str, Enum, metaclass=_ConstructibleAxisMeta):
    """The 24 neurotransmitter/cognitive equivalences."""

    # Biological axes
    GLUTAMATE = "glutamate"
    GABA = "gaba"
    DOPAMINE = "dopamine"
    SEROTONIN = "serotonin"
    ACETYLCHOLINE = "acetylcholine"
    NOREPINEPHRINE = "norepinephrine"
    EPINEPHRINE = "epinephrine"
    CORTISOL = "cortisol"
    OXYTOCIN = "oxytocin"
    CANNABINOID = "cannabinoid"
    MELATONIN = "melatonin"
    ADENOSINE = "adenosine"

    # Cognitive axes
    FOCUS = "focus"
    CREATIVITY = "creativity"
    ANALYSIS_DEPTH = "analysis_depth"
    PATTERN_RECOGNITION = "pattern_recognition"
    ABSTRACTION_LEVEL = "abstraction_level"
    INFERENCE_SPEED = "inference_speed"
    UNCERTAINTY_TOLERANCE = "uncertainty_tolerance"
    COGNITIVE_FLEXIBILITY = "cognitive_flexibility"
    METACOGNITION = "metacognition"
    ANALOGICAL_TRANSFER = "analogical_transfer"
    DIALECTICAL_BALANCE = "dialectical_balance"
    INSIGHT_READINESS = "insight_readiness"


class NTEAxisGovernance(BaseModel):
    """Governance role and cross-talk for each NTE axis."""

    axis: NTEAxis
    niche: str
    governance_role: str
    cross_talk: Dict[str, str] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


NTE_AXES: Dict[NTEAxis, NTEAxisGovernance] = {
    NTEAxis.GLUTAMATE: NTEAxisGovernance(
        axis=NTEAxis.GLUTAMATE,
        niche="Excitation",
        governance_role="Drive to act and learn. High = strong excitation, active learning. Low = conservative, slow to change.",
        cross_talk={
            "opposed_by": "GABA (E/I balance)",
            "modulated_by": "Cannabinoid (retrograde gating)",
        },
    ),
    NTEAxis.GABA: NTEAxisGovernance(
        axis=NTEAxis.GABA,
        niche="Inhibition",
        governance_role="Filtering and confidence gating. High = strong rejection of weak signals. Low = permissive, noise-tolerant.",
        cross_talk={
            "opposes": "Glutamate (E/I balance)",
            "co_released_with": "Serotonin",
        },
    ),
    NTEAxis.DOPAMINE: NTEAxisGovernance(
        axis=NTEAxis.DOPAMINE,
        niche="Reward/Learning",
        governance_role="Learning rate on prediction errors. High = strong belief updates on surprises. Low = confirmation of existing models.",
        cross_talk={
            "modulated_by": "Serotonin (impulse control), Norepinephrine (novelty priming)",
            "inhibited_by": "GABA (prevents over-reward)",
        },
    ),
    NTEAxis.SEROTONIN: NTEAxisGovernance(
        axis=NTEAxis.SEROTONIN,
        niche="Decision/Patience",
        governance_role="Decision threshold and confidence calibration. High = willing to wait for more evidence. Low = quick commitment.",
        cross_talk={
            "opposes": "Dopamine (explore-exploit balance)",
            "modulates": "Dopamine action translation",
        },
    ),
    NTEAxis.ACETYLCHOLINE: NTEAxisGovernance(
        axis=NTEAxis.ACETYLCHOLINE,
        niche="Plasticity",
        governance_role="Learning rate for novel inputs and expected uncertainty. High = updating from data. Low = relying on priors.",
        cross_talk={
            "opposed_by": "Norepinephrine (unexpected uncertainty)",
            "modulated_by": "GABA (gates ACh release)",
        },
    ),
    NTEAxis.NOREPINEPHRINE: NTEAxisGovernance(
        axis=NTEAxis.NOREPINEPHRINE,
        niche="Arousal",
        governance_role="Available cognitive bandwidth and network reset. High = ready to re-route, explore. Low = focus on current task.",
        cross_talk={
            "gates": "Dopamine reward learning",
            "opposed_by": "GABA",
        },
    ),
    NTEAxis.EPINEPHRINE: NTEAxisGovernance(
        axis=NTEAxis.EPINEPHRINE,
        niche="Acute Stress",
        governance_role="Urgency signal. High = reject low-trust sources, route through fast-path. Low = calm processing.",
        cross_talk={
            "synergizes_with": "Norepinephrine (arousal)",
            "opposed_by": "GABA (calming), Oxytocin (social buffering)",
        },
    ),
    NTEAxis.CORTISOL: NTEAxisGovernance(
        axis=NTEAxis.CORTISOL,
        niche="Chronic Stress",
        governance_role="Sustained load management and structural adaptation. High = reallocate resources, reduce exploration.",
        cross_talk={
            "downregulates": "Oxytocin (sustained stress erodes bonding)",
            "opposed_by": "Melatonin (recovery hormone)",
        },
    ),
    NTEAxis.OXYTOCIN: NTEAxisGovernance(
        axis=NTEAxis.OXYTOCIN,
        niche="Trust/Bonding",
        governance_role="The trust currency. Bonds between UROs. High = in-group loyalty, out-group caution.",
        cross_talk={
            "amplified_by": "Dopamine (social reward)",
            "opposed_by": "Epinephrine (stress disrupts bonding)",
        },
    ),
    NTEAxis.CANNABINOID: NTEAxisGovernance(
        axis=NTEAxis.CANNABINOID,
        niche="Forgetting",
        governance_role="Memory pruning and trust decay. High = actively forgetting outdated patterns. Low = holding onto everything.",
        cross_talk={
            "gates": "GABA and Glutamate (retrograde signaling)",
            "modulates": "Dopamine (VTA disinhibition)",
        },
    ),
    NTEAxis.MELATONIN: NTEAxisGovernance(
        axis=NTEAxis.MELATONIN,
        niche="Consolidation",
        governance_role="Consolidation and maintenance cycles. High = replay, consolidate, garbage collect. Low = active encoding.",
        cross_talk={
            "inverse_with": "Cortisol (circadian rhythm)",
            "synthesized_from": "Serotonin",
        },
    ),
    NTEAxis.ADENOSINE: NTEAxisGovernance(
        axis=NTEAxis.ADENOSINE,
        niche="Fatigue",
        governance_role="Resource depletion and load shedding. High = shed load, enter power-save. Low = fresh, full resources.",
        cross_talk={
            "inhibits": "Dopamine release (tired = less motivated)",
            "triggers": "Melatonin (fatigue \u2192 rest \u2192 consolidation)",
        },
    ),
}

# --- Convergence compatibility exports (auto-generated) ---
# compat:NTEVector
try:
    from uro.canonical_shim import NTEVector
except Exception:
    NTEVector = None
# compat:NTEVectorModel
try:
    from uro.api.models import NTEVectorModel
except Exception:
    NTEVectorModel = None


# === START: CognitiveAxis-24-taxonomy ===
class CognitiveAxis(str, Enum):
    """Deprecated compatibility enum for the 12 cognitive axes.

    Canonical state uses NTEAxis, which now contains all 24 axes.
    This enum remains temporarily so existing imports do not crash.
    """

    FOCUS = "focus"
    CREATIVITY = "creativity"
    ANALYSIS_DEPTH = "analysis_depth"
    PATTERN_RECOGNITION = "pattern_recognition"
    ABSTRACTION_LEVEL = "abstraction_level"
    INFERENCE_SPEED = "inference_speed"
    UNCERTAINTY_TOLERANCE = "uncertainty_tolerance"
    COGNITIVE_FLEXIBILITY = "cognitive_flexibility"
    METACOGNITION = "metacognition"
    ANALOGICAL_TRANSFER = "analogical_transfer"
    DIALECTICAL_BALANCE = "dialectical_balance"
    INSIGHT_READINESS = "insight_readiness"


BIOLOGICAL_AXES = (
    "glutamate",
    "gaba",
    "dopamine",
    "serotonin",
    "acetylcholine",
    "norepinephrine",
    "epinephrine",
    "cortisol",
    "oxytocin",
    "cannabinoid",
    "melatonin",
    "adenosine",
)

COGNITIVE_AXES = tuple(a.value for a in CognitiveAxis)

# Canonical 24-axis order is the order of NTEAxis itself.
AXES_24 = tuple(a.value for a in NTEAxis)


def nte24(state=None, baseline=50.0):
    """Full 24-axis state as {axis_value: level}, baseline-filled."""
    state = state or {}
    out = {}

    for axis in NTEAxis:
        value = state.get(axis, state.get(axis.value, baseline))
        try:
            out[axis.value] = float(value)
        except Exception:
            out[axis.value] = baseline

    return out


_COGNITIVE_GOVERNANCE = {
    NTEAxis.FOCUS: NTEAxisGovernance(
        axis=NTEAxis.FOCUS,
        niche="Attentional gain",
        governance_role="Task-set maintenance and signal amplification. High = locked-on focus. Low = distractible or broadly sampling.",
        cross_talk={
            "supported_by": "Norepinephrine, Serotonin",
            "opposed_by": "Adenosine, high novelty",
        },
    ),
    NTEAxis.CREATIVITY: NTEAxisGovernance(
        axis=NTEAxis.CREATIVITY,
        niche="Divergent exploration",
        governance_role="Generation of novel candidate structures. High = exploratory recombination. Low = conservative reproduction of known patterns.",
        cross_talk={
            "amplified_by": "Dopamine, Acetylcholine",
            "constrained_by": "GABA, Cortisol",
        },
    ),
    NTEAxis.ANALYSIS_DEPTH: NTEAxisGovernance(
        axis=NTEAxis.ANALYSIS_DEPTH,
        niche="Recursive decomposition",
        governance_role="Depth of recursive reasoning and structural decomposition. High = deep multi-step analysis. Low = shallow/fast processing.",
        cross_talk={
            "supported_by": "Serotonin, Melatonin",
            "disrupted_by": "Epinephrine",
        },
    ),
    NTEAxis.PATTERN_RECOGNITION: NTEAxisGovernance(
        axis=NTEAxis.PATTERN_RECOGNITION,
        niche="Compression/matching",
        governance_role="Matching incoming signals to known compressed structures. High = strong pattern completion. Low = weak generalization.",
        cross_talk={
            "uses": "Acetylcholine, Dopamine",
            "noisy_when": "Glutamate excessively high",
        },
    ),
    NTEAxis.ABSTRACTION_LEVEL: NTEAxisGovernance(
        axis=NTEAxis.ABSTRACTION_LEVEL,
        niche="Distance from concrete data",
        governance_role="Level of abstraction used in representation. High = symbolic/general. Low = concrete/literal.",
        cross_talk={
            "raised_by": "Acetylcholine, Creativity",
            "stabilized_by": "Serotonin",
        },
    ),
    NTEAxis.INFERENCE_SPEED: NTEAxisGovernance(
        axis=NTEAxis.INFERENCE_SPEED,
        niche="Hypothesis evaluation rate",
        governance_role="Rate at which candidate inferences are evaluated. High = fast inference loops. Low = cautious/slow evaluation.",
        cross_talk={
            "boosted_by": "Norepinephrine, Epinephrine",
            "slowed_by": "Adenosine, high load",
        },
    ),
    NTEAxis.UNCERTAINTY_TOLERANCE: NTEAxisGovernance(
        axis=NTEAxis.UNCERTAINTY_TOLERANCE,
        niche="Tolerance of unknown states",
        governance_role="Willingness to continue operating without full evidence. High = robust under ambiguity. Low = demands certainty.",
        cross_talk={
            "buffered_by": "Oxytocin, Serotonin",
            "eroded_by": "Cortisol",
        },
    ),
    NTEAxis.COGNITIVE_FLEXIBILITY: NTEAxisGovernance(
        axis=NTEAxis.COGNITIVE_FLEXIBILITY,
        niche="Set switching",
        governance_role="Ability to switch strategies, frames, or contexts. High = adaptable. Low = perseverative or locked.",
        cross_talk={
            "enabled_by": "Acetylcholine, Norepinephrine",
            "opposed_by": "excessive Focus",
        },
    ),
    NTEAxis.METACOGNITION: NTEAxisGovernance(
        axis=NTEAxis.METACOGNITION,
        niche="Self-modeling",
        governance_role="Monitoring and correcting the system's own reasoning process. High = strong self-review. Low = blind execution.",
        cross_talk={
            "stabilized_by": "Serotonin, GABA",
            "informs": "Dopamine belief updating",
        },
    ),
    NTEAxis.ANALOGICAL_TRANSFER: NTEAxisGovernance(
        axis=NTEAxis.ANALOGICAL_TRANSFER,
        niche="Cross-domain mapping",
        governance_role="Mapping structures from one domain into another. High = strong transfer. Low = domain-bound reasoning.",
        cross_talk={
            "amplified_by": "Dopamine, Acetylcholine",
            "requires": "Pattern recognition + abstraction",
        },
    ),
    NTEAxis.DIALECTICAL_BALANCE: NTEAxisGovernance(
        axis=NTEAxis.DIALECTICAL_BALANCE,
        niche="Opposition management",
        governance_role="Capacity to hold opposing hypotheses without premature collapse. High = stable dialectics. Low = premature certainty.",
        cross_talk={
            "supported_by": "Serotonin, Oxytocin",
            "disrupted_by": "Epinephrine",
        },
    ),
    NTEAxis.INSIGHT_READINESS: NTEAxisGovernance(
        axis=NTEAxis.INSIGHT_READINESS,
        niche="Model-shift readiness",
        governance_role="Readiness to collapse accumulated evidence into a new model. High = near insight. Low = accumulation phase.",
        cross_talk={
            "triggered_by": "Dopamine, Acetylcholine, Melatonin",
            "gated_by": "Metacognition",
        },
    ),
}

# Extend canonical governance to all 24 axes.
NTE_AXES.update(_COGNITIVE_GOVERNANCE)
# === END: CognitiveAxis-24-taxonomy ===


def normalize_nte_state(partial_state: dict) -> dict:
    """
    Ensures any incoming NTE state (8, 12, or 24 axes) is fully populated 
    to the canonical 24-axis model. Missing axes are padded with BASELINE (50.0).
    """
    BASELINE = 50.0
    try:
        full_axes = [a.value if hasattr(a, 'value') else a for a in AXES_24]
    except NameError:
        full_axes = [a.value for a in NTEAxis]
        
    full_state = {axis: BASELINE for axis in full_axes}
    
    if not partial_state:
        return full_state
        
    for k, v in partial_state.items():
        canonical_key = str(k).lower()
        if canonical_key in full_state:
            full_state[canonical_key] = max(0.0, min(100.0, float(v)))
            
    return full_state
