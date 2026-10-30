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
PostgreSQL Logical Replication Handler
"""

import psycopg2
from .base import ReplicationEmitter, ReplicationReceiver
from .protocol import BackendType
import logging
import json

logger = logging.getLogger(__name__)

class PostgresReplicationEmitter(ReplicationEmitter):
    def __init__(self, sender_urid: str, receiver_urid: str, dsn: str, slot_name: str = "uro_replication_slot"):
        super().__init__(BackendType.POSTGRES, sender_urid, receiver_urid)
        self.dsn = dsn
        self.slot_name = slot_name
        self.conn = None
        
    def initialize(self):
        if self.conn:
            return
            
        try:
            self.conn = psycopg2.connect(self.dsn)
            self.conn.autocommit = True
            
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_replication_slots WHERE slot_name = %s", (self.slot_name,))
                if not cur.fetchone():
                    cur.execute("SELECT pg_create_logical_replication_slot(%s, 'test_decoding')", (self.slot_name,))
                    
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise
            
    def capture_changes(self):
        if not self.conn:
            self.initialize()
            
        try:
            with self.conn.cursor() as cur:
                while True:
                    cur.execute("SELECT data FROM pg_logical_slot_peek_changes(%s, NULL, NULL)", (self.slot_name,))
                    changes = cur.fetchall()
                    
                    if changes:
                        payload = json.dumps([row[0] for row in changes]).encode('utf-8')
                        yield payload
                        cur.execute("SELECT pg_logical_slot_get_changes(%s, NULL, NULL)", (self.slot_name,))
                    else:
                        import time
                        time.sleep(0.1)
                        
        except Exception as e:
            logger.error(f"Error capturing changes: {e}")
            raise

class PostgresReplicationReceiver(ReplicationReceiver):
    def __init__(self, dsn: str):
        super().__init__(BackendType.POSTGRES)
        self.dsn = dsn
        self.conn = None
        
    def initialize(self):
        if self.conn:
            return
            
        try:
            self.conn = psycopg2.connect(self.dsn)
            self.conn.autocommit = False
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise
            
    def apply_change(self, payload: bytes):
        if not self.conn:
            self.initialize()
            
        try:
            change_records = json.loads(payload.decode('utf-8'))
            
            with self.conn.cursor() as cur:
                for change_str in change_records:
                    parts = change_str.split(':')
                    if len(parts) < 3:
                        continue
                        
                    table_name = parts[0].strip()
                    action = parts[1].strip()
                    columns_str = parts[2].strip()
                    
                    columns = {}
                    if columns_str:
                        for col_pair in columns_str.split(','):
                            if '=' in col_pair:
                                col_name, col_value = col_pair.split('=', 1)
                                columns[col_name.strip()] = col_value.strip().strip("'")
                                
                    if action == 'INSERT':
                        cols = ', '.join(columns.keys())
                        placeholders = ', '.join(['%s'] * len(columns))
                        values = list(columns.values())
                        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
                        cur.execute(sql, values)
                        
                    elif action == 'UPDATE':
                        set_clause = ', '.join([f"{k}=%s" for k in columns.keys()])
                        values = list(columns.values())
                        pk_col = list(columns.keys())[0]
                        pk_val = values[0]
                        sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_col}=%s"
                        cur.execute(sql, values + [pk_val])
                        
                    elif action == 'DELETE':
                        pk_col = list(columns.keys())[0]
                        pk_val = list(columns.values())[0]
                        sql = f"DELETE FROM {table_name} WHERE {pk_col}=%s"
                        cur.execute(sql, (pk_val,))
                        
                self.conn.commit()
                
        except Exception as e:
            logger.error(f"Error applying changes: {e}")
            if self.conn:
                self.conn.rollback()
            raise
