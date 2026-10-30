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


#!/usr/bin/env python3
"""
Qdrant (Vector State) Replication Handler
Implements URO-based replication for Qdrant vector databases.
Uses a high-water mark and state-tracking approach to capture point mutations.
"""

import json
import time
import logging
import hashlib
import threading
from typing import Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, PointIdsList

from .base import ReplicationEmitter, ReplicationReceiver
from .protocol import BackendType

logger = logging.getLogger(__name__)

class QdrantReplicationEmitter(ReplicationEmitter):
    """
    Emits Qdrant changes by tracking point state (upserts and deletes).
    """
    
    def __init__(
        self,
        sender_urid: str,
        receiver_urid: str,
        collection_name: str,
        host: str = "127.0.0.1",
        port: int = 6333,
        poll_interval: float = 1.0,
        batch_size: int = 100
    ):
        super().__init__(BackendType.QDRANT, sender_urid, receiver_urid)
        self.collection_name = collection_name
        self.host = host
        self.port = port
        self.poll_interval = poll_interval
        self.batch_size = batch_size
        self.client: Optional[QdrantClient] = None
        
        # State tracking: maps point_id -> payload_hash
        self.known_state: Dict[Any, str] = {}
        self.known_ids: set = set()
        self.state_lock = threading.Lock()
        
    def initialize(self):
        """Connect to Qdrant and initialize state tracking."""
        if self.client:
            return
            
        try:
            self.client = QdrantClient(host=self.host, port=self.port)
            collections = [c.name for c in self.client.get_collections().collections]
            if self.collection_name not in collections:
                raise ValueError(f"Collection {self.collection_name} not found")
                
            logger.info(f"Qdrant emitter initialized for collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant emitter: {e}")
            raise
            
    def _compute_hash(self, point: PointStruct) -> str:
        """Compute a hash of the point's payload and vector to detect updates."""
        data = {"vector": point.vector, "payload": point.payload}
        return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()

    def capture_changes(self):
        """
        Capture Qdrant changes by polling and comparing state.
        Yields JSON-encoded batches of upserts and deletes.
        """
        if not self.client:
            self.initialize()
            
        try:
            while True:
                current_ids = set()
                upserts = []
                
                offset = None
                while True:
                    points, next_offset = self.client.scroll(
                        collection_name=self.collection_name,
                        limit=self.batch_size,
                        offset=offset,
                        with_payload=True,
                        with_vectors=True
                    )
                    
                    if not points:
                        break
                        
                    for point in points:
                        current_ids.add(point.id)
                        current_hash = self._compute_hash(point)
                        
                        with self.state_lock:
                            prev_hash = self.known_state.get(point.id)
                            
                        if prev_hash != current_hash:
                            upserts.append({
                                "id": point.id,
                                "vector": point.vector,
                                "payload": point.payload
                            })
                            with self.state_lock:
                                self.known_state[point.id] = current_hash
                                
                    if next_offset is None:
                        break
                    offset = next_offset
                    
                # Detect deletes
                deletes = []
                with self.state_lock:
                    deleted_ids = self.known_ids - current_ids
                    for did in deleted_ids:
                        deletes.append(did)
                        del self.known_state[did]
                    self.known_ids = current_ids
                    
                if upserts or deletes:
                    change_record = {
                        "collection": self.collection_name,
                        "upserts": upserts,
                        "deletes": deletes,
                        "timestamp": time.time()
                    }
                    yield json.dumps(change_record).encode('utf-8')
                    
                time.sleep(self.poll_interval)
                
        except Exception as e:
            logger.error(f"Error capturing Qdrant changes: {e}")
            raise

class QdrantReplicationReceiver(ReplicationReceiver):
    """
    Applies Qdrant changes from replication messages.
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 6333):
        super().__init__(BackendType.QDRANT)
        self.host = host
        self.port = port
        self.client: Optional[QdrantClient] = None
        
    def initialize(self):
        if not self.client:
            try:
                self.client = QdrantClient(host=self.host, port=self.port)
            except Exception as e:
                logger.error(f"Failed to initialize Qdrant receiver: {e}")
                raise
            
    def apply_change(self, payload: bytes):
        if not self.client:
            self.initialize()
            
        try:
            change = json.loads(payload.decode('utf-8'))
            collection = change["collection"]
            upserts = change.get("upserts", [])
            deletes = change.get("deletes", [])
            
            if upserts:
                points = [
                    PointStruct(id=p["id"], vector=p["vector"], payload=p["payload"])
                    for p in upserts
                ]
                self.client.upsert(collection_name=collection, points=points)
                
            if deletes:
                self.client.delete(
                    collection_name=collection,
                    points_selector=PointIdsList(points=deletes)
                )
                
        except Exception as e:
            logger.error(f"Error applying Qdrant changes: {e}")
            raise
