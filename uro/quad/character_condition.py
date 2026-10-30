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
# MODULE START : uro.quad.character_condition
# ---------------------------------------------------------------------
# FILE         : uro/quad/character_condition.py
# PURPOSE      : Character vs Condition equilibrium math (RFC 46):
#                returns within 1 SD leave character untouched; sustained
#                large deviations drift character toward the condition.
# STANDARD     : URO-STD-0001 S-Quad
# =====================================================================
"Character vs Condition equilibrium math (RFC 46)."

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

__all__ = ["CharacterCondition", "SD_UNIT"]

# Documented convention: one standard deviation equals 10 trait points.
SD_UNIT = 10.0


@dataclass
class CharacterCondition:
    "PURPOSE: Near-fixed character equilibrium plus immediate condition (RFC 46)."
    character: Dict[str, float] = field(default_factory=dict)
    condition: Dict[str, float] = field(default_factory=dict)

    def set_condition(self, trait: str, value: float) -> None:
        "PURPOSE: Record the immediate state of one trait."
        self.condition[trait] = max(0.0, min(100.0, float(value)))

    def deviation_sd(self, trait: str) -> float:
        "PURPOSE: Condition deviation from character in SD units."
        base = self.character.get(trait, 50.0)
        return (self.condition.get(trait, base) - base) / SD_UNIT

    def apply_period(self, trait: str, sustained_periods: int = 1,
                     drift_rate: float = 0.01) -> float:
        "PURPOSE: RFC 46.1/46.2 drift rule; bounded, monotonic toward condition."
        dev = self.deviation_sd(trait)
        base = self.character.get(trait, 50.0)
        if abs(dev) <= 1.0:
            return base
        excess = dev - (1.0 if dev > 0 else -1.0)
        drift = drift_rate * excess * max(1, sustained_periods) * SD_UNIT
        new = max(0.0, min(100.0, base + drift))
        cond = self.condition.get(trait, base)
        new = min(new, cond) if base <= cond else max(new, cond)
        self.character[trait] = new
        return new

    def equilibrium(self) -> Dict[str, float]:
        "PURPOSE: The near-fixed character levels the object returns to."
        return dict(self.character)
# =====================================================================
# MODULE END   : uro.quad.character_condition
# =====================================================================
