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
from typing import List, Dict, Any

class BeaconType(str, Enum):
    I_EXIST = "I_EXIST"
    SO_DO_I = "SO_DO_I"
    I_DO_THIS = "I_DO_THIS"
    BUSY_SLOW = "BUSY_SLOW"
    WORKS_WITH = "WORKS_WITH"
    LOOKING_FOR = "LOOKING_FOR"

# RFC 74.1 parent discovery sequence (name, payload pattern).
PARENT_SEQUENCE = (("accepted_natural", "0 0 CRO"), ("processable", "CRO 0 0"), ("understood", "CRO CRO"))
# RFC 74.2 child sequence.
CHILD_SEQUENCE = ("native", "processable", "understood", "request_beacon_response")
# RFC 74.3 interface sequence order.
INTERFACE_SEQUENCE = (BeaconType.I_EXIST, BeaconType.SO_DO_I, BeaconType.I_DO_THIS, BeaconType.BUSY_SLOW, BeaconType.WORKS_WITH, BeaconType.LOOKING_FOR)


class BeaconManager:
    """
    URO S9.7 Beacons.
    Manages discovery and capability advertisement between UROs.
    """
    def __init__(self):
        self.registry: Dict[str, List[Dict[str, Any]]] = {}

    def broadcast(self, sender: str, beacon_type: BeaconType, payload: Dict[str, Any] = None):
        if sender not in self.registry:
            self.registry[sender] = []
        
        self.registry[sender].append({
            "type": beacon_type.value,
            "payload": payload or {},
            "sender": sender
        })
        return {"status": "broadcasted", "type": beacon_type.value}

    def get_beacons(self, beacon_type: BeaconType = None) -> List[Dict[str, Any]]:
        all_beacons = []
        for beacons in self.registry.values():
            all_beacons.extend(beacons)
        
        if beacon_type:
            return [b for b in all_beacons if b["type"] == beacon_type.value]
        return all_beacons
