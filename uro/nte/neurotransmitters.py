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
# MODULE START : uro.nte.neurotransmitters
# ---------------------------------------------------------------------
# FILE         : uro/nte/neurotransmitters.py
# PURPOSE      : Neurotransmitter Equivalences (NTE) and the synapse
#                firing model (non-binary decision).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"""Neurotransmitter Equivalences and synapse firing model."""

from __future__ import annotations

import random as _random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict

from uro.nte.axes import NTEAxis

__all__ = ["NTE", "NTEState", "Receptor", "Synapse"]


# Deprecated 10-member fork removed per ADR-011/ADR-012.
# Canonical taxonomy is the 24-axis NTEAxis; NTE remains as its alias.
NTE = NTEAxis


@dataclass
class NTEState:
    def __init__(self, levels=None, **kwargs):
        """Accept kwargs like epinephrine=0.5, dopamine=0.5 for dock compatibility."""
        if levels is None:
            levels = {n: 0.5 for n in NTE}
        self.levels = levels
        for k, v in kwargs.items():
            try:
                nte = NTE[k.upper()]
                self.levels[nte] = float(v)
            except (KeyError, AttributeError):
                pass  # silently ignore unknown kwargs

    """Holds current levels for each NTE. Accepts flexible kwargs for dock compatibility."""
    levels: Dict[NTE, float] = field(
        default_factory=lambda: {n: 0.5 for n in NTE})

    def __post_init__(self):
        # Already initialized via field(default_factory)
        pass

    @classmethod
    def initialize(cls, **kwargs) -> "NTEState":
        """Factory for dock compatibility: NTEState(epinephrine=0.5, dopamine=0.5, ...)"""
        inst = cls()
        for k, v in kwargs.items():
            try:
                nte = NTE[k.upper()]
                inst.levels[nte] = float(v)
            except (KeyError, AttributeError):
                pass  # silently ignore unknown kwargs
        return inst

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    def to_canonical(self) -> dict:
        "PURPOSE: Bridge legacy [0,1] levels to canonical 24-axis [0,100] state (ADR-012)."
        return {a.value: max(0.0, min(100.0, self.levels.get(a, 0.5) * 100.0)) for a in NTEAxis}

    @classmethod
    def from_canonical(cls, levels: dict) -> "NTEState":
        "PURPOSE: Build a legacy view from a canonical 24-axis [0,100] state (ADR-012)."
        inst = cls()
        for axis in NTEAxis:
            inst.levels[axis] = max(0.0, min(1.0, float(levels.get(axis.value, 50.0)) / 100.0))
        return inst

    def set(self, nte: NTE, value: float) -> None:
        """Set the level of an NTE."""
        self.levels[nte] = value

    def get(self, nte: NTE) -> float:
        """Return the level of an NTE."""
        return self.levels.get(nte, 0.0)


@dataclass
class Receptor:
    """A receptor that binds protagonist and antagonist signals."""
    receptor_count: int = 10
    potentiators: float = 0.0
    antagonists: float = 0.0

    def activity_ratio(self) -> float:
        """Compute the activation ratio per the NTE firing model."""
        total = self.potentiators + self.antagonists
        if total <= 0 or self.receptor_count <= 0:
            return 0.0
        p_fraction = self.potentiators / total
        if self.potentiators > self.receptor_count:
            r_p = _random.random() * self.receptor_count * p_fraction
        else:
            r_p = self.potentiators
        return min(1.0, (2.0 * r_p) / self.receptor_count)


class Synapse:
    """A junction that decides (non-binary) whether to transmit."""

    def __init__(self, receptor: Receptor, nte: NTEState | None = None) -> None:
        """Create a synapse."""
        self.receptor = receptor
        self.nte = nte or NTEState()

    def fire(self) -> bool:
        """Decide whether the synapse fires."""
        ratio = self.receptor.activity_ratio()
        gaba = self.nte.get(NTE.GABA)
        dopamine = self.nte.get(NTE.DOPAMINE)
        adjusted = ratio * (1.0 - max(0.0, gaba)) * (1.0 + max(0.0, dopamine))
        return _random.random() <= min(1.0, max(0.0, adjusted))
# =====================================================================
# MODULE END   : uro.nte.neurotransmitters
# =====================================================================
