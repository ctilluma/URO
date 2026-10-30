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
URO TCP Transport Layer
Handles reliable TCP connections with URO message framing and cryptographic validation.
"""

import socket
import struct
import threading
import logging
from typing import Callable, Optional, Tuple
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

MAGIC = b'URO1'
HEADER_SIZE = 8
MAX_MESSAGE_SIZE = 100 * 1024 * 1024

@dataclass
class ConnectionInfo:
    peer_urid: str
    peer_address: Tuple[str, int]
    validated: bool = False
    last_seen: float = 0.0

class UROTransport:
    """TCP transport with URO framing and peer validation."""
    
    def __init__(self, host: str, port: int, urid: str, inahash_validator: Callable):
        self.host = host
        self.port = port
        self.urid = urid
        self.inahash_validator = inahash_validator
        self.server_socket: Optional[socket.socket] = None
        self.connections: dict[socket.socket, ConnectionInfo] = {}
        self.running = False
        self.lock = threading.Lock()
        
    def start(self):
        """Start listening for incoming connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        logger.info(f"URO Transport listening on {self.host}:{self.port}")
        
        accept_thread = threading.Thread(target=self._accept_loop, daemon=True)
        accept_thread.start()
        
    def stop(self):
        """Stop the transport and close all connections."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        
        with self.lock:
            for sock in list(self.connections.keys()):
                try:
                    sock.close()
                except:
                    pass
            self.connections.clear()
            
    def _accept_loop(self):
        """Accept incoming connections."""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                logger.info(f"Accepted connection from {address}")
                
                handler = threading.Thread(
                    target=self._handle_connection,
                    args=(client_socket, address),
                    daemon=True
                )
                handler.start()
            except socket.error as e:
                if self.running:
                    logger.error(f"Accept error: {e}")
                    
    def _handle_connection(self, client_socket: socket.socket, address: Tuple[str, int]):
        """Handle an incoming connection."""
        conn_info = ConnectionInfo(
            peer_urid="unknown",
            peer_address=address,
            validated=False,
            last_seen=time.time()
        )
        
        with self.lock:
            self.connections[client_socket] = conn_info
            
        try:
            handshake_uro = self._receive_message(client_socket)
            if not handshake_uro:
                logger.warning(f"Handshake failed from {address}")
                return
                
            if not self._validate_handshake(handshake_uro, conn_info):
                logger.warning(f"Handshake validation failed from {address}")
                return
                
            conn_info.validated = True
            logger.info(f"Validated peer {conn_info.peer_urid} from {address}")
            
            while self.running:
                uro_message = self._receive_message(client_socket)
                if not uro_message:
                    break
                conn_info.last_seen = time.time()
                
        except Exception as e:
            logger.error(f"Connection handler error: {e}")
        finally:
            with self.lock:
                if client_socket in self.connections:
                    del self.connections[client_socket]
            try:
                client_socket.close()
            except:
                pass
                
    def _receive_message(self, sock: socket.socket) -> Optional[bytes]:
        """Receive a complete URO message."""
        try:
            header = self._recv_exact(sock, HEADER_SIZE)
            if not header:
                return None
                
            magic, length = struct.unpack('>4sI', header)
            if magic != MAGIC:
                logger.error("Invalid magic bytes")
                return None
                
            if length > MAX_MESSAGE_SIZE:
                logger.error(f"Message too large: {length}")
                return None
                
            payload = self._recv_exact(sock, length)
            return payload
            
        except Exception as e:
            logger.error(f"Receive error: {e}")
            return None
            
    def _recv_exact(self, sock: socket.socket, size: int) -> Optional[bytes]:
        """Receive exactly N bytes."""
        data = b''
        while len(data) < size:
            try:
                chunk = sock.recv(size - len(data))
                if not chunk:
                    return None
                data += chunk
            except socket.error:
                return None
        return data
        
    def send_message(self, sock: socket.socket, uro_bytes: bytes) -> bool:
        """Send a URO message."""
        try:
            length = len(uro_bytes)
            header = struct.pack('>4sI', MAGIC, length)
            sock.sendall(header + uro_bytes)
            return True
        except Exception as e:
            logger.error(f"Send error: {e}")
            return False
            
    def _validate_handshake(self, uro_bytes: bytes, conn_info: ConnectionInfo) -> bool:
        """Validate the initial handshake URO."""
        try:
            if b'handshake' not in uro_bytes[:100]:
                return False
                
            if not self.inahash_validator(uro_bytes):
                return False
                
            conn_info.peer_urid = "peer_gateway"
            return True
            
        except Exception as e:
            logger.error(f"Handshake validation error: {e}")
            return False

    def get_validated_connections(self) -> list[ConnectionInfo]:
        """Get list of validated peer connections."""
        with self.lock:
            return [info for info in self.connections.values() if info.validated]
