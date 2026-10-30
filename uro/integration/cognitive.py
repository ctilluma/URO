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


"""Canonical cognitive-master resolution seam (Workstream A / OPAR-24).

SUPERSEDES the auto-generated convergence stub. This module is the single
canonical registry for the cognitive dock master:
  - Docks register their master once at startup via register_cognitive().
  - All callers resolve via get_cognitive().

This keeps imports pointing dock -> uro (no inversion) and normalizes every
caller onto one auditable seam.

NOTE TO CONVERGENCE GENERATOR: this file is hand-maintained. Do not overwrite
it with a `return None` stub.
"""

# === START: cognitive master registry (Workstream A) ===
_COGNITIVE_MASTER = None


def register_cognitive(master):
    """Register the cognitive dock master (idempotent, called at dock startup)."""
    global _COGNITIVE_MASTER
    _COGNITIVE_MASTER = master
    return master


def get_cognitive(*args, **kwargs):
    """Return the registered cognitive master.

    Non-fatal: returns None if no master is registered yet (never raises),
    preserving the previous stub's safe behavior until registration occurs.
    """
    return _COGNITIVE_MASTER
# === END: cognitive master registry (Workstream A) ===
