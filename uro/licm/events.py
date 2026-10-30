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


"""V.A.U.R.O.S. LICM Event Ring Buffer."""
from __future__ import annotations
import time
import threading
from collections import deque
from typing import Any, Dict, List

class LicmEventBuffer:
    def __init__(self, maxlen: int = 10000):
        self._buffer: deque = deque(maxlen=maxlen)
        self._seq = 0
        self._lock = threading.Lock()

    def append(self, event_type: str, payload: Dict[str, Any]) -> int:
        with self._lock:
            self._seq += 1
            event = {
                "seq": self._seq,
                "type": event_type,
                "payload": payload,
                "timestamp": time.time()
            }
            self._buffer.append(event)
            return self._seq

    def get_since(self, since_seq: int) -> List[Dict[str, Any]]:
        with self._lock:
            if not self._buffer:
                return []
            start_idx = 0
            for i, ev in enumerate(self._buffer):
                if ev["seq"] > since_seq:
                    start_idx = i
                    break
            else:
                return []
            return list(self._buffer)[start_idx:]

    @property
    def latest_seq(self) -> int:
        with self._lock:
            return self._seq

_dock_buffers: Dict[str, LicmEventBuffer] = {}

def get_event_buffer(dock_id: str) -> LicmEventBuffer:
    if dock_id not in _dock_buffers:
        _dock_buffers[dock_id] = LicmEventBuffer()
    return _dock_buffers[dock_id]
