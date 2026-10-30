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


# =====================================================================
# MODULE START : uro.nte.nte_state
# ---------------------------------------------------------------------
# FILE         : uro/nte/nte_state.py
# PURPOSE      : 24-axis NTE state view on the legacy [0,1] scale.
#                Brought up to the canonical 24-axis taxonomy (ADR-011,
#                ADR-013) while preserving the legacy public API
#                (kwargs constructor, attribute access, as_dict).
# STANDARD     : URO-STD-0001 S10.2
# =====================================================================
"Legacy-module 24-axis NTE state (ADR-011/013); canonical model is uro.nte.state.NTEStateURO."

from uro.nte.axes import NTEAxis

__all__ = ["NTEState"]

_LEGACY_EXTRAS = ("endorphins", "histamine")


class NTEState:
    "PURPOSE: 24-axis neuro-chemical state on the legacy [0,1] scale (ADR-013)."

    def __init__(self, **kwargs):
        "PURPOSE: Accept canonical axis kwargs plus legacy extras; default 0.5."
        object.__setattr__(self, "_levels", {a.value: 0.5 for a in NTEAxis})
        object.__setattr__(self, "_extras", {})
        for key, value in kwargs.items():
            if key in _LEGACY_EXTRAS:
                self._extras[key] = max(0.0, min(1.0, float(value)))
            elif key in self._levels:
                self._levels[key] = max(0.0, min(1.0, float(value)))

    def __getattr__(self, name):
        "PURPOSE: Expose axis levels and legacy extras as attributes."
        levels = object.__getattribute__(self, "_levels")
        if name in levels:
            return levels[name]
        extras = object.__getattribute__(self, "_extras")
        if name in extras:
            return extras[name]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        "PURPOSE: Clamp axis writes to [0,1]; unknown names set normally."
        if name in ("_levels", "_extras"):
            object.__setattr__(self, name, value)
            return
        if name in self._levels:
            self._levels[name] = max(0.0, min(1.0, float(value)))
        elif name in _LEGACY_EXTRAS:
            self._extras[name] = max(0.0, min(1.0, float(value)))
        else:
            object.__setattr__(self, name, value)

    def as_dict(self) -> dict:
        "PURPOSE: All 24 canonical axes on the legacy [0,1] scale."
        return dict(self._levels)

    def to_canonical(self) -> dict:
        "PURPOSE: Bridge legacy [0,1] levels to canonical 24-axis [0,100] state."
        return {k: max(0.0, min(100.0, v * 100.0)) for k, v in self._levels.items()}
# =====================================================================
# MODULE END   : uro.nte.nte_state
# =====================================================================
