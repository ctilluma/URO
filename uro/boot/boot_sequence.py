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
# MODULE START : uro.boot.boot_sequence
# ---------------------------------------------------------------------
# FILE         : uro/boot/boot_sequence.py
# PURPOSE      : The 16-step full boot sequence with ordered execution
#                and halt-on-failure semantics (RFC 107).
# STANDARD     : URO-STD-0001 S12
# =====================================================================
"The 16-step full boot sequence (RFC 107)."

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Tuple

__all__ = ["BOOT_STEPS", "BootContext", "BootRunner"]

BOOT_STEPS: Tuple[str, ...] = (
    "loader_verify", "kernel_decrypt_verify", "memory_init",
    "core_uros_load", "security_init", "nte_baseline", "coordinator_online",
    "dock_registry_load", "docks_boot", "pathing_restore", "synapse_restore",
    "personality_load", "learning_online", "economy_connect",
    "beacon_broadcast", "system_ready",
)


@dataclass
class BootContext:
    "PURPOSE: Mutable artifacts and flags shared across boot steps."
    artifacts: Dict[str, Any] = field(default_factory=dict)
    flags: Dict[str, bool] = field(default_factory=dict)


class BootRunner:
    "PURPOSE: Execute the 16 steps in order; halt on first False handler."

    def __init__(self, handlers: Dict[str, Callable[[BootContext], bool]] = None) -> None:
        self.handlers = handlers or {}
        self.context = BootContext()
        self.completed: List[str] = []

    def run(self) -> Dict[str, Any]:
        "PURPOSE: Run all steps; READY on completion, HALTED on first failure."
        for step in BOOT_STEPS:
            handler = self.handlers.get(step)
            ok = True if handler is None else bool(handler(self.context))
            if not ok:
                return {"status": "HALTED", "step": step,
                        "completed": tuple(self.completed)}
            self.completed.append(step)
        return {"status": "READY", "completed": tuple(self.completed)}

    @staticmethod
    def step_index(name: str) -> int:
        "PURPOSE: Position of a step within the canonical sequence."
        return BOOT_STEPS.index(name)
# =====================================================================
# MODULE END   : uro.boot.boot_sequence
# =====================================================================
