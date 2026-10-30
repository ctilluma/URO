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
uro.identity - Identity compatibility module
"""

import sys, os
for fw_name in ['sentinel_framework', 'auction_framework', 'bazaar_framework', 'aegis_framework']:
    try:
        fw_path = os.path.join(os.getcwd(), 'docks', fw_name.replace('_framework', ''), fw_name + '.py')
        if os.path.exists(fw_path):
            import importlib.util
            spec = importlib.util.spec_from_file_location(fw_name, fw_path)
            fw = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(fw)
            URID = fw.URID
            INAHASH = fw.INAHASH
            break
    except:
        continue
else:
    import uuid, hashlib
    class URID:
        @staticmethod
        def generate(**kwargs):
            inst = URID.__new__(URID)
            try:
                URID.__init__(inst, **kwargs)
            except Exception:
                pass
            for _a in ("value", "id", "urid"):
                if not hasattr(inst, _a):
                    setattr(inst, _a, f"uro-" + uuid.uuid4().hex[:8])
            return inst
    
    class INAHASH:
        @staticmethod
        def compute(data):
            return hashlib.sha256(str(data).encode()).hexdigest()[:16]

__all__ = ['URID', 'INAHASH']

"""Flat facade module - re-exports canonical base UROs (Fractal URO Mandate)."""
from uro.core.urid import URID
from uro.base_uros import INAHASH
__all__=["URID","INAHASH"]
