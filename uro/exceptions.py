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
# MODULE START : uro.exceptions
# ---------------------------------------------------------------------
# FILE         : uro/exceptions.py
# PURPOSE      : Exception hierarchy. All errors derive from UROError.
# STANDARD     : URO-STD-0001 S11
# =====================================================================
"""Exception hierarchy for the URO reference implementation."""

from __future__ import annotations


class UROError(Exception):
    """Base class for all URO-related errors."""


class URIDError(UROError):
    """Malformed or out-of-range URID."""


class UROStructureError(UROError):
    """Structural invariant violation."""


class PathingError(UROError):
    """Path cannot be resolved or is invalid."""


class AssociationError(UROError):
    """Association cannot be formed or is invalid."""


class SecurityError(UROError):
    """Base class for security subsystem errors."""


class HashError(SecurityError):
    """Hashing operation failed."""


class EncryptionError(SecurityError):
    """Encryption/decryption failed."""


class IdentityError(SecurityError):
    """Identity verification failed."""


class ACLError(SecurityError):
    """ACL evaluation is invalid."""


class PolicyError(SecurityError):
    """Policy URO cannot be evaluated."""


class InterchangeError(UROError):
    """Serialization/deserialization failed."""


class ConnectorError(UROError):
    """Database / connector fault."""


class SchedulerError(UROError):
    """Scheduler fault."""


class TranslationError(UROError):
    """AUPI translation fault."""


class PaymentError(UROError):
    """InSPaneda payment fault."""


class OPARError(UROError):
    """OPAR lifecycle fault (observe/plan/act/review)."""


class SynapseError(UROError):
    """Synapse vector or modulation fault."""


class UROMemoryError(UROError):
    """Memory hierarchy or consolidation fault."""


class BootError(UROError):
    """System boot or self-check fault."""


class CustodyError(UROError):
    """Custody chain or 2-way exchange fault."""
class HeaderIntegrityError(UROStructureError):
    "Header integrity (Blake2-256) verification failed."


# =====================================================================
# MODULE END   : uro.exceptions
# =====================================================================
