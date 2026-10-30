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


"""Canonical dock manifest for the V.A.U.R.O.S. swarm.

Auto-generated from docker-compose.yml. Provides the authoritative list of
dock hostnames the Observer should monitor, parameterized by deployment profile.
Infrastructure storage services (infra_postgres/redis/qdrant) are excluded since
they don't expose HTTP health APIs.
"""
from typing import List

# Base dock names that take a profile suffix: {base}_{profile}
DOCK_BASES = [
    "aegis",
    "architect",
    "auction",
    "autodidact",
    "bazaar",
    "boardroom",
    "bursar",
    "chaos",
    "chaos_findings",
    "chronos",
    "coder",
    "codereview",
    "cognitive",
    "concierge",
    "coordinator",
    "dast",
    "envoy",
    "finance",
    "foundry",
    "gateway",
    "gnosis",
    "helix",
    "herald",
    "host_controller",
    "iast",
    "intermediary_dock",
    "lineage",
    "llm_bridge",
    "logs",
    "loom",
    "lucid",
    "memory",
    "metabolism",
    "morphic_mesh",
    "nexus",
    "observer",
    "oracle",
    "phoenix",
    "provisioner",
    "qdrant",
    "redis",
    "refinery",
    "registry",
    "rosetta",
    "sast",
    "scholar",
    "sensorium",
    "sentinel",
    "sigil",
    "threat_intelligence_vault",
    "twin",
]

# Singleton services with no profile suffix (shared across profiles)
SINGLETON_SERVICES = [
    "airlock",
    "data_shunter",
]

# HTTP paths to try when probing dock health (different docks use different paths)
HEALTH_PATHS = ["/health", "/_health", "/ready", "/status", "/memory/status"]


def get_dock_hostnames(profile: str = "prod") -> List[str]:
    """Return all dock hostnames for a given deployment profile.

    Docks follow the {base}_{profile} convention (e.g. cognitive_prod).
    Singletons (airlock, data_shunter) have no suffix.
    """
    hostnames = [f"{base}_{profile}" for base in DOCK_BASES]
    hostnames.extend(SINGLETON_SERVICES)
    return hostnames
