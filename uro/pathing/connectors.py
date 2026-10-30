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
from enum import Enum
from typing import Dict, Any

class ConnectorType(str, Enum):
    OUTPUT = "OUTPUT"       # 0|URO OTHER
    INPUT = "INPUT"         # URO OTHER|0
    LINK = "LINK"           # URO SELF|URO OTHER
    CHILD = "CHILD"         # URO OTHER|URO SELF
    PATH = "PATH"           # URO OTHER1|URO OTHER2

class Connector:
    """
    URO S9.8 Connectors.
    Defines the directional relationship between UROs.
    """
    def __init__(self, connector_type: ConnectorType, source: str, target: str = None):
        self.type = connector_type
        self.source = source
        self.target = target

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "source": self.source,
            "target": self.target
        }

    @classmethod
    def from_urid_pair(cls, urid1: str, urid2: str, self_urid: str = None) -> "Connector":
        "PURPOSE: Classify per RFC 80 matrix; self_urid disambiguates SELF vs OTHER."
        if urid1 == "0" and urid2 != "0":
            return cls(ConnectorType.OUTPUT, urid2)
        elif urid1 != "0" and urid2 == "0":
            return cls(ConnectorType.INPUT, urid1)
        elif self_urid is not None:
            if urid1 == self_urid and urid2 != self_urid:
                return cls(ConnectorType.LINK, urid1, urid2)
            if urid1 != self_urid and urid2 == self_urid:
                return cls(ConnectorType.CHILD, urid1, urid2)
            return cls(ConnectorType.PATH, urid1, urid2)
        elif urid1 == urid2:
            return cls(ConnectorType.LINK, urid1)
        else:
            return cls(ConnectorType.PATH, urid1, urid2)
