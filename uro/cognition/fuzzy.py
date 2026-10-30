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
MODULE: Fuzzy Primitives
INTENT: Membership functions and fuzzy aggregation for the neuro-fuzzy matrix.
        Custom integration: Gaussian prototypes + linguistic terms, so all
        inputs feed rates in parallel (no sequential branching).
STANDARD: URO-STD-0001 S23
"""
from __future__ import annotations
import math
from typing import Dict, List

__all__ = ["trimf", "gauss_close", "fuzzy_and", "normalize", "linguistic"]


def trimf(x: float, a: float, b: float, c: float) -> float:
    """Triangular membership (LOW/MED/HIGH style linguistic terms)."""
    if x <= a or x >= c:
        return 0.0
    if x <= b:
        return (x - a) / (b - a) if b > a else 1.0
    return (c - x) / (c - b) if c > b else 1.0


def gauss_close(x: float, prototype: float, sigma: float = 25.0) -> float:
    """Fuzzy 'closeness' of a crisp value to a prototype (Gaussian)."""
    return math.exp(-(((x - prototype) / sigma) ** 2))


def linguistic(x: float) -> Dict[str, float]:
    """Map a crisp 0-100 value to LOW/MED/HIGH membership degrees."""
    return {
        "LOW": trimf(x, 0.0, 0.0, 50.0),
        "MED": trimf(x, 25.0, 50.0, 75.0),
        "HIGH": trimf(x, 50.0, 100.0, 100.0),
    }


def fuzzy_and(degrees: List[float]) -> float:
    """Fuzzy AND across a set of membership degrees (geometric mean)."""
    if not degrees:
        return 0.0
    prod = 1.0
    for d in degrees:
        prod *= max(d, 1e-9)
    return prod ** (1.0 / len(degrees))


def normalize(weights: Dict[str, float]) -> Dict[str, float]:
    """Normalize a weight dict into a probability distribution."""
    total = sum(weights.values())
    if total <= 0:
        n = len(weights) or 1
        return {k: 1.0 / n for k in weights}
    return {k: v / total for k, v in weights.items()}
