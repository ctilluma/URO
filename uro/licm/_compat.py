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

from typing import Any


def model_dump(model: Any) -> dict:
    if isinstance(model, dict):
        return model
    if hasattr(model, "model_dump"):
        try:
            return model.model_dump(mode="json")
        except TypeError:
            return model.model_dump()
    if hasattr(model, "dict"):
        return model.dict()
    raise TypeError(f"cannot dump model-like object: {type(model)!r}")


def model_validate(cls: Any, data: Any):
    if hasattr(cls, "model_validate"):
        return cls.model_validate(data)
    if hasattr(cls, "parse_obj"):
        return cls.parse_obj(data)
    if isinstance(data, dict):
        return cls(**data)
    raise TypeError(f"cannot validate {cls!r} with {type(data)!r}")
