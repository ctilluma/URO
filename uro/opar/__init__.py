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
# MODULE START : uro.opar
# ---------------------------------------------------------------------
# FILE         : uro/opar/__init__.py
# PURPOSE      : Canonical OPAR-24 package exports (RFC 10-17) plus
#                legacy operations-API re-exports for compatibility.
# STANDARD     : URO-STD-0001 OPAR-24
# =====================================================================
"Canonical OPAR-24 package (RFC 10-17)."
from uro.opar.stages import STAGES, StageResult
from uro.opar.base import OPARBase, nte24, BASELINE
from uro.opar.protocol import OPARCapability
from uro.opar.grounding import GroundingResult, LocalGroundingEngine, get_grounding_engine
from uro.opar.compliance import checklist, run_conformance, source_has_no_op_stub
__all__ = ["STAGES", "StageResult", "OPARBase", "nte24", "BASELINE",
           "OPARCapability", "GroundingResult", "LocalGroundingEngine",
           "get_grounding_engine", "checklist", "run_conformance",
           "source_has_no_op_stub"]
# Legacy operations API (pre-canonical name collision), kept for compat.
try:
    from uro.opar_operations_legacy import (OPAREngine, OPARRequest, OPARResponse,
        OPARContext, OPAROperationType, OPARStatus)
    __all__ += ["OPAREngine", "OPARRequest", "OPARResponse", "OPARContext",
                "OPAROperationType", "OPARStatus"]
except Exception:
    pass
# =====================================================================
# MODULE END   : uro.opar
# =====================================================================
