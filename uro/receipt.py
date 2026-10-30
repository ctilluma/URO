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
uro.receipt - Receipt compatibility module
Provides Receipt and related types for docks that import from uro.receipt
"""

# Import from the canonical framework
import sys, os
# Try dock-specific framework first, fall back to aegis
for fw_name in ['sentinel_framework', 'auction_framework', 'bazaar_framework', 'aegis_framework']:
    try:
        fw_path = os.path.join(os.getcwd(), 'docks', fw_name.replace('_framework', ''), fw_name + '.py')
        if os.path.exists(fw_path):
            import importlib.util
            spec = importlib.util.spec_from_file_location(fw_name, fw_path)
            fw = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(fw)
            Receipt = fw.Receipt
            ReceiptStatus = fw.ReceiptStatus
            break
    except:
        continue
else:
    # Minimal fallback
    class ReceiptStatus:
        FULFILLED = "FULFILLED"
        DEFERRED = "DEFERRED"
        INCAPABLE = "INCAPABLE"
    
    class Receipt:
        def __init__(self, status=None, payload=None, reason=None, **kwargs):
            self.status = status or ReceiptStatus.FULFILLED
            self.payload = payload or {}
            self.reason = reason or ""

__all__ = ['Receipt', 'ReceiptStatus']

"""Flat facade module - re-exports canonical base UROs (Fractal URO Mandate)."""

from uro.exchange.receipt import ReceiptURO, ReceiptMode
from uro.base_uros import FULFILLED, DEFERRED, INCAPABLE, ReceiptEnvelope, create_receipt
Receipt = ReceiptURO
ReceiptStatus = ReceiptMode
__all__ = ["Receipt","ReceiptURO","ReceiptStatus","ReceiptMode","ReceiptEnvelope",
           "FULFILLED","DEFERRED","INCAPABLE","create_receipt"]

# --- Convergence compatibility exports (auto-generated) ---
# compat:RECEIPT_DEFERRED
class RECEIPT_DEFERRED:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:RECEIPT_FULFILLED
class RECEIPT_FULFILLED:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# compat:RECEIPT_INCAPABLE
class RECEIPT_INCAPABLE:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
