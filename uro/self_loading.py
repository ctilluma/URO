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
# MODULE START : uro.self_loading
# ---------------------------------------------------------------------
# FILE         : uro/self_loading.py
# PURPOSE      : Object self-loading: pull scripted config, ensure parent
#                script/object code, compile and hold locally during
#                reflection (RFC 86, 3.10).
# STANDARD     : URO-STD-0001 S3.10
# =====================================================================
"Object self-loading of scripted configuration and parent code (RFC 86)."

from __future__ import annotations

from typing import Any, Dict

__all__ = ["SelfLoader"]


class SelfLoader:
    "PURPOSE: Pull config, assure parent code, optional local compile (RFC 86)."

    def __init__(self) -> None:
        self.config: Dict[str, Any] = {}
        self.parent_code: Dict[str, Any] = {}
        self.compiled: Dict[str, bool] = {}

    def pull_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        "PURPOSE: Pull scripted object configuration (RFC 86 step 1)."
        self.config.update(config)
        return self.config

    def ensure_parent_code(self, parent_id: str, code: Any) -> Any:
        "PURPOSE: Ensure script/object code for parents is present (RFC 86)."
        self.parent_code.setdefault(parent_id, code)
        return self.parent_code[parent_id]

    def compile_local(self, parent_id: str) -> bool:
        "PURPOSE: During reflection, compile and hold code locally (RFC 86)."
        if parent_id not in self.parent_code:
            return False
        self.compiled[parent_id] = True
        return True
# =====================================================================
# MODULE END   : uro.self_loading
# =====================================================================
