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
# MODULE START : uro.learning.action_uro
# ---------------------------------------------------------------------
# FILE         : uro/learning/action_uro.py
# PURPOSE      : Action URO types (chain/sequence/serial/parallel) and
#                cumulative costing in time, price, reliability (RFC 92).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"Action URO types and cumulative costing (RFC 92)."

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List

__all__ = ["ActionType", "ActionCost", "ActionURO"]


class ActionType(str, Enum):
    "PURPOSE: RFC 92.1 action composition types."
    CHAIN = "chain"
    SEQUENCE = "sequence"
    SERIAL = "serial"
    PARALLEL = "parallel"


@dataclass
class ActionCost:
    "PURPOSE: Cost triple for one action piece (RFC 92.2)."
    time: float = 0.0
    price: float = 0.0
    reliability: float = 1.0


@dataclass
class ActionURO:
    "PURPOSE: Composable action with cumulative cost roll-up (RFC 92)."
    kind: ActionType
    parts: List["ActionURO"] = field(default_factory=list)
    cost: ActionCost = field(default_factory=ActionCost)

    def total_cost(self) -> ActionCost:
        "PURPOSE: Roll up time/price/reliability from self to final product."
        if not self.parts:
            return ActionCost(self.cost.time, self.cost.price, self.cost.reliability)
        subs = [p.total_cost() for p in self.parts]
        if self.kind == ActionType.PARALLEL:
            base = max(s.time for s in subs)
        else:
            base = sum(s.time for s in subs)
        price = self.cost.price + sum(s.price for s in subs)
        rel = self.cost.reliability
        for s in subs:
            rel *= s.reliability
        return ActionCost(base + self.cost.time, price, rel)
# =====================================================================
# MODULE END   : uro.learning.action_uro
# =====================================================================
