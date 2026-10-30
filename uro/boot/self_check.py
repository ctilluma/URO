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
# MODULE START : uro.boot.self_check
# ---------------------------------------------------------------------
# FILE         : uro/boot/self_check.py
# PURPOSE      : Four-step self-check with quarantine semantics: INAHASH,
#                URID integrity, NTE bounds, custody head (RFC 109).
# STANDARD     : URO-STD-0001 S12
# =====================================================================
"Four-step self-check with quarantine semantics (RFC 109)."

from __future__ import annotations

from typing import Any, Dict, Tuple

__all__ = ["SELF_CHECK_STEPS", "self_check"]

SELF_CHECK_STEPS: Tuple[str, ...] = (
    "inahash_verify", "urid_integrity", "nte_bounds", "custody_head")


def self_check(obj: Any) -> Dict[str, Any]:
    "PURPOSE: Run the four checks; quarantine when any fails (RFC 109)."
    results: Dict[str, Any] = {}
    compute = getattr(obj, "compute_inahash", None)
    stored = getattr(obj, "inahash", "")
    results["inahash_verify"] = bool(stored) and compute is not None and stored == compute()
    u1 = getattr(obj, "urid1", None)
    u2 = getattr(obj, "urid2", None)
    zero = hasattr(u1, "is_zero") and u1.is_zero()
    results["urid_integrity"] = u1 is not None and u2 is not None and not zero
    nte = getattr(obj, "nte_state", None) or getattr(obj, "nte", None) or obj
    levels = getattr(nte, "levels", None)
    results["nte_bounds"] = levels is not None and all(
        0.0 <= float(v) <= 100.0 for v in levels.values())
    head = getattr(obj, "custody_head", None)
    results["custody_head"] = True if head is None else head == stored
    results["quarantined"] = not all(results[k] for k in SELF_CHECK_STEPS)
    return results
# =====================================================================
# MODULE END   : uro.boot.self_check
# =====================================================================
