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
# MODULE START : uro.learning
# ---------------------------------------------------------------------
# FILE         : uro/learning/__init__.py
# PURPOSE      : Open-source learning primitives (RFC 89-100) per ADR-021.
# STANDARD     : URO-STD-0001 S10
# =====================================================================
"Learning primitives package (RFC 89-100, open-source layer per ADR-021)."
from uro.learning.primitives import (CauseEffectLedger, ExperimentLog,
    FeedbackLoop, ObservationRecord, SequenceTracker, segment_by_gaps,
    correlate_gaps, differentiate, correlate)
from uro.learning.dicho import DichoRegistry
from uro.learning.action_uro import ActionType, ActionCost, ActionURO
from uro.learning.attention import AttentionManager, INTERNAL_STREAM
from uro.learning.aloneness import AlonenessPropagator
from uro.learning.cas_loop import CASLoop
__all__ = ["CauseEffectLedger", "ExperimentLog", "FeedbackLoop",
           "ObservationRecord", "SequenceTracker", "segment_by_gaps",
           "correlate_gaps", "differentiate", "correlate", "DichoRegistry",
           "ActionType", "ActionCost", "ActionURO", "AttentionManager",
           "INTERNAL_STREAM", "AlonenessPropagator", "CASLoop"]
# =====================================================================
# MODULE END   : uro.learning
# =====================================================================
