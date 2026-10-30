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
URO Replication Protocol Messages
"""

import json
import time
import hashlib
import struct
from dataclasses import dataclass, asdict
from typing import Optional
from enum import Enum

class MessageType(Enum):
    HANDSHAKE = "handshake"
    REPLICATION_SYNC = "replication_sync"
    HEARTBEAT = "heartbeat"
    ACK = "ack"

class BackendType(Enum):
    POSTGRES = "postgres"
    KEYDB = "keydb"
    QDRANT = "qdrant"
    ELASTICSEARCH = "elasticsearch"

@dataclass
class UROHeader:
    sender_urid: str
    receiver_urid: str
    message_type: str
    backend_type: Optional[str]
    sequence_number: int
    timestamp: float
    payload_hash: str
    
    def to_dict(self) -> dict:
        return asdict(self)
        
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

@dataclass
class ReplicationMessage:
    header: UROHeader
    payload: bytes
    signature: str
    
    def serialize(self) -> bytes:
        header_json = self.header.to_json().encode('utf-8')
        header_len = len(header_json)
        sig_bytes = self.signature.encode('utf-8')
        sig_len = len(sig_bytes)
        
        return (
            struct.pack('>I', header_len) + header_json +
            self.payload +
            struct.pack('>I', sig_len) + sig_bytes
        )
        
    @classmethod
    def deserialize(cls, data: bytes) -> 'ReplicationMessage':
        offset = 0
        header_len = struct.unpack('>I', data[offset:offset+4])[0]
        offset += 4
        header_json = data[offset:offset+header_len].decode('utf-8')
        offset += header_len
        header_dict = json.loads(header_json)
        header = UROHeader(**header_dict)
        
        sig_len = struct.unpack('>I', data[-4:])[0]
        payload = data[offset:-4-sig_len]
        signature = data[-sig_len:].decode('utf-8')
        
        return cls(header=header, payload=payload, signature=signature)

def create_handshake(sender_urid: str, receiver_urid: str) -> ReplicationMessage:
    header = UROHeader(
        sender_urid=sender_urid,
        receiver_urid=receiver_urid,
        message_type=MessageType.HANDSHAKE.value,
        backend_type=None,
        sequence_number=0,
        timestamp=time.time(),
        payload_hash="handshake"
    )
    return ReplicationMessage(header=header, payload=b'', signature='')

def create_replication_sync(
    sender_urid: str,
    receiver_urid: str,
    backend_type: BackendType,
    sequence_number: int,
    payload: bytes
) -> ReplicationMessage:
    payload_hash = hashlib.sha256(payload).hexdigest()
    
    header = UROHeader(
        sender_urid=sender_urid,
        receiver_urid=receiver_urid,
        message_type=MessageType.REPLICATION_SYNC.value,
        backend_type=backend_type.value,
        sequence_number=sequence_number,
        timestamp=time.time(),
        payload_hash=payload_hash
    )
    return ReplicationMessage(header=header, payload=payload, signature='')
