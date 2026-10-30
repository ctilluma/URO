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
# MODULE START : uro.learning.dicho
# ---------------------------------------------------------------------
# FILE         : uro/learning/dicho.py
# PURPOSE      : Dicho (idiom) processing: phrases across languages map to
#                a shared core URO idea; commonalities first, then
#                sentence structure (RFC 91.1).
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"Dicho (idiom) processing against core URO ideas (RFC 91.1)."

from __future__ import annotations

from typing import Dict, List, Optional

__all__ = ["DichoRegistry"]


class DichoRegistry:
    "PURPOSE: Map dichos across languages to a shared core URO idea."

    def __init__(self) -> None:
        self._phrase_to_core: Dict[str, str] = {}
        self._core_to_phrases: Dict[str, List[str]] = {}

    def register(self, phrase: str, core_idea: str) -> None:
        "PURPOSE: Bind a phrase to its core URO idea."
        key = phrase.lower()
        self._phrase_to_core[key] = core_idea
        self._core_to_phrases.setdefault(core_idea, []).append(key)

    def resolve(self, phrase: str) -> Optional[str]:
        "PURPOSE: Commonality-first lookup of the core idea (RFC 91.1)."
        return self._phrase_to_core.get(phrase.lower())

    def commonalities(self, phrase_a: str, phrase_b: str) -> Optional[str]:
        "PURPOSE: Shared core idea between two dichos, else None."
        a = self.resolve(phrase_a)
        b = self.resolve(phrase_b)
        if a is not None and a == b:
            return a
        return None

    def structure_fallback(self, phrase_a: str, phrase_b: str) -> List[str]:
        "PURPOSE: Sentence-structure comparison when no shared core exists."
        ta = set(phrase_a.lower().split())
        tb = set(phrase_b.lower().split())
        return sorted(ta & tb)
# =====================================================================
# MODULE END   : uro.learning.dicho
# =====================================================================
