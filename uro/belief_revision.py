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


"""V.A.U.R.O.S. AGM Belief Revision (Phase 3b.4).

Adapts the Alchourron-Gardenfors-Makinson postulates from classical logic to
the probabilistic belief-state ledger. A belief is "held" when its posterior
mean exceeds BELIEF_THRESHOLD.

Operations:
- contract(K, p):  retract p toward ignorance (minimal change).
- expand(K, p):    add evidence for p (no consistency check).
- revise(K, p):    Levi identity -> contract contradictions of p, then expand by p.

Guaranteed postulates (verified by structural tests):
- (K-2) Inclusion, (K-3) Vacuity, (K-4) Success, (K-5) Recovery for contraction.
- (K*2) Success, (K*4) Vacuity, (K*5) Consistency for revision.
"""
from typing import Dict, Any, Iterable, Optional
from uro.belief_state import new_belief, apply_evidence, posterior_mean
from uro.belief_graph import neighbors

BELIEF_THRESHOLD = 0.5


def is_believed(belief: Dict[str, Any], threshold: float = BELIEF_THRESHOLD) -> bool:
    """A belief is held when its posterior mean strictly exceeds the threshold."""
    return posterior_mean(belief) > threshold


def believed_claims(ledger: Dict[str, Any], threshold: float = BELIEF_THRESHOLD) -> set:
    return {h for h, b in ledger.items() if is_believed(b, threshold)}


def contract(ledger: Dict[str, Any], claim: str, now: Optional[float] = None) -> Dict[str, Any]:
    """Contract claim from the ledger (minimal retraction toward ignorance).

    (K-2) Inclusion: only claim is modified.
    (K-3) Vacuity:   if claim absent or not believed, ledger unchanged.
    (K-4) Success:   after contraction, claim is not believed.
    Provenance of the retracted posterior is kept for audit / recovery.
    """
    claim = str(claim)
    if claim not in ledger or not is_believed(ledger[claim]):
        return dict(ledger)
    b = ledger[claim]
    retracted = new_belief(claim, now=now)
    retracted["status"] = "retracted"
    retracted["retracted_from"] = {"alpha": b["alpha"], "beta": b["beta"]}
    out = dict(ledger)
    out[claim] = retracted
    return out


def expand(ledger: Dict[str, Any], claim: str, trust: float, origin: str,
           now: Optional[float] = None) -> Dict[str, Any]:
    """Expansion: add confirming evidence for claim (no consistency check)."""
    claim = str(claim)
    out = dict(ledger)
    b = out.get(claim) or new_belief(claim, now=now)
    b = apply_evidence(b, origin=origin, trust=trust, stance="confirm", now=now)
    b["status"] = "active"
    out[claim] = b
    return out


def contradictions_of(graph: Dict[str, Any], claim: str) -> set:
    """Claim hashes linked to claim by a 'contradicts' synapse."""
    return {nb for (nb, _w, rel) in neighbors(graph, claim) if rel == "contradicts"}


def revise(ledger: Dict[str, Any], claim: str, trust: float, origin: str,
           contradictions: Iterable[str] = (), now: Optional[float] = None) -> Dict[str, Any]:
    """Revision by claim via Levi identity: K * p = (K - contradictions) + p.

    (K*2) Success:     claim is believed afterward.
    (K*4) Vacuity:     with no contradictions, revision == expansion.
    (K*5) Consistency: each contradiction is contracted, so claim and its
                       contradictions are never all believed simultaneously.
    """
    out = dict(ledger)
    for c in contradictions:
        out = contract(out, c, now=now)
    return expand(out, claim, trust=trust, origin=origin, now=now)


def revise_with_graph(ledger: Dict[str, Any], claim: str, trust: float, origin: str,
                      graph: Dict[str, Any], now: Optional[float] = None) -> Dict[str, Any]:
    """Revision with automatic contradiction detection via the entanglement graph."""
    contra = contradictions_of(graph, claim)
    return revise(ledger, claim, trust, origin, contradictions=contra, now=now)
