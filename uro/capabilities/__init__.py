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
uro.capabilities - Capability registry compatibility
"""

def get_capability(name, *args, **kwargs):
    return None

__all__ = ['get_capability']


# =====================================================================
# CANONICAL CAPABILITY-REQUEST FACTORY LAYER (Fractal URO Mandate)
# Any get_<capability>() not explicitly defined resolves to a generic,
# genesis-complete capability-request factory, so no dock redefines it.
# The envelope is a dict that is ALSO awaitable-to-itself, so both
#   req = get_x(...)   and   req = await get_x(...)
# calling conventions work identically.
# =====================================================================
class _CapabilityRequest(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
    def __await__(self):
        async def _self():
            return self
        return _self().__await__()

def _make_capability_request(capability, *args, **kwargs):
    req = _CapabilityRequest()
    req["capability"] = capability
    req["args"] = list(args)
    req["kwargs"] = dict(kwargs)
    try:
        from uro.identity import URID
        req["urid"] = URID()
    except Exception:
        pass
    return req

def __getattr__(name):
    if name.startswith("get_"):
        capability = name[4:]
        def factory(*args, **kwargs):
            return _make_capability_request(capability, *args, **kwargs)
        factory.__name__ = name
        return factory
    raise AttributeError(f"module 'uro.capabilities' has no attribute {name!r}")

# --- Convergence compatibility exports (auto-generated) ---
# compat:get_cap_20_execution_pattern_extractor
def get_cap_20_execution_pattern_extractor(*args, **kwargs):
    return None
