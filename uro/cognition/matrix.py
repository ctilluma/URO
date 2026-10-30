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
MODULE: Fuzzy Matrix URO (the decision brain)
INTENT: A URO that maps parallel input rates to a distribution over outcomes
        via fuzzy prototype similarity, and tracks verdict dynamics.
        The matrix itself is a URO (lineage, NTE, custody) so it can be
        registered, evolved, audited, and sold in the marketplace.
STANDARD: URO-STD-0001 S25
"""
from __future__ import annotations
from typing import Dict
from pydantic import BaseModel, Field, ConfigDict

from uro.core.urid import URID
from uro.security.hashing import inahash
from uro.cognition.fuzzy import gauss_close, fuzzy_and, normalize
from uro.cognition.verdict import VerdictDynamics

__all__ = ["FuzzyMatrixURO", "OUTCOME_SPACE", "DEFAULT_PROTOTYPES"]

# The outcome space for the outlier/novelty decision
OUTCOME_SPACE = [
    "malicious", "novel_unverified", "novel_verified", "corrupt", "irrelevant"
]

# Ideal input prototypes per outcome (values 0-100). All inputs feed in parallel.
DEFAULT_PROTOTYPES: Dict[str, Dict[str, float]] = {
    "malicious":        {"chain_trust": 10, "coherence": 20, "provenance": 20, "hist_novelty": 30, "sandbox": 10, "cross": 20},
    "novel_unverified": {"chain_trust": 40, "coherence": 70, "provenance": 40, "hist_novelty": 70, "sandbox": 40, "cross": 50},
    "novel_verified":   {"chain_trust": 80, "coherence": 85, "provenance": 70, "hist_novelty": 80, "sandbox": 85, "cross": 75},
    "corrupt":          {"chain_trust": 70, "coherence": 15, "provenance": 60, "hist_novelty": 30, "sandbox": 20, "cross": 30},
    "irrelevant":       {"chain_trust": 50, "coherence": 50, "provenance": 50, "hist_novelty": 20, "sandbox": 50, "cross": 30},
}


class FuzzyMatrixURO(BaseModel):
    """A fuzzy decision matrix, itself a first-class URO."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    urid1: URID = Field(...)
    urid2: URID = Field(...)

    prototypes: Dict[str, Dict[str, float]] = Field(default_factory=lambda: dict(DEFAULT_PROTOTYPES))
    sigma: float = Field(25.0, description="Gaussian width for fuzzy closeness")

    # The living verdict (distribution + dynamics)
    verdict: VerdictDynamics = Field(...)

    inahash: str = Field(default="")

    def evaluate(self, inputs: Dict[str, float], agg: str = "geometric",
                 strict_outcomes=None) -> Dict[str, float]:
        """
        Map parallel input rates to a distribution over outcomes.

        Each outcome's strength = fuzzy similarity of the input vector to that
        outcome's prototype (all inputs contribute in parallel).

        agg: "geometric" (strict conjunction, default - preserves prior
             behavior) or "arithmetic" (softer, additive contribution).
        strict_outcomes: outcomes that ALWAYS use geometric conjunction
             (e.g. 'prune' - every sign must agree before we delete).
        """
        strict_outcomes = strict_outcomes or set()
        weights = {}
        for outcome, proto in self.prototypes.items():
            degrees = []
            for inp, ideal in proto.items():
                actual = inputs.get(inp, 50.0)
                degrees.append(gauss_close(actual, ideal, self.sigma))
            mode = "geometric" if (outcome in strict_outcomes or agg == "geometric") else "arithmetic"
            weights[outcome] = self._aggregate(degrees, mode)
        dist = normalize(weights)
        self.verdict.update(dist)
        self.seal()
        return dist

    @staticmethod
    def _aggregate(degrees, mode: str) -> float:
        if not degrees:
            return 0.0
        if mode == "arithmetic":
            return sum(degrees) / len(degrees)
        return fuzzy_and(degrees)

    def seal(self) -> None:
        data = self.model_dump(exclude={"inahash"})
        self.inahash = inahash(str(data).encode()).hex()

    @classmethod
    def new(cls) -> "FuzzyMatrixURO":
        u = URID.new()
        return cls(
            urid1=u, urid2=u,
            verdict=VerdictDynamics(urid1=u, urid2=URID.new()),
        )
