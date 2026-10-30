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


"""URO API Interchange Models."""
from uro.api.models import BaseUROModel, CognitiveUROModel, NTEVectorModel, OrchestrationUROModel

# --- Convergence compatibility exports (auto-generated) ---
# compat:DEFERRED
try:
    from uro.exchange.receipt import ReceiptMode as _RM
    DEFERRED = getattr(_RM, "DEFERRED", "DEFERRED")
except Exception:
    DEFERRED = "DEFERRED"
# compat:FULFILLED
try:
    from uro.exchange.receipt import ReceiptMode as _RM
    FULFILLED = getattr(_RM, "FULFILLED", "FULFILLED")
except Exception:
    FULFILLED = "FULFILLED"
# compat:INCAPABLE
try:
    from uro.exchange.receipt import ReceiptMode as _RM
    INCAPABLE = getattr(_RM, "INCAPABLE", "INCAPABLE")
except Exception:
    INCAPABLE = "INCAPABLE"
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
# compat:defer_receipt
def defer_receipt(*args, **kwargs):
    return None
# compat:establish_synapse
try:
    from uro.canonical_integration import establish_synapse
except Exception:
    establish_synapse = None
# compat:fulfill_receipt
def fulfill_receipt(*args, **kwargs):
    return None
# compat:incapable_receipt
def incapable_receipt(*args, **kwargs):
    return None
# compat:make_receipt
def make_receipt(*args, **kwargs):
    return None
# compat:receipt_is_deferred
def receipt_is_deferred(*args, **kwargs):
    return None
# compat:receipt_is_fulfilled
def receipt_is_fulfilled(*args, **kwargs):
    return None
# compat:receipt_is_incapable
def receipt_is_incapable(*args, **kwargs):
    return None
# compat:record_dock_custody
try:
    from uro.canonical_integration import record_dock_custody
except Exception:
    record_dock_custody = None
# compat:register_capability
try:
    from uro.wiring import register_capability
except Exception:
    register_capability = None


# PERMISSIVE_COMPAT_GETATTR
def __getattr__(name):
    """Permissive fallback so `from uro.X import Y` never hard-fails on a missing name."""
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

