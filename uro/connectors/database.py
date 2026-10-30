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


# =====================================================================
# MODULE START : uro.connectors.database
# ---------------------------------------------------------------------
# FILE         : uro/connectors/database.py
# PURPOSE      : The SQL<->URO connector (CONN.DBSE). Models DB, tables,
#                columns, constraints, references as UROs.
# STANDARD     : URO-STD-0001 S13
# =====================================================================
"""Database URO connector (CONN.DBSE)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from uro.core.uro import URO
from uro.core.urid import URID
from uro.exceptions import ConnectorError
from uro.security.acl import ACL
from uro.relations.association import Association

__all__ = ["ColumnURO", "TableURO", "DatabaseURO"]


class ColumnURO(URO):
    """A URO representing a single column definition."""

    def __init__(self, name: str, column_type: str = "str") -> None:
        """Create a column URO."""
        _identity = URID.new()
        super().__init__(_identity, _identity, {"kind": "CONN.DBSE.COL"})
        self.name = name
        self.column_type = column_type


class TableURO(URO):
    """A URO representing a table (group) of row UROs."""

    def __init__(self, name: str) -> None:
        """Create a table URO."""
        _identity = URID.new()
        super().__init__(_identity, _identity, {"kind": "CONN.DBSE.TABL"})
        self.name = name
        self.columns: List[ColumnURO] = []
        self.constraints: List[ACL] = []
        self.references: List[Association] = []
        self.rows: List[URO] = []

    def add_column(self, column: ColumnURO) -> "TableURO":
        """Add a column URO."""
        self.columns.append(column)
        return self

    def insert(self, row_uro: URO) -> None:
        """INSERT - attach a row URO to the table."""
        self.rows.append(row_uro)
        self.add_child(row_uro)

    def delete(self, row_uro: URO) -> None:
        """DELETE - remove a row URO from the table."""
        if row_uro not in self.rows:
            raise ConnectorError("row not found")
        self.rows.remove(row_uro)
        self.children.pop(row_uro.urid2, None)

    def select(self, where: Optional[Any] = None) -> List[URO]:
        """SELECT - return row UROs, optionally filtered."""
        if where is None:
            return list(self.rows)
        return [r for r in self.rows if where(r.payload)]


class DatabaseURO(URO):
    """A URO representing a database (CONN.DBSE)."""

    def __init__(self, name: str) -> None:
        """Create a database URO."""
        _identity = URID.new()
        super().__init__(_identity, _identity, {"kind": "CONN.DBSE"})
        self.name = name
        self.tables: Dict[str, TableURO] = {}

    def create_table(self, name: str) -> TableURO:
        """Create and register a new table URO."""
        if name in self.tables:
            raise ConnectorError(f"table {name} already exists")
        table = TableURO(name)
        self.tables[name] = table
        self.add_child(table)
        return table

    def table(self, name: str) -> TableURO:
        """Return a table URO by name."""
        if name not in self.tables:
            raise ConnectorError(f"no such table {name}")
        return self.tables[name]
# =====================================================================
# MODULE END   : uro.connectors.database
# =====================================================================
