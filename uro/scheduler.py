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
# MODULE START : uro.scheduler
# ---------------------------------------------------------------------
# FILE         : uro/scheduler.py
# PURPOSE      : The Adaptive OPAR Scheduler. Runs many URO lifecycles
#                concurrently and adapts the wait time between iterations
#                based on the level of input/requested output, per the
#                standard: "an object raises and lowers wait times
#                between iterations based on level of input or requested
#                output. Always on vs. one off."
#
#                - More queued input  -> shorter wait (spin faster).
#                - Less queued input  -> longer wait  (conserve cycles).
#                - always_on objects keep running; one-off objects run
#                  only when explicitly invoked.
# STANDARD     : URO-STD-0001 S8 (OPAR), S10 (Adaptive Pacing)
# =====================================================================
"""Adaptive, asynchronous OPAR scheduler for many UROs."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from uro.core.uro import URO
from uro.exceptions import SchedulerError
from uro.phases.opar import OPARCycle

__all__ = ["ScheduledURO", "AdaptiveScheduler"]


@dataclass
class ScheduledURO:
    """A scheduling entry binding a URO to its OPAR cycle and cadence.

    Attributes:
        uro: The URO being scheduled.
        cycle: The OPAR cycle driving the URO.
        base_interval: The nominal seconds between iterations.
        always_on: If True, keeps running; if False, one-off.
        iterations: Count of completed cycles.
    """
    uro: URO
    cycle: OPARCycle
    base_interval: float = 0.05
    always_on: bool = True
    iterations: int = 0


class AdaptiveScheduler:
    """Runs many OPAR cycles concurrently with adaptive pacing.

    The scheduler maintains one :class:`ScheduledURO` per registered URO
    and executes their OPAR cycles concurrently using asyncio. The wait
    between iterations adapts to the current input-queue depth so busy
    UROs spin faster and idle UROs conserve cycles.
    """

    def __init__(self) -> None:
        """Create an empty scheduler."""
        self._entries: Dict[int, ScheduledURO] = {}
        self._stop = asyncio.Event()

    # -- Registration --------------------------------------------------
    def register(self, uro: URO, base_interval: float = 0.05,
                 always_on: bool = True) -> OPARCycle:
        """Register a URO for scheduling.

        Args:
            uro: The URO to schedule.
            base_interval: Nominal seconds between iterations.
            always_on: Whether the URO runs continuously.

        Returns:
            OPARCycle: The cycle bound to the URO.

        Raises:
            SchedulerError: If the URO is already registered.
        """
        if id(uro) in self._entries:
            raise SchedulerError("URO already registered with scheduler")
        cycle = OPARCycle(uro)
        self._entries[id(uro)] = ScheduledURO(
            uro=uro, cycle=cycle, base_interval=base_interval,
            always_on=always_on,
        )
        return cycle

    def entry(self, uro: URO) -> ScheduledURO:
        """Return the ScheduledURO for a registered URO.

        Args:
            uro: The registered URO.

        Returns:
            ScheduledURO: The scheduling entry.

        Raises:
            SchedulerError: If the URO is not registered.
        """
        e = self._entries.get(id(uro))
        if e is None:
            raise SchedulerError("URO not registered with scheduler")
        return e

    # -- Stimulus ------------------------------------------------------
    def feed(self, uro: URO, stimulus: Any) -> None:
        """Enqueue an external stimulus for a registered URO.

        Args:
            uro: The target URO.
            stimulus: The stimulus to observe on the next cycle.
        """
        self.entry(uro).cycle.enqueue(stimulus)

    # -- Adaptive pacing ----------------------------------------------
    def adaptive_interval(self, entry: ScheduledURO) -> float:
        """Compute the next wait based on queue depth.

        More queued input shortens the wait; an empty queue lengthens it
        (up to 4x base). Clamped to a sane minimum.

        Args:
            entry: The scheduling entry.

        Returns:
            float: Seconds to wait before the next iteration.
        """
        depth = len(entry.cycle.input_queue)
        interval = entry.base_interval / (1.0 + depth)
        upper = entry.base_interval * 4.0
        return max(0.0005, min(interval, upper))

    # -- Execution -----------------------------------------------------
    async def _run_entry(self, entry: ScheduledURO, steps: int) -> None:
        """Run one entry for a fixed number of steps.

        Args:
            entry: The scheduling entry.
            steps: Number of OPAR cycles to run.
        """
        for _ in range(steps):
            if self._stop.is_set():
                break
            entry.cycle.run(1)
            entry.iterations += 1
            await asyncio.sleep(self.adaptive_interval(entry))

    async def run(self, steps: int = 3) -> Dict[int, int]:
        """Run every always-on URO for a number of steps concurrently.

        Args:
            steps: Number of OPAR cycles per URO.

        Returns:
            Dict[int, int]: Mapping of URO id to iterations completed.
        """
        self._stop.clear()
        targets = [e for e in self._entries.values() if e.always_on]
        await asyncio.gather(*(self._run_entry(e, steps) for e in targets))
        return {id(e.uro): e.iterations for e in targets}

    def stop(self) -> None:
        """Signal all running loops to stop."""
        self._stop.set()
# =====================================================================
# MODULE END   : uro.scheduler
# =====================================================================
