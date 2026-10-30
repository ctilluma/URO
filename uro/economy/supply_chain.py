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
# MODULE START : uro.economy.supply_chain
# ---------------------------------------------------------------------
# FILE         : uro/economy/supply_chain.py
# PURPOSE      : Supply chain ledger: track cost accumulation through
#                production stages (RFC 112).
# STANDARD     : URO-STD-0001 S35
# =====================================================================
"Supply chain cost tracking (RFC 112)."

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

__all__ = ["SupplyChainStage", "SupplyChainLedger"]


@dataclass
class SupplyChainStage:
    "PURPOSE: One production stage with cost and value-add."
    stage_id: str
    cost: float
    value_add: float = 0.0
    notes: str = ""


@dataclass
class SupplyChainLedger:
    "PURPOSE: Track cumulative cost through production stages."
    stages: List[SupplyChainStage] = field(default_factory=list)

    def add_stage(self, stage: SupplyChainStage) -> None:
        "PURPOSE: Append a production stage."
        self.stages.append(stage)

    def total_cost(self) -> float:
        "PURPOSE: Sum of all stage costs."
        return sum(s.cost for s in self.stages)

    def total_value_add(self) -> float:
        "PURPOSE: Sum of all value-add components."
        return sum(s.value_add for s in self.stages)

    def final_price(self, margin: float = 0.2) -> float:
        "PURPOSE: Cost plus margin."
        return self.total_cost() * (1.0 + margin)
# =====================================================================
# MODULE END   : uro.economy.supply_chain
# =====================================================================
