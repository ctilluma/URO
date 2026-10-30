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


# V.A.U.R.O.S AUTO-GENERATED
# ======================================================================= #
# MODULE INTENT: Standardized V.A.U.R.O.S. Cryptographic Engine (INAHASH).
# ======================================================================= #
import os
import hashlib
import blake3

def compute_inahash(msg: bytes) -> str:
    """INAHASH = Blake3-1024( SHA3-1024( MSG ) )"""
    sha3_digest = hashlib.sha3_512(msg).digest()
    return blake3.blake3(sha3_digest).hexdigest()

def generate_urid() -> str:
    """Generates a 512-bit compliant URID fragment."""
    return compute_inahash(os.urandom(64))[:64]
