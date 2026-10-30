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


"""API-layer re-exports for receipt types."""
from uro.exchange.receipt import ReceiptURO, ReceiptMode
Receipt = ReceiptURO
ReceiptStatus = ReceiptMode
ReceiptEnvelope = ReceiptURO
__all__ = ["ReceiptURO", "ReceiptMode", "Receipt", "ReceiptStatus", "ReceiptEnvelope"]

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
