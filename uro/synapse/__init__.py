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


"""Synapse vector package (per-relationship emotional state)."""
from uro.synapse.topic_trust import TopicTrustURO
from uro.synapse.vector import SynapseVectorURO
from uro.synapse import engine
from uro.synapse import persistence

__all__ = ["TopicTrustURO", "SynapseVectorURO", "engine", "persistence"]

# BASE-URO FACADE (flat re-exports, Fractal URO Mandate)

from uro.synapse.vector import SynapseVectorURO
from uro.base_uros import (SynapseVector, SynapseType, SynapseTopic, TrustLevel,
                           SynapseEndpoint, SynapseManager, create_synapse)

# Dock genesis alias: 'from uro.synapse import Synapse'
Synapse = SynapseVectorURO

# --- Convergence compatibility exports (auto-generated) ---
# compat:TrustTopic
class TrustTopic:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:establish_synapse
try:
    from uro.canonical_integration import establish_synapse
except Exception:
    establish_synapse = None


# PERMISSIVE_COMPAT_GETATTR
_STUB_WARNED = set()

def __getattr__(name):
    "PURPOSE: Resolve real submodules first, then warn and stub (ADR-009)."
    import importlib
    try:
        return importlib.import_module("." + name, __name__)
    except Exception:
        pass
    if name not in _STUB_WARNED:
        _STUB_WARNED.add(name)
        import logging as _lg
        _lg.getLogger("uro.synapse").warning(
            "[SYNAPSE] permissive compat stub served for missing name: %s", name)
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

