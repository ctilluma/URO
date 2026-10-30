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

from uro.core.urid import URID
from typing import Any, Dict

def make_urid_pair(source: Any, identifier: Any) -> Dict[str, Any]:
    """
    S2 URID pair using canonical URID.
    URID1 = source/template/origin.
    URID2 = identifier inside that source.
    """
    # Generate canonical URIDs
    urid1 = URID.generate(seed=str(source))
    urid2 = URID.generate(seed=str(identifier))
    
    return {
        "urid1": urid1,
        "urid2": urid2,
        "urid1_hex": urid1.to_hex(),
        "urid2_hex": urid2.to_hex(),
    }
