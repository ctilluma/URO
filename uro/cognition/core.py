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
MODULE: Cognitive Core (the cumulative learner)
INTENT: The LEAST stateless object in the swarm. Tracks every request, every
        input vector, every strategy chosen, and every outcome; uses that
        experience to increasingly override its fuzzy priors. Becomes more
        intelligent with each passing request.
STANDARD: URO-STD-0001 S29

LEARNING MODEL:
  final(strategy) = fuzzy_prior * (1-w_p) + learned_prior * w_p
  where w_p = experience/(experience + k).  As experience grows, learned
  intelligence dominates the static prototype prior.

  * observe()          -> choose a strategy (fuzzy + learned + NTE exploration)
  * record_outcome()   -> reward-gated Hebbian prototype update + dopamine RPE
  * recall_similar()   -> content-addressed retrieval of past experience
  * snapshot()/restore -> persist the whole learned state as UROs
"""
from __future__ import annotations

import time
import uuid
import random
from typing import Any, Dict, List, Optional, Tuple

from uro.cognition.cognitive_fuzzy import new_cognitive_matrix, cognitive_inputs
from uro.cognition.fuzzy import gauss_close, fuzzy_and, normalize
from uro.nte.state import NTEStateURO
from uro.nte.axes import NTEAxis
from uro.core.urid import URID

__all__ = ["CognitiveCore"]


class CognitiveCore:
    """Stateful, cumulative cognitive learner."""

    def __init__(self, dock_name: str = "cognitive", k: float = 5.0):
        self.dock_name = dock_name
        self.k = k                      # experience half-saturation
        self.matrix = new_cognitive_matrix()
        self.nte = NTEStateURO(urid1=URID.new(), urid2=URID.new())
        self.episodes: List[Dict[str, Any]] = []   # every request ever seen
        self.by_id: Dict[str, Dict[str, Any]] = {}
        self.vectors: List[Dict[str, float]] = []  # every input vector

    # ── experience-weighted learned prior ───────────────────────────────────
    def _prior(self, inputs: Dict[str, float]) -> Tuple[Dict[str, float], float]:
        agg: Dict[str, List[float]] = {}
        total = 0.0
        n = len(self.episodes)
        for ep in self.episodes:
            if ep["reward"] is None:
                continue
            # content-addressed similarity to this context
            degrees = [gauss_close(inputs[kk], ep["inputs"].get(kk, 50.0), 25.0)
                       for kk in inputs]
            sim = fuzzy_and(degrees)
            recency = 1.0 / (1.0 + (n - ep["idx"]))
            w = sim * recency
            if w <= 1e-6:
                continue
            a = agg.setdefault(ep["chosen"], [0.0, 0.0])
            a[0] += w
            a[1] += w * ep["reward"]
            total += w
        prior = {s: (v[1] / v[0]) if v[0] > 1e-6 else 0.5 for s, v in agg.items()}
        return prior, total

    # ── observe: choose a strategy ──────────────────────────────────────────
    def observe(self, inputs: Dict[str, float], explore: bool = True) \
            -> Tuple[str, str, Dict[str, float], float]:
        fuzzy = self.matrix.evaluate(inputs)          # fuzzy prior + dynamics
        prior, exp = self._prior(inputs)
        w_p = exp / (exp + self.k)                    # learned weight grows

        final = normalize({
            kk: fuzzy.get(kk, 0.0) * (1 - w_p) + prior.get(kk, 0.5) * w_p
            for kk in fuzzy
        })

        top = max(final, key=final.get)

        # NTE-modulated exploration (plasticity opens exploration)
        chosen = top
        if explore:
            rate = (self.nte.get_level(NTEAxis.ACETYLCHOLINE) / 100.0) * 0.3
            if random.random() < rate:
                chosen = random.choices(list(final), weights=list(final.values()))[0]

        rid = uuid.uuid4().hex
        ep = {"id": rid, "idx": len(self.episodes), "inputs": dict(inputs),
              "chosen": chosen, "reward": None, "prior_prob": final[chosen],
              "time": time.time()}
        self.episodes.append(ep)
        self.by_id[rid] = ep
        self.vectors.append(dict(inputs))
        return rid, chosen, final, w_p

    # ── record_outcome: the learning step ───────────────────────────────────
    def record_outcome(self, rid: str, reward: float) -> None:
        ep = self.by_id.get(rid)
        if ep is None:
            return
        ep["reward"] = max(0.0, min(1.0, reward))

        # Reward-gated Hebbian prototype update: move the chosen strategy's
        # prototype toward contexts that succeeded, away from those that failed.
        lr = 0.1 * (self.nte.get_level(NTEAxis.ACETYLCHOLINE) / 100.0 + 0.2)
        proto = self.matrix.prototypes.get(ep["chosen"])
        if proto:
            gate = ep["reward"] - 0.5
            for key, val in ep["inputs"].items():
                if key in proto:
                    proto[key] += lr * gate * (val - proto[key])
                    proto[key] = max(0.0, min(100.0, proto[key]))

        # Dopamine reward-prediction-error
        rpe = ep["reward"] - ep["prior_prob"]
        self.nte.apply_delta(NTEAxis.DOPAMINE, rpe * 20.0)
        self.matrix.seal()

    # ── content-addressed recall ────────────────────────────────────────────
    def recall_similar(self, inputs: Dict[str, float], topn: int = 3) -> List[Dict]:
        scored = []
        for ep in self.episodes:
            degrees = [gauss_close(inputs[kk], ep["inputs"].get(kk, 50.0), 25.0)
                       for kk in inputs]
            scored.append((fuzzy_and(degrees), ep))
        scored.sort(key=lambda t: -t[0])
        return [{"sim": s, "chosen": e["chosen"], "reward": e["reward"]}
                for s, e in scored[:topn]]

    # ── persistence as UROs ─────────────────────────────────────────────────
    def snapshot(self) -> Dict[str, Any]:
        return {
            "dock": self.dock_name,
            "episodes": self.episodes,
            "prototypes": self.matrix.prototypes,
            "nte": {ax.value: self.nte.get_level(ax) for ax in NTEAxis},
        }

    def intelligence(self) -> float:
        """How much learned experience currently dominates the prior (w_p)."""
        _, exp = self._prior({k: 50.0 for k in
                              next(iter(self.matrix.prototypes.values()))})
        return exp / (exp + self.k)
