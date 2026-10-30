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


from __future__ import annotations

from typing import Any, Dict, List

from .hashutil import seal_object
from .timeutil import now_iso


class ImmutableLedger:
    """
    Append-only hash-chained ledger for ACL denials, control receipts, and effects.
    S14.4: history is append-only.
    """

    def __init__(self) -> None:
        self.entries: List[Dict[str, Any]] = []
        self._prev_hash = "0" * 128

    def append(self, event: str, payload: Any) -> Dict[str, Any]:
        body = {
            "seq": len(self.entries) + 1,
            "ts": now_iso(),
            "event": event,
            "payload": payload,
            "prev_hash": self._prev_hash,
        }
        digest, algorithm = seal_object(body)
        record = dict(body)
        record["hash"] = digest
        record["hash_algorithm"] = algorithm
        self.entries.append(record)
        self._prev_hash = digest
        return record
