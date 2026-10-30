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
# MODULE START : uro.security.custody
# ---------------------------------------------------------------------
# FILE         : uro/security/custody.py
# PURPOSE      : Custody send chain and 2-way exchange protocol over keyed
#                INAHASH MACs (RFC 63); PKI signature binding deferred to
#                the signature-consolidation pass (ADR-024).
# STANDARD     : URO-STD-0001 S9
# =====================================================================
"Custody send chain and 2-way exchange protocol (RFC 63)."

from __future__ import annotations

from typing import Any, Dict, List

from uro.security.hashing import inahash, sha512

__all__ = ["send_custody", "two_way_exchange", "verify_two_way"]


def _mac(key: bytes, blob: bytes) -> str:
    "PURPOSE: Keyed INAHASH MAC used as the custody signature."
    return inahash(key + blob).hex()


def send_custody(chain: List[Dict[str, Any]], signer_key: bytes, obj_bytes: bytes) -> Dict[str, Any]:
    "PURPOSE: RFC 63.1: append trusted signature with hash; return trust receipt."
    entry = {"sig": _mac(signer_key, obj_bytes), "hash": sha512(obj_bytes).hex()}
    chain.append(entry)
    return {"trust_received_index": len(chain) - 1, "hash_of_trust": entry["hash"]}


def two_way_exchange(sender_key: bytes, receiver_key: bytes,
                     snd_bytes: bytes, rcv_bytes: bytes) -> Dict[str, Any]:
    "PURPOSE: RFC 63.2: sender signs RCV, receiver signs SND."
    return {"sender_signs_rcv": _mac(sender_key, rcv_bytes),
            "receiver_signs_snd": _mac(receiver_key, snd_bytes)}


def verify_two_way(sender_key: bytes, receiver_key: bytes, snd_bytes: bytes,
                   rcv_bytes: bytes, sigs: Dict[str, str]) -> bool:
    "PURPOSE: Recompute both cross-signatures to establish trusted exchange."
    return (sigs.get("sender_signs_rcv") == _mac(sender_key, rcv_bytes)
            and sigs.get("receiver_signs_snd") == _mac(receiver_key, snd_bytes))
# =====================================================================
# MODULE END   : uro.security.custody
# =====================================================================
