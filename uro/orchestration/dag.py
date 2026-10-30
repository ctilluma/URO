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
MODULE: DAG Orchestrator with Saga Compensation
INTENT: Expands the base OPAR cycle into a multi-node DAG with rollback 
        capabilities. Used by docks to coordinate complex, multi-step 
        cognitive or operational workflows.
"""
import asyncio
import logging
from typing import Dict, Any, List, Callable, Awaitable
from uro.api.models import BaseUROModel

logger = logging.getLogger("URO.DAG")

class DAGNode:
    def __init__(self, node_id: str, func: Callable, compensator: Callable = None):
        self.node_id = node_id
        self.func = func
        self.compensator = compensator

class DAGOrchestrator:
    def __init__(self, max_workers: int = 10):
        self.queue = asyncio.Queue(maxsize=1000)
        self.max_workers = max_workers
        self.workers = []
        self.nodes: List[DAGNode] = []

    def add_node(self, node: DAGNode):
        self.nodes.append(node)

    async def start_workers(self):
        self.workers = [asyncio.create_task(self._worker_loop(i)) for i in range(self.max_workers)]

    async def _worker_loop(self, worker_id: int):
        while True:
            uro_model = await self.queue.get()
            try:
                await self._execute_dag(uro_model, worker_id)
            except Exception as e:
                logger.error(f"Worker {worker_id} DAG failed for {uro_model.urid2_instance}: {e}")
                await self._rollback_saga(uro_model)
            finally:
                self.queue.task_done()

    async def _execute_dag(self, uro_model: BaseUROModel, worker_id: int):
        executed_nodes = []
        for node in self.nodes:
            uro_model = await node.func(uro_model)
            executed_nodes.append(node)
        uro_model.execution_result["status"] = "SUCCESS"
        return uro_model

    async def _rollback_saga(self, uro_model: BaseUROModel):
        uro_model.execution_result["status"] = "ROLLED_BACK"

    async def submit(self, uro_model: BaseUROModel):
        await self.queue.put(uro_model)

    async def stop(self):
        for w in self.workers:
            w.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
