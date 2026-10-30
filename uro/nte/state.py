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
MODULE: NTE State URO (Collection of Levels, 24-Axis Canonical)
INTENT: A URO representing the complete NTE state (all 24 axes). This is the
        fast-path reference for checking emotional state.
STANDARD: URO-STD-0001 S10.2
"""
from __future__ import annotations

import time
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator

from uro.core.urid import URID
from uro.security.hashing import inahash
from uro.nte.axes import NTEAxis
from uro.nte.level import NTELevelURO

__all__ = ["NTEStateURO", "NTEState"]


class NTEStateURO(BaseModel):
    """
    A URO representing the complete NTE state (all 24 axes).
    
    This is the fast-path reference for checking emotional state.
    The per-axis UROs are the durable, auditable record.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # ── IDENTITY ──────────────────────────────────────
    urid1: URID = Field(..., description="Parent URO (dock, synapse, etc.)")
    urid2: URID = Field(..., description="This NTE state's identity")
    
    # ── STATE ─────────────────────────────────────────
    # Fast-path: 24-dimensional vector for quick checks
    levels: Dict[NTEAxis, float] = Field(
        default_factory=lambda: {axis: 50.0 for axis in NTEAxis},
        description="Current levels for all 24 axes"
    )
    
    # ── REFERENCES TO PER-AXIS UROs ───────────────────
    # Durable record: each axis is its own URO with lineage and custody
    axis_refs: Dict[NTEAxis, URID] = Field(
        default_factory=dict,
        description="References to per-axis NTE Level UROs"
    )
    
    # ── INTEGRITY ─────────────────────────────────────
    inahash: str = Field(default="", description="INAHASH seal")
    parent_inahash: Optional[str] = Field(None, description="Parent URO's INAHASH")
    
    # ── TIMESTAMP ─────────────────────────────────────
    timestamp: float = Field(default_factory=time.time, description="Last update time")
    
    # === START: NTEState-24-Normalization ===
    @model_validator(mode="after")
    def _normalize_24_axes(self) -> "NTEStateURO":
        """
        Backward-compatible normalization.

        Guarantees that every NTEStateURO contains all 24 canonical axes.
        Old 12-axis states are accepted and missing cognitive axes are
        backfilled to baseline.
        """
        lookup = {}

        for axis in NTEAxis:
            lookup[axis.value] = axis
            lookup[axis.name] = axis

        raw_levels = self.levels or {}
        normalized = {}

        for key, value in raw_levels.items():
            axis = None

            if isinstance(key, NTEAxis):
                axis = key
            else:
                key_str = str(getattr(key, "value", key))
                axis = lookup.get(key_str)

                if axis is None:
                    axis = lookup.get(str(getattr(key, "name", "")))

            if axis is None:
                continue

            try:
                normalized[axis] = max(0.0, min(100.0, float(value)))
            except Exception:
                normalized[axis] = 50.0

        for axis in NTEAxis:
            normalized.setdefault(axis, 50.0)

        self.levels = normalized
        return self
    # === END: NTEState-24-Normalization ===

    def compute_inahash(self) -> str:
        """Compute the INAHASH seal."""
        data = self.model_dump(exclude={"inahash"})
        msg = str(data).encode()
        return inahash(msg).hex()
    
    def seal(self) -> None:
        """Seal this URO."""
        self.inahash = self.compute_inahash()
    
    def get_level(self, axis: NTEAxis) -> float:
        """Get the level for a specific axis."""
        return self.levels.get(axis, 50.0)
    
    def set_level(self, axis: NTEAxis, level: float) -> None:
        """Set the level for a specific axis."""
        self.levels[axis] = max(0.0, min(100.0, level))
        self.timestamp = time.time()
    
    def apply_delta(self, axis: NTEAxis, delta: float) -> None:
        """Apply a delta to a specific axis."""
        current = self.get_level(axis)
        self.set_level(axis, current + delta)
    
    def get_dominant_axis(self) -> NTEAxis:
        """Get the axis with the highest level."""
        return max(self.levels, key=self.levels.get)
    
    def is_balanced(self, threshold: float = 15.0) -> bool:
        """Check if all axes are within threshold of baseline (50)."""
        return all(abs(level - 50.0) <= threshold for level in self.levels.values())


# Backward-compat alias: docks import the pre-rename name NTEState.
NTEState = NTEStateURO
