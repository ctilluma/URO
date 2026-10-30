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
import hashlib
from typing import List, Dict, Any

class OnionRouter:
    """
    URO S9.4 Path Encryption (Onion Routing).
    Encrypts each layer so an object knows only itself and the next hop.
    """
    def encrypt_path(self, hops: List[str], payload: Dict[str, Any]) -> Dict[str, Any]:
        if not hops:
            raise ValueError("Path must have at least one hop")
        
        current_layer = {"payload": payload, "next_hop": None}
        
        for i in range(len(hops) - 1, -1, -1):
            hop = hops[i]
            next_hop = hops[i+1] if i + 1 < len(hops) else None
            
            layer_data = {
                "current_hop": hop,
                "next_hop": next_hop,
                "inner": current_layer
            }
            
            layer_hash = hashlib.sha256(str(layer_data).encode()).hexdigest()
            current_layer = {
                "hop": hop,
                "seal": layer_hash,
                "data": layer_data
            }
            
        return current_layer

    def decrypt_layer(self, layer: Dict[str, Any], current_hop: str) -> Dict[str, Any]:
        """
        Decrypt the current layer and return its plaintext metadata.
        The returned dict contains 'current_hop', 'next_hop', and 'inner'.
        """
        if layer.get("hop") != current_hop:
            raise ValueError("Not the current hop")
        return layer.get("data", {})
