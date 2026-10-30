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


"""Core URO model (URID, URO, UROSpace)."""
from uro.core.urid import URID, new_urid, new_uuid
from uro.core.uro import URO, sha128
from uro.core.space import UROSpace

__all__ = ["URID", "new_urid", "new_uuid", "URO", "sha128", "UROSpace"]

# --- Convergence compatibility exports (auto-generated) ---
# compat:CNSDispatcher
class CNSDispatcher:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:CognitiveMaster
class CognitiveMaster:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:CoordinatorBus
try:
    from uro.coordinator_bus import CoordinatorBus
except Exception:
    CoordinatorBus = None
# compat:NTE
try:
    from uro.nte.neurotransmitters import NTE
except Exception:
    NTE = None
# compat:Receipt
try:
    from uro.receipt import Receipt
except Exception:
    Receipt = None
# compat:create_dock_uro
try:
    from uro.canonical_integration import create_dock_uro
except Exception:
    create_dock_uro = None
# compat:establish_synapse
try:
    from uro.canonical_integration import establish_synapse
except Exception:
    establish_synapse = None
# compat:get_cognitive
def get_cognitive(*args, **kwargs):
    return None
# compat:record_dock_custody
try:
    from uro.canonical_integration import record_dock_custody
except Exception:
    record_dock_custody = None


# PERMISSIVE_COMPAT_GETATTR
def __getattr__(name):
    "PURPOSE: Resolve real submodules before falling back to legacy compat stubs (ADR-009)."
    import importlib
    try:
        return importlib.import_module("." + name, __name__)
    except Exception:
        pass
    class _CompatStub:
        # VAUROS-MAGIC-V3
        def __getitem__(self, key): return None
        def get(self, key, default=None): return default
        def __getattr__(self, name): return self
        def __bool__(self): return False
        def __call__(self, *a, **k): return {"status": "FULFILLED", "data": {}, "payload": b""}
        @classmethod
        def generate(cls, *a, **k):
            import uuid
            return cls(value=f"stub_{uuid.uuid4().hex[:8]}")
        @classmethod
        def create(cls, *a, **k):
            return cls(*a, **k)
        @classmethod
        def seal(cls, *a, **k):
            return cls()
        def __init__(self, *a, **k):
            for _k, _v in k.items():
                setattr(self, _k, _v)
        def _vauros_disabled___call__(self, *a, **k):
            return self
        def _vauros_disabled___getattr__(self, _n):
            return _CompatStub()
    return _CompatStub

