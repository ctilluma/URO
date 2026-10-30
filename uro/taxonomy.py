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
# MODULE START : uro.taxonomy
# ---------------------------------------------------------------------
# FILE         : uro/taxonomy.py
# PURPOSE      : Canonical taxonomy of well-known URO namespaces. Because
#                everything is a URO, named object types are registered
#                as first-class template UROs in a shared UROSpace.
# STANDARD     : URO-STD-0001 S12
# =====================================================================
"""Canonical taxonomy of well-known URO namespaces."""

from __future__ import annotations

from uro.core.space import UROSpace
from uro.core.uro import URO

__all__ = ["WELL_KNOWN_TYPES", "build_taxonomy"]

WELL_KNOWN_TYPES = (
    "PKI.PUBK", "PKI.SIGN", "INAHASH",
    "TIME.SECONDS", "TIME.DATE",
    "CONN.DBSE", "CONN.DBSE.TABL", "CONN.DBSE.SQL.INSERT",
    "CONN.DBSE.SQL.DELETE", "CONN.DBSE.SQL.SELECT", "CONN.DBSE.SQL.WHERE",
    "REL.ASSOCIATION", "REL.PATH",
    "PHASE.OPAR",
    "PAY.INSPANEDA", "PAY.INSPATIVO", "PAY.LEDGER", "PAY.ACCT",
    "AUPI.TRANSLATOR",
    "NTE.SERATONIN", "NTE.EPINEPHRINE", "NTE.OXYTOCIN",
    "NTE.NOREPINEPHRINE", "NTE.ACETYLCHOLINE", "NTE.GABA",
    "NTE.DOPAMINE", "NTE.CANNABINOID",
    "PHYS.MAGLEV.REGIONAL", "PHYS.MAGLEV.INTERNATIONAL",
    "PHYS.ROBOTICS", "PHYS.WETWARE", "PHYS.WATER.BIOVIRON",
    "META.NOTHING", "META.EVERYTHING",
)


def build_taxonomy() -> UROSpace:
    """Build a UROSpace populated with the well-known type templates."""
    space = UROSpace(name="taxonomy")
    space.register(URO.nothing())
    space.register(URO.everything())
    for name in WELL_KNOWN_TYPES:
        template = URO.new(payload={"type": name})
        template._meta["name"] = name  # noqa: SLF001 - taxonomy tag
        space.register(template)
    return space
# =====================================================================
# MODULE END   : uro.taxonomy
# =====================================================================
