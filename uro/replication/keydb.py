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
KeyDB (Redis Active-Active) Replication Handler
Implements URO-based replication for KeyDB multi-master setups.
"""

import redis
from .base import ReplicationEmitter, ReplicationReceiver
from .protocol import BackendType
import logging
import json
import time
import threading

logger = logging.getLogger(__name__)

class KeyDBReplicationEmitter(ReplicationEmitter):
    """
    Emits KeyDB changes via replication stream.
    KeyDB supports Active-Active multi-master replication.
    """
    
    def __init__(
        self,
        sender_urid: str,
        receiver_urid: str,
        host: str = "127.0.0.1",
        port: int = 6379,
        password: str = None
    ):
        super().__init__(BackendType.KEYDB, sender_urid, receiver_urid)
        self.host = host
        self.port = port
        self.password = password
        self.client = None
        self.replication_thread = None
        self.change_queue = []
        self.queue_lock = threading.Lock()
        
    def initialize(self):
        """Connect to KeyDB instance."""
        if self.client:
            return
            
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                decode_responses=True
            )
            # Test connection
            self.client.ping()
            logger.info("KeyDB replication emitter initialized")
        except Exception as e:
            logger.error(f"Failed to initialize KeyDB: {e}")
            raise
            
    def capture_changes(self):
        """
        Capture KeyDB changes using PSUBSCRIBE to keyspace notifications.
        Requires: notify-keyspace-events = "KEA" in redis.conf
        """
        if not self.client:
            self.initialize()
            
        # Enable keyspace notifications if not already enabled
        try:
            self.client.config_set('notify-keyspace-events', 'KEA')
        except redis.exceptions.ResponseError:
            logger.warning("Could not enable keyspace notifications (may be read-only)")
            
        pubsub = self.client.pubsub()
        pubsub.psubscribe('__keyevent@0__:*')
        
        try:
            for message in pubsub.listen():
                if message['type'] == 'pmessage':
                    event_type = message['channel'].split(':')[-1]
                    key = message['data']
                    
                    # Capture the change
                    change_record = {
                        'event': event_type,
                        'key': key,
                        'timestamp': time.time()
                    }
                    
                    # For SET operations, capture the value
                    if event_type in ('set', 'hset', 'lpush', 'rpush', 'sadd', 'zadd'):
                        try:
                            if event_type == 'set':
                                change_record['value'] = self.client.get(key)
                            elif event_type == 'hset':
                                change_record['value'] = self.client.hgetall(key)
                            elif event_type in ('lpush', 'rpush'):
                                change_record['value'] = self.client.lrange(key, 0, -1)
                            elif event_type == 'sadd':
                                change_record['value'] = list(self.client.smembers(key))
                            elif event_type == 'zadd':
                                change_record['value'] = self.client.zrange(key, 0, -1, withscores=True)
                        except Exception as e:
                            logger.error(f"Failed to capture value for {key}: {e}")
                            
                    payload = json.dumps(change_record).encode('utf-8')
                    yield payload
                    
        except Exception as e:
            logger.error(f"Error capturing KeyDB changes: {e}")
            raise

class KeyDBReplicationReceiver(ReplicationReceiver):
    """
    Applies KeyDB changes from replication messages.
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 6379, password: str = None):
        super().__init__(BackendType.KEYDB)
        self.host = host
        self.port = port
        self.password = password
        self.client = None
        
    def initialize(self):
        """Connect to local KeyDB."""
        if self.client:
            return
            
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                decode_responses=True
            )
            self.client.ping()
            logger.info("KeyDB replication receiver initialized")
        except Exception as e:
            logger.error(f"Failed to initialize KeyDB receiver: {e}")
            raise
            
    def apply_change(self, payload: bytes):
        """Apply a KeyDB change."""
        if not self.client:
            self.initialize()
            
        try:
            change = json.loads(payload.decode('utf-8'))
            event = change['event']
            key = change['key']
            value = change.get('value')
            
            if event == 'set':
                self.client.set(key, value)
            elif event == 'del':
                self.client.delete(key)
            elif event == 'hset':
                if value:
                    self.client.hset(key, mapping=value)
            elif event == 'hdel':
                if value:
                    self.client.hdel(key, *value.keys())
            elif event == 'lpush':
                if value:
                    self.client.lpush(key, *value)
            elif event == 'rpush':
                if value:
                    self.client.rpush(key, *value)
            elif event == 'lpop':
                self.client.lpop(key)
            elif event == 'rpop':
                self.client.rpop(key)
            elif event == 'sadd':
                if value:
                    self.client.sadd(key, *value)
            elif event == 'srem':
                if value:
                    self.client.srem(key, *value)
            elif event == 'zadd':
                if value:
                    for member, score in value:
                        self.client.zadd(key, {member: score})
            elif event == 'expire':
                if value:
                    self.client.expire(key, int(value))
                    
            logger.debug(f"Applied KeyDB change: {event} on {key}")
            
        except Exception as e:
            logger.error(f"Error applying KeyDB change: {e}")
            raise
