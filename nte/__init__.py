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


from uro.nte.normalizer import (
    BASELINE, CANONICAL_24_AXES, BIOLOGICAL_AXES, COGNITIVE_AXES,
    normalize_nte_state, apply_cross_talk, decay_state, clamp_state, nte_vector,
)
__all__ = ["BASELINE","CANONICAL_24_AXES","BIOLOGICAL_AXES","COGNITIVE_AXES",
           "normalize_nte_state","apply_cross_talk","decay_state","clamp_state","nte_vector"]
