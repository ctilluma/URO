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

from enum import Enum
from typing import Any, Dict

from .exceptions import LicmProvenanceError


class Provenance(str, Enum):
    LIVE = "LIVE"
    DERIVED = "DERIVED"
    DEMO = "DEMO"
    UNMEASURED = "UNMEASURED"

    @classmethod
    def parse(cls, value: Any) -> "Provenance":
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            value = value.get("kind", value.get("provenance"))
        if value is None:
            raise LicmProvenanceError("provenance is required")
        text = str(value).strip().upper().replace("-", "_").replace(" ", "_")
        if text in cls.__members__:
            return cls.__members__[text]
        try:
            return cls(text)
        except ValueError as exc:
            raise LicmProvenanceError(f"unknown provenance: {value!r}") from exc


STATUS_PROVENANCES = {Provenance.LIVE, Provenance.DERIVED, Provenance.UNMEASURED}


def normalize_provenance(provenance: Any) -> Dict[str, Any]:
    if isinstance(provenance, dict):
        kind = Provenance.parse(provenance)
        out: Dict[str, Any] = {"kind": kind.value}
        for key in ("derivation", "reason", "source", "method", "note"):
            if provenance.get(key) not in (None, ""):
                out[key] = provenance[key]
    else:
        kind = Provenance.parse(provenance)
        out = {"kind": kind.value}

    if out["kind"] == Provenance.DERIVED.value and not out.get("derivation"):
        raise LicmProvenanceError("DERIVED provenance requires a derivation string")
    if out["kind"] == Provenance.UNMEASURED.value and not out.get("reason"):
        raise LicmProvenanceError("UNMEASURED provenance requires a reason")
    return out


def live(value: Any, **meta: Any) -> Dict[str, Any]:
    out: Dict[str, Any] = {"value": value, "provenance": Provenance.LIVE.value}
    out.update(meta)
    return out


def derive_from_registry(value: Any, derivation: str, **meta: Any) -> Dict[str, Any]:
    if not derivation:
        raise LicmProvenanceError("DERIVED provenance requires a derivation string")
    out: Dict[str, Any] = {
        "value": value,
        "provenance": Provenance.DERIVED.value,
        "derivation": derivation,
    }
    out.update(meta)
    return out


def unmeasured(reason: str, value: Any = None) -> Dict[str, Any]:
    if not reason:
        raise LicmProvenanceError("UNMEASURED provenance requires a reason")
    return {
        "value": value,
        "provenance": Provenance.UNMEASURED.value,
        "reason": reason,
    }


def validate_status_payload(payload: Any) -> None:
    """
    QA gate: any status field without LIVE/DERIVED/UNMEASURED provenance fails.
    DEMO is not valid for operational status fields.
    """

    def _path(parts):
        return "/" + "/".join(str(part) for part in parts) if parts else "<root>"

    def _walk(node: Any, path, key=None):
        if key is not None and str(key).startswith("_"):
            return

        if isinstance(node, dict):
            if "provenance" in node:
                kind = Provenance.parse(node["provenance"])
                if kind not in STATUS_PROVENANCES:
                    raise LicmProvenanceError(
                        f"status provenance at {_path(path)} must be LIVE, DERIVED, or UNMEASURED; got {kind.value}"
                    )
                if kind == Provenance.DERIVED and not node.get("derivation"):
                    raise LicmProvenanceError(f"DERIVED status field at {_path(path)} requires derivation")
                if kind == Provenance.UNMEASURED and not node.get("reason"):
                    raise LicmProvenanceError(f"UNMEASURED status field at {_path(path)} requires reason")
                return

            if "value" in node:
                raise LicmProvenanceError(f"status field at {_path(path)} has value but no provenance")

            for child_key, child in node.items():
                _walk(child, path + [child_key], child_key)
            return

        if isinstance(node, list):
            for idx, item in enumerate(node):
                _walk(item, path + [idx], None)
            return

        raise LicmProvenanceError(f"status field at {_path(path)} lacks provenance")

    if payload is None:
        raise LicmProvenanceError("status payload cannot be None")
    _walk(payload, [], None)
