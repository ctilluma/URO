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


from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable

class LICMProvider(ABC):
    def __init__(self, dock_id: str):
        self.dock_id = dock_id
    """Abstract base class for dock LICM integration."""
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Return current dock status with provenance-badged metrics."""
        pass
    
    @abstractmethod
    def get_events(self, since_seq: int = 0, limit: int = 50) -> Dict[str, Any]:
        """Return event stream for this dock."""
        pass
    
    def get_nte_state(self) -> Dict[str, float]:
        """Return 24-axis NTE state (optional, defaults to neutral)."""
        return {}

class SimpleLICMProvider(LICMProvider):
    """Concrete LICM provider that accepts callable functions for quick scaffolding."""
    
    def __init__(
        self,
        dock_id: str,
        status_fn: Callable[[], Dict[str, Any]],
        events_fn: Optional[Callable[[int, int], Dict[str, Any]]] = None,
        nte_fn: Optional[Callable[[], Dict[str, float]]] = None
    ):
        self.dock_id = dock_id
        self._status_fn = status_fn
        self._events_fn = events_fn or (lambda seq=0, limit=50: {"events": [], "total_count": 0, "has_more": False})
        self._nte_fn = nte_fn or (lambda: {})
    
    def get_status(self) -> Dict[str, Any]:
        return self._status_fn()
    
    def get_events(self, since_seq: int = 0, limit: int = 50) -> Dict[str, Any]:
        return self._events_fn(since_seq, limit)
    
    def get_nte_state(self) -> Dict[str, float]:
        return self._nte_fn()
