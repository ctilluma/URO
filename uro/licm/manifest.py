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


from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel, Field


class LicmCompliance(BaseModel):
    S2: bool = True
    S4: bool = True
    S7: bool = True
    S9: bool = True


class LICMManifest(BaseModel):
    dock_id: str
    menu_label: str
    icon: str = "cube"
    color_accent: str = "#22c55e"
    pitch: str = ""
    views: List[Any] = Field(default_factory=list)
    endpoints: List[Any] = Field(default_factory=list)
    ws_channel: str = "licm.events"
    compliance: LicmCompliance = Field(default_factory=LicmCompliance)
