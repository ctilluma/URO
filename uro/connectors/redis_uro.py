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


"""
MODULE: Redis URO Connector (Short-Term Memory)
INTENT: Wraps Redis operations as URO interactions for rapid, ephemeral 
        cognitive state retention and queueing.
"""
import json
from typing import Optional, Any
from uro.core.uro import URO
from uro.core.urid import URID
from uro.api.models import BaseUROModel

class RedisUROConnector:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def store_short_term(self, uro_model: BaseUROModel, ttl: int = 3600) -> None:
        key = f"uro:stm:{uro_model.urid2_instance}"
        await self.redis.set(key, uro_model.model_dump_json(), ex=ttl)

    async def retrieve_short_term(self, urid2_instance: str) -> Optional[BaseUROModel]:
        key = f"uro:stm:{urid2_instance}"
        data = await self.redis.get(key)
        if data:
            return BaseUROModel.model_validate_json(data)
        return None
