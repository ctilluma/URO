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
# MODULE START : uro.aupi
# ---------------------------------------------------------------------
# FILE         : uro/aupi.py
# PURPOSE      : AUPI - Automated URO Programming Interface. The
#                translation layer that lets a URO convert the UPI it HAS
#                into the UPI it NEEDS by pathing across translators.
#
#                From the standard: "a URO contains a number URO, and
#                needs to provide a phone number to another URO. This
#                allows the URO to find a phone number URO, send it the
#                number URO it has, and receive back a phone number URO."
#
#                Translators are themselves UROs (AUPI.TRANSLATOR) and
#                can be chained (a->b, b->c  =>  a->c).
# STANDARD     : URO-STD-0001 S-URO Interfacing (AUPI)
# =====================================================================
"""AUPI - automated translation between available and required UPIs."""

from __future__ import annotations

from collections import deque
from typing import Any, Callable, Dict, List, Tuple

from uro.core.uro import URO
from uro.core.urid import URID
from uro.relations.association import Association, ConnectionType
from uro.exceptions import TranslationError

__all__ = ["Translator", "AUPI", "typed_uro"]


def typed_uro(type_name: str, value: Any) -> URO:
    """Create a URO carrying a typed value.

    Typed UROs use a payload of {"type": str, "value": Any} so the AUPI
    can reason about what kind of information they hold.

    Args:
        type_name: The logical type name (e.g. "number").
        value: The value being carried.

    Returns:
        URO: A URO whose payload describes the typed value.
    """
    return URO.new(payload={"type": type_name, "value": value})


class Translator(URO):
    """A URO that converts one UPI type into another.

    Attributes:
        source_type: The input type name.
        target_type: The output type name.
        func: The conversion callable value -> value.
    """

    def __init__(self, source_type: str, target_type: str,
                 func: Callable[[Any], Any]) -> None:
        """Create a translator URO.

        Args:
            source_type: Input type name.
            target_type: Output type name.
            func: Conversion callable.
        """
        _identity = URID.new()
        super().__init__(_identity, _identity, {"kind": "AUPI.TRANSLATOR"})
        self.source_type = source_type
        self.target_type = target_type
        self.func = func

    def apply(self, value: Any) -> Any:
        """Apply the conversion to a value.

        Args:
            value: The input value.

        Returns:
            Any: The converted value.
        """
        return self.func(value)


class AUPI(URO):
    """The automated translation layer.

    AUPI maintains a directed graph of translators keyed by source type
    and resolves a path from an available type to a required type, then
    applies the chain of conversions.
    """

    def __init__(self) -> None:
        """Create an empty AUPI translation layer."""
        _identity = URID.new()
        super().__init__(_identity, _identity, {"kind": "AUPI"})
        self._edges: Dict[str, List[Translator]] = {}
        self._container_cache: Dict[Tuple[str, str], List[Translator]] = {}

    def register(self, source_type: str, target_type: str,
                 func: Callable[[Any], Any]) -> Translator:
        """Register a translator between two types.

        Args:
            source_type: Input type name.
            target_type: Output type name.
            func: Conversion callable.

        Returns:
            Translator: The registered translator URO.
        """
        t = Translator(source_type, target_type, func)
        self._edges.setdefault(source_type, []).append(t)
        self.add_child(t)
        return t

    def find_path(self, source_type: str,
                  target_type: str) -> List[Translator]:
        """Find a chain of translators from source to target (BFS).

        Args:
            source_type: Starting type.
            target_type: Desired type.

        Returns:
            List[Translator]: An ordered list of translators to apply.

        Raises:
            TranslationError: If no translation path exists.
        """
        if source_type == target_type:
            return []
        queue = deque([(source_type, [])])
        seen = {source_type}
        while queue:
            current, path = queue.popleft()
            for t in self._edges.get(current, []):
                if t.target_type == target_type:
                    return path + [t]
                if t.target_type not in seen:
                    seen.add(t.target_type)
                    queue.append((t.target_type, path + [t]))
        raise TranslationError(
            f"no translation path from {source_type!r} to {target_type!r}")

    def translate_value(self, value: Any, source_type: str,
                        target_type: str) -> Any:
        """Translate a raw value between types.

        Args:
            value: The input value.
            source_type: The input type.
            target_type: The desired type.

        Returns:
            Any: The converted value.
        """
        result = value
        for t in self.find_path(source_type, target_type):
            result = t.apply(result)
        return result

    def translate(self, source_uro: URO, target_type: str) -> URO:
        """Translate a typed URO into a new typed URO of target_type.

        Args:
            source_uro: A URO whose payload is {"type", "value"}.
            target_type: The desired output type.

        Returns:
            URO: A new typed URO carrying the converted value.

        Raises:
            TranslationError: If the source is untyped or untranslatable.
        """
        payload = source_uro.payload
        if not isinstance(payload, dict) or "type" not in payload:
            raise TranslationError("source URO is not a typed URO")
        src_type = payload["type"]
        new_value = self.translate_value(payload["value"], src_type,
                                         target_type)
        out = typed_uro(target_type, new_value)
        # Record the translation as a relationship between the UROs.
        Association(source_uro, out, ConnectionType.PATH)
        return out

    def resolve_container(self, source_uro: URO, target_type: str) -> URO:
        "PURPOSE: RFC 88 container resolution with cached localized wrapper paths."
        key = (self._payload_type(source_uro), target_type)
        if key not in self._container_cache:
            self._container_cache[key] = self.find_path(key[0], key[1])
        return self.translate(source_uro, target_type)

    def _payload_type(self, source_uro: URO) -> str:
        "PURPOSE: Extract the logical type name from a typed URO payload."
        payload = source_uro.payload
        if isinstance(payload, dict) and "type" in payload:
            return payload["type"]
        raise TranslationError("source URO is not a typed URO")
# =====================================================================
# MODULE END   : uro.aupi
# =====================================================================
