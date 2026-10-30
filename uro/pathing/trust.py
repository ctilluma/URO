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
from typing import List, Dict, Any
from collections import Counter

class TrustValueProtocol:
    """
    URO S9.2 Trust Value Request Protocol.
    Evaluates responses from known UROs to determine path trust.
    """
    def __init__(self, trust_threshold: float = 75.0):
        self.trust_threshold = trust_threshold

    def evaluate_responses(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not responses:
            return {"status": "no_responses", "trust_points": 0}

        values = [r.get("value") for r in responses if "value" in r]
        if not values:
            return {"status": "no_values", "trust_points": 0}

        counts = Counter(values)
        total = len(values)
        majority_value, majority_count = counts.most_common(1)[0]
        majority_pct = (majority_count / total) * 100

        trust_points = 0
        status = "reanalyze"

        if majority_pct >= 100.0:
            status = "consensus"
            trust_points = 1
            actions = ["use_result"]
        elif majority_pct >= 90.0:
            status = "tv_check"
            trust_points = 0
            actions = ["use_high_tv_responder"]
        elif majority_pct >= 75.0:
            status = "deep_check"
            trust_points = 0
            actions = ["explore_hypotheses", "ask_minority_deep_check"]
        else:
            status = "reanalyze"
            trust_points = 0
            actions = ["reanalyze_query"]
        
        return {
            "status": status,
            "majority_value": majority_value,
            "majority_pct": majority_pct,
            "trust_points": trust_points,
            "total_responses": total,
            "actions": actions,
        }
