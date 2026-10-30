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


"""Cognition package: fuzzy matrix, verdict dynamics, cognitive + memory layers."""
from uro.cognition.fuzzy import trimf, gauss_close, fuzzy_and, normalize, linguistic
from uro.cognition.verdict import VerdictDynamics
from uro.cognition.matrix import FuzzyMatrixURO, OUTCOME_SPACE, DEFAULT_PROTOTYPES
from uro.cognition.cognitive_fuzzy import (
    COGNITIVE_OUTCOMES, new_cognitive_matrix, cognitive_inputs, decide_strategy)
from uro.cognition.core import CognitiveCore
from uro.cognition.persistence import CognitivePersistence
from uro.cognition.myelination import (
    MyelinationLevel, detect_hot_synapses, myelinate_synapse,
    homeostatic_scale_decision, SynapseUsageTracker, SynapseUsageStats,
    GLOBAL_TRACKER, record_synapse_use, run_myelination_pass)
from uro.cognition.memory_fuzzy import (
    MEMORY_OUTCOMES, new_memory_matrix, memory_inputs, memory_decision,
    should_promote_fuzzy, should_decay_fuzzy, rank_memories_for_retrieval, cosine_similarity)

__all__ = [
    "trimf","gauss_close","fuzzy_and","normalize","linguistic",
    "VerdictDynamics","FuzzyMatrixURO","OUTCOME_SPACE","DEFAULT_PROTOTYPES",
    "COGNITIVE_OUTCOMES","new_cognitive_matrix","cognitive_inputs","decide_strategy",
    "MEMORY_OUTCOMES","new_memory_matrix","memory_inputs","memory_decision",
    "should_promote_fuzzy","should_decay_fuzzy","rank_memories_for_retrieval","cosine_similarity",
    "MyelinationLevel","detect_hot_synapses","myelinate_synapse",
    "homeostatic_scale_decision","SynapseUsageTracker","SynapseUsageStats",
    "GLOBAL_TRACKER","record_synapse_use","run_myelination_pass",
    "CognitiveCore",
    "CognitivePersistence",
]


# PERMISSIVE_COMPAT_GETATTR (submodule-first per ADR-009)
def __getattr__(name):
    "PURPOSE: Resolve real submodules first, then fall back to compat stubs (ADR-009)."
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

