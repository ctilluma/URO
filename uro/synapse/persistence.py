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
MODULE: Synapse Durable Persistence
INTENT: Disk-backed storage for SynapseVectorURO objects so the relationship
        (R) graph survives restarts and is included in full swarm rebuilds.
STANDARD: URO-STD-0001 S10.4
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from uro.core.urid import URID
from uro.nte.axes import NTEAxis
from uro.nte.state import NTEStateURO
from uro.synapse.vector import SynapseVectorURO

__all__ = ["STATE_ROOT", "save_synapse", "load_synapse", "get_or_create_synapse",
           "list_synapse_ids", "modulate_and_persist"]

STATE_ROOT = Path(os.environ.get(
    "URO_STATE_ROOT",
    os.path.expanduser("~/.auraforge_state/uro/synapses"),
))


# === START: Path and Index Helpers ===
def _dir() -> Path:
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    return STATE_ROOT


def _index_path() -> Path:
    return _dir() / "index.json"


def _load_index() -> Dict[str, str]:
    p = _index_path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def _save_index(idx: Dict[str, str]) -> None:
    ip = _index_path()
    ip.write_text(json.dumps(idx, indent=2))
    try:
        os.chmod(ip, 0o664)
    except Exception:
        pass


def _uid_str(u) -> str:
    to_hex = getattr(u, "to_hex", None)
    if callable(to_hex):
        try:
            h = to_hex()
            if isinstance(h, str) and h:
                return h
        except Exception:
            pass
    for attr in ("hex", "value", "id", "urn"):
        v = getattr(u, attr, None)
        if isinstance(v, str):
            return v
    return str(u)


def _sanitize(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name)[:120]


def _pair_key(a, b) -> str:
    return "|".join(sorted([_uid_str(a), _uid_str(b)]))
# === END: Path and Index Helpers ===


# === START: Save and Load ===
def _json_default(o):
    """Serialization fallback: map URID and any unknown type to a stable string."""
    if isinstance(o, URID):
        return _uid_str(o)
    return str(o)


def _probe_urid_factory():
    """Discover at import time a constructor that round-trips a URID string."""
    try:
        probe = URID.new() if callable(getattr(URID, "new", None)) else URID()
    except Exception:
        return None
    s = _uid_str(probe)
    candidates = (
        lambda t: URID.from_hex(t),
        lambda t: URID(t),
        lambda t: URID.new(t),
        lambda t: URID.from_str(t),
        lambda t: URID(value=t),
        lambda t: URID(hex=t),
    )
    for fn in candidates:
        try:
            if _uid_str(fn(s)) == s:
                return fn
        except Exception:
            continue
    return None


_URID_FACTORY = _probe_urid_factory()


def _urid_from_str(s: str):
    """Reconstruct a URID from its canonical string, preserving identity."""
    if not isinstance(s, str) or not s:
        return None
    if _URID_FACTORY is not None:
        try:
            u = _URID_FACTORY(s)
            if _uid_str(u) == s:
                return u
        except Exception:
            pass
    return None


def _coerce_urids(d):
    """Recursively restore URID instances from strings prior to validation."""
    if isinstance(d, dict):
        out = {}
        for k, v in d.items():
            if isinstance(v, str) and "urid" in k.lower():
                u = _urid_from_str(v)
                out[k] = u if u is not None else v
            else:
                out[k] = _coerce_urids(v)
        return out
    if isinstance(d, list):
        return [_coerce_urids(x) for x in d]
    return d


def save_synapse(synapse: SynapseVectorURO) -> Path:
    """Seal and write one synapse to disk; update the pair index."""
    synapse.seal()
    fp = _dir() / (_sanitize(_uid_str(synapse.synapse_urid)) + ".json")
    payload = json.dumps(
        synapse.model_dump(mode="python"),
        indent=2,
        default=_json_default,
    )
    fp.write_text(payload)
    try:
        os.chmod(fp, 0o664)
    except Exception:
        pass
    idx = _load_index()
    idx[_pair_key(synapse.urid1, synapse.urid2)] = _uid_str(synapse.synapse_urid)
    _save_index(idx)
    return fp


# === START: 24-Axis Disk Migration ===
def _normalize_raw_nte(raw: dict) -> dict:
    """
    Backward-compatible disk migration.

    Converts old 12-axis persisted NTE states into canonical 24-axis states.
    Missing canonical axes are backfilled to baseline.
    Unknown axes are dropped for now.
    """
    if not isinstance(raw, dict):
        return raw

    nte = raw.get("nte_state")

    if not isinstance(nte, dict):
        return raw

    lookup = {}

    for axis in NTEAxis:
        lookup[axis.value] = axis.value
        lookup[axis.name] = axis.value

    levels = nte.get("levels")

    if isinstance(levels, dict):
        normalized_levels = {}

        for key, value in levels.items():
            canonical_key = lookup.get(str(key))

            if canonical_key is None:
                continue

            try:
                normalized_levels[canonical_key] = float(value)
            except Exception:
                normalized_levels[canonical_key] = 50.0

        for axis in NTEAxis:
            normalized_levels.setdefault(axis.value, 50.0)

        nte["levels"] = normalized_levels

    axis_refs = nte.get("axis_refs")

    if isinstance(axis_refs, dict):
        normalized_refs = {}

        for key, value in axis_refs.items():
            canonical_key = lookup.get(str(key))

            if canonical_key is not None:
                normalized_refs[canonical_key] = value

        nte["axis_refs"] = normalized_refs

    raw["nte_state"] = nte
    return raw
# === END: 24-Axis Disk Migration ===


def load_synapse(synapse_urid) -> Optional[SynapseVectorURO]:
    """Load one synapse from disk by its synapse URID."""
    fp = _dir() / (_sanitize(_uid_str(synapse_urid)) + ".json")

    if not fp.exists():
        return None

    try:
        raw = json.loads(fp.read_text())
        raw = _coerce_urids(raw)
        raw = _normalize_raw_nte(raw)
        return SynapseVectorURO.model_validate(raw)
    except Exception as e:
        import sys, traceback
        print(f"[SYNAPSE-PERSIST] load failed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return None


def list_synapse_ids() -> List[str]:
    return list(_load_index().values())
# === END: Save and Load ===


# === START: Registry and Modulation Entry ===
def get_or_create_synapse(urid1, urid2) -> SynapseVectorURO:
    """Return the existing synapse for an endpoint pair, or create and save it."""
    idx = _load_index()
    key = _pair_key(urid1, urid2)
    sid = idx.get(key)
    if sid:
        existing = load_synapse(sid)
        if existing is not None:
            return existing
    u1 = _urid_from_str(urid1) if isinstance(urid1, str) else urid1
    u2 = _urid_from_str(urid2) if isinstance(urid2, str) else urid2
    s = URID()
    nte = NTEStateURO(urid1=s, urid2=URID())
    syn = SynapseVectorURO(urid1=u1 if u1 is not None else urid1,
                           urid2=u2 if u2 is not None else urid2,
                           synapse_urid=s, nte_state=nte)
    save_synapse(syn)
    idx = _load_index()
    idx[_pair_key(urid1, urid2)] = _uid_str(s)
    _save_index(idx)
    return syn


def modulate_and_persist(synapse: SynapseVectorURO, outcome: dict) -> dict:
    """Modulate all 24 axes for one interaction, then persist immediately."""
    synapse.record_interaction(outcome)
    save_synapse(synapse)
    return dict(synapse.nte_state.levels)
# === END: Registry and Modulation Entry ===

# === START: Deferred I/O Buffer ===
_DIRTY_BUFFER: set = set()
_DIRTY_REFS: dict = {}
FLUSH_THRESHOLD = 64

def mark_dirty(synapse: SynapseVectorURO) -> None:
    """Mark a synapse as modified for deferred persistence (non-blocking)."""
    try:
        sid = _uid_str(synapse.synapse_urid)
        _DIRTY_BUFFER.add(sid)
        _DIRTY_REFS[sid] = synapse
        if len(_DIRTY_BUFFER) >= FLUSH_THRESHOLD:
            flush_dirty()
    except Exception:
        pass

def flush_dirty() -> int:
    """Persist all dirty synapses to disk. Returns count flushed."""
    count = 0
    for sid in list(_DIRTY_BUFFER):
        if sid in _DIRTY_REFS:
            try:
                save_synapse(_DIRTY_REFS[sid])
                count += 1
            except Exception:
                pass
    _DIRTY_BUFFER.clear()
    _DIRTY_REFS.clear()
    return count


def _register_exit_flush() -> None:
    """Guarantee a graceful-shutdown flush of the write-behind buffer."""
    import atexit
    atexit.register(flush_dirty)


_register_exit_flush()
# === END: Deferred I/O Buffer ===
