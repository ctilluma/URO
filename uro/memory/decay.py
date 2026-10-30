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


from __future__ import annotations
import time

def apply_cognitive_decay(original_conf: float, age_in_hours: float) -> float:
    """
    URO S8.5 Cognitive Decay (Confidence Depreciation).
    Beliefs in memory undergo exponential decay based on age:
    decayed_conf = original_conf * (0.95 ^ age_in_hours)
    """
    if age_in_hours < 0:
        age_in_hours = 0.0
    return original_conf * (0.95 ** age_in_hours)

def hours_since(timestamp: float) -> float:
    return max(0.0, (time.time() - timestamp) / 3600.0)
