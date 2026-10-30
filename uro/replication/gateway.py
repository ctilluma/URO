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
Gateway Replication Handler
"""

import logging
from typing import Callable
from .protocol import ReplicationMessage, MessageType
from .base import ReplicationReceiver

logger = logging.getLogger(__name__)

class GatewayReplicationHandler:
    def __init__(self, local_urid: str, inahash_validator: Callable):
        self.local_urid = local_urid
        self.inahash_validator = inahash_validator
        self.receivers: dict[str, ReplicationReceiver] = {}
        
    def register_receiver(self, backend_type: str, receiver: ReplicationReceiver):
        self.receivers[backend_type] = receiver
        logger.info(f"Registered receiver for backend: {backend_type}")
        
    def validate_and_route(self, message: ReplicationMessage) -> bool:
        if message.header.receiver_urid != self.local_urid:
            logger.warning(f"Message not for us: {message.header.receiver_urid}")
            return False
            
        if not self.inahash_validator(message):
            logger.warning("INAHASH validation failed")
            return False
            
        if message.header.message_type != MessageType.REPLICATION_SYNC.value:
            return False
            
        backend_type = message.header.backend_type
        if backend_type not in self.receivers:
            logger.warning(f"No receiver for backend: {backend_type}")
            return False
            
        try:
            self.receivers[backend_type].receive_message(message)
            return True
        except Exception as e:
            logger.error(f"Error routing to {backend_type}: {e}")
            return False
