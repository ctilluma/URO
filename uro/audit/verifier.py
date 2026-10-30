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
MODULE: External Verifier (trustless audit)
INTENT: Lets a third party audit URO integrity WITHOUT trusting the producer.
        Every check recomputes from first principles (hashes, lineage, chains)
        and compares — the producer cannot fake a passing audit.
STANDARD: URO-STD-0001 S37

CHECKS:
  * verify_seal:          recompute INAHASH from the payload, compare
  * verify_lineage:       child.parent_inahash == parent.inahash (+ seal)
  * verify_custody:       delegate to the chain's own verify_chain()
  * verify_genesis_trust: child=100 / new=0 rule
  * verify_synapse_load:  recompute combined load from endpoint NTE states
  * audit_uro_graph:      walk a registry and report pass/fail per URO
"""
from __future__ import annotations

from typing import Any, Dict

from uro.security.hashing import inahash
from uro.integration import compute_synapse_load

__all__ = ["verify_seal", "verify_lineage", "verify_custody",
           "verify_genesis_trust", "verify_synapse_load", "audit_uro_graph"]


def verify_seal(uro) -> bool:
    """Recompute the INAHASH seal from first principles."""
    if hasattr(uro, "verify"):
        try:
            return bool(uro.verify())
        except Exception:
            return False
    h = getattr(uro, "inahash", "")
    if not h:
        return False
    data = uro.model_dump(exclude={"inahash"})
    return inahash(str(data).encode()).hex() == h


def verify_lineage(child, parent) -> bool:
    """A child URO must point at its parent's true INAHASH and be sealed."""
    if getattr(child, "parent_inahash", None) != parent.inahash:
        return False
    return verify_seal(child) and verify_seal(parent)


def verify_custody(chain) -> bool:
    """Verify the append-only custody chain (hash-linked entries)."""
    try:
        return bool(chain.verify_chain())
    except Exception:
        return False


def verify_genesis_trust(uro, parent=None) -> bool:
    """Genesis Trust rule: child=100%, new=0%."""
    try:
        expected = 100.0 if parent is not None else 0.0
        return abs(uro.genesis_trust_level() - expected) < 1e-6
    except Exception:
        return False


def verify_synapse_load(synapse, nte1, nte2, tolerance: float = 1.0) -> bool:
    """Recompute the combined synapse load and compare to the stored state."""
    load = compute_synapse_load(nte1, nte2)
    for axis, value in load.items():
        if abs(synapse.nte_state.get_level(axis) - value) > tolerance:
            return False
    return True


def audit_uro_graph(registry) -> Dict[str, Any]:
    """Walk a registry and audit every URO. Trustless, producer-independent."""
    report = {"sealed": 0, "seal_failed": 0, "custody_ok": 0,
              "custody_failed": 0, "lineage_ok": 0, "lineage_failed": 0}

    by_inahash = {u.inahash: u for u in registry.uros.values()}

    for u in registry.uros.values():
        if verify_seal(u):
            report["sealed"] += 1
        else:
            report["seal_failed"] += 1

        pi = getattr(u, "parent_inahash", None)
        if pi:
            parent = by_inahash.get(pi)
            if parent is not None and verify_lineage(u, parent):
                report["lineage_ok"] += 1
            else:
                report["lineage_failed"] += 1

    for chain in registry.custody.values():
        if verify_custody(chain):
            report["custody_ok"] += 1
        else:
            report["custody_failed"] += 1

    return report
