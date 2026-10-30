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
URO Replication Library
"""
from .protocol import (
    MessageType, BackendType, UROHeader, ReplicationMessage,
    create_handshake, create_replication_sync
)
from .base import ReplicationEmitter, ReplicationReceiver
from .gateway import GatewayReplicationHandler
from .postgres import PostgresReplicationEmitter, PostgresReplicationReceiver
from .keydb import KeyDBReplicationEmitter, KeyDBReplicationReceiver
from .qdrant import QdrantReplicationEmitter, QdrantReplicationReceiver

__all__ = [
    'MessageType', 'BackendType', 'UROHeader', 'ReplicationMessage',
    'create_handshake', 'create_replication_sync',
    'ReplicationEmitter', 'ReplicationReceiver', 'GatewayReplicationHandler',
    'PostgresReplicationEmitter', 'PostgresReplicationReceiver',
    'KeyDBReplicationEmitter', 'KeyDBReplicationReceiver',
    'QdrantReplicationEmitter', 'QdrantReplicationReceiver',
]

__version__ = '1.2.0'
