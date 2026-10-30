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


"""V.A.U.R.O.S. Entanglement Synapse Graph (Phase 3b.2).

Links belief states (claim hashes) so a belief-strength change in one propagates
an attenuated, provenance-tracked nudge to its neighbors.

Design laws:
- Propagation is belief-transfer, NOT evidence creation: nudges are capped and
  saturate by ORIGINAL source, so entanglement can never amplify a flood or
  double-count one origin's signal across multiple paths.
- 'supports' synapses co-vary; 'contradicts' synapses anti-covary.
- Attenuation: nudge = delta * synapse_weight; below min_delta, propagation stops.
- Cycle-safe (visited set) and depth-limited (max_depth).
"""
from typing import Dict, Any
from uro.belief_state import new_belief, nudge_belief

DEFAULT_MAX_DEPTH = 2
DEFAULT_MIN_DELTA = 0.01


def new_synapse_graph() -> Dict[str, Any]:
    return {"edges": {}}


def _edge_key(a, b) -> str:
    return "|".join(sorted([str(a), str(b)]))


def add_synapse(graph, a, b, weight, relation="supports"):
    """Add an undirected synapse. weight clamped to [0,1]."""
    if relation not in ("supports", "contradicts"):
        raise ValueError(f"relation must be 'supports' or 'contradicts', got {relation!r}")
    w = max(0.0, min(1.0, float(weight)))
    graph["edges"][_edge_key(a, b)] = {"a": str(a), "b": str(b), "weight": w, "relation": relation}
    return graph


def neighbors(graph, node):
    """Yield (other_node, weight, relation) for every synapse touching node."""
    node = str(node)
    out = []
    for e in graph["edges"].values():
        if e["a"] == node:
            out.append((e["b"], e["weight"], e["relation"]))
        elif e["b"] == node:
            out.append((e["a"], e["weight"], e["relation"]))
    return out


def propagate_delta(graph, beliefs, source, delta,
                    max_depth=DEFAULT_MAX_DEPTH, min_delta=DEFAULT_MIN_DELTA):
    """Propagate a belief-strength delta from source outward through the graph.

    beliefs: dict claim_hash -> belief dict. Returns a NEW beliefs dict.
    Provenance = source: every nudge saturates by the ORIGINAL source, so one
    origin's signal is counted once per node even across multi-path routes.
    """
    source = str(source)
    updated = {k: dict(v) for k, v in beliefs.items()}
    if source not in updated:
        updated[source] = new_belief(source)
    _propagate(updated, graph, current=source, origin=source, delta=float(delta),
               depth=0, max_depth=max_depth, min_delta=min_delta, visited={source})
    return updated


def _propagate(beliefs, graph, current, origin, delta, depth, max_depth, min_delta, visited):
    if depth >= max_depth:
        return
    for (nb, weight, relation) in neighbors(graph, current):
        nud = delta * weight
        if relation == "contradicts":
            nud = -nud
        if abs(nud) < min_delta:
            continue
        if nb in visited:
            continue
        visited.add(nb)
        if nb not in beliefs:
            beliefs[nb] = new_belief(nb)
        beliefs[nb] = nudge_belief(beliefs[nb], source_tag=origin, signed_weight=nud)
        _propagate(beliefs, graph, current=nb, origin=origin, delta=nud,
                   depth=depth + 1, max_depth=max_depth, min_delta=min_delta, visited=visited)
