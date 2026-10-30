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
Base Replication Classes
"""

from abc import ABC, abstractmethod
from typing import Iterator
from .protocol import ReplicationMessage, BackendType
import logging

logger = logging.getLogger(__name__)

class ReplicationEmitter(ABC):
    def __init__(self, backend_type: BackendType, sender_urid: str, receiver_urid: str):
        self.backend_type = backend_type
        self.sender_urid = sender_urid
        self.receiver_urid = receiver_urid
        self.sequence_number = 0
        
    @abstractmethod
    def capture_changes(self) -> Iterator[bytes]:
        pass
        
    @abstractmethod
    def initialize(self):
        pass
        
    def emit_messages(self) -> Iterator[ReplicationMessage]:
        from .protocol import create_replication_sync
        
        self.initialize()
        
        for payload in self.capture_changes():
            self.sequence_number += 1
            message = create_replication_sync(
                sender_urid=self.sender_urid,
                receiver_urid=self.receiver_urid,
                backend_type=self.backend_type,
                sequence_number=self.sequence_number,
                payload=payload
            )
            yield message

class ReplicationReceiver(ABC):
    def __init__(self, backend_type: BackendType):
        self.backend_type = backend_type
        self.last_sequence = 0
        
    @abstractmethod
    def apply_change(self, payload: bytes):
        pass
        
    @abstractmethod
    def initialize(self):
        pass
        
    def receive_message(self, message: ReplicationMessage):
        if message.header.sequence_number <= self.last_sequence:
            logger.warning(f"Duplicate message: {message.header.sequence_number}")
            return
            
        self.initialize()
        self.apply_change(message.payload)
        self.last_sequence = message.header.sequence_number
