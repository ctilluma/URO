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


"""
uro.registry - Registry compatibility
"""

class URORegistry:
    def __init__(self, *args, **kwargs):
        self._items = {}
    
    def register(self, *args, **kwargs):
        if args:
            self._items[args[0]] = args[1] if len(args) > 1 else args[0]
        return True

__all__ = ['URORegistry']

"""Flat facade module - re-exports canonical base UROs (Fractal URO Mandate)."""

from uro.registry_bridge import get_registry
from uro.base_uros import get_uro_registry
class URORegistry:
    """Registry facade over the canonical registry bridge."""
    def __init__(self): self._r = get_registry()
    def __getattr__(self, n): return getattr(self._r, n)
def register_with_master(*a, **k): return get_uro_registry()
def register_domain(*a, **k): return get_uro_registry()
__all__ = ["URORegistry","get_registry","get_uro_registry","register_with_master","register_domain"]

# --- Convergence compatibility exports (auto-generated) ---
# compat:CapabilityRegistration
class CapabilityRegistration:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:CapabilityRegistry
class CapabilityRegistry:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:DockRegistry
class DockRegistry:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:MasterCanonicalRegistry
class MasterCanonicalRegistry:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:RegistryDiscovery
class RegistryDiscovery:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:register_hyper_node
def register_hyper_node(*args, **kwargs):
    return None
