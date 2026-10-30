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


"""V.A.U.R.O.S. Belief Engine - Bayesian posterior + trust-dominant evidence scoring.

Design laws (epistemic immune system):
- Belief is a distribution (beta posterior), never a point estimate.
- Repetition within a single origin is NOT evidence (hard saturation).
- Trust dominates: max-origin-trust gates support; a flood of low-trust sources
  can never outrank a single high-trust counter-statement.
- Diversity only amplifies trust you already have (bonus scaled by max_trust),
  so low-trust floods stay low while high-trust corroboration compounds.
- Origins below TRUST_FLOOR contribute nothing (genesis-trust gate).
- Absence of evidence is ignorance, not disproof (callers keep uniform priors).
"""
import math

TRUST_FLOOR = 0.2
DEFAULT_PRIOR = (1.0, 1.0)  # Beta(1,1) = uniform ignorance


def beta_posterior(alpha, beta):
    """Return (mean, variance) of Beta(alpha, beta)."""
    a, b = float(alpha), float(beta)
    mean = a / (a + b)
    var = (a * b) / (((a + b) ** 2) * (a + b + 1.0))
    return mean, var


def beta_update(alpha, beta, confirm_weight=0.0, counter_weight=0.0):
    """Conjugate update: trust-weighted confirmations add to alpha,
    trust-weighted counter-evidence adds to beta."""
    return alpha + max(0.0, confirm_weight), beta + max(0.0, counter_weight)


def trust_dominant_support(evidence, verification=1.0):
    """Score a body of evidence. evidence: iterable of (origin, trust, count)
    or dict origin -> (trust, count).

    Rules:
      - per-origin repetition saturates (count>=1 treated as count==1)
      - origins below TRUST_FLOOR are ignored entirely
      - support = max_trust * (1 + max_trust * log10(1 + qualifying_diversity))
        * verification
    Diversity is scaled by max_trust so low-trust floods cannot compound.
    """
    if isinstance(evidence, dict):
        items = [(o, t, c) for o, (t, c) in evidence.items()]
    else:
        items = [(o, t, c) for (o, t, c) in evidence]
    qualifying = [t for (_o, t, c) in items if c >= 1 and t >= TRUST_FLOOR]
    if not qualifying:
        return 0.0
    max_trust = max(qualifying)
    diversity = len(qualifying)
    return max_trust * (1.0 + max_trust * math.log10(1.0 + diversity)) * verification


def flood_vs_counter(flood_trust, flood_origins, counter_trust, verification=1.0):
    """Compare a flood (many distinct low-trust origins, one mention each)
    against a single high-trust counter-statement.
    Returns (flood_support, counter_support)."""
    flood = [(f"low_{i}", flood_trust, 1) for i in range(flood_origins)]
    counter = [("high_trust_origin", counter_trust, 1)]
    return (trust_dominant_support(flood, verification),
            trust_dominant_support(counter, verification))
