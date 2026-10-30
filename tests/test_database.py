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


"""Tests for the SQL<->URO connector."""
import pytest

from uro import DatabaseURO, ColumnURO, URO
from uro.exceptions import ConnectorError


def test_create_table():
    db = DatabaseURO("app")
    t = db.create_table("users")
    assert db.table("users") is t


def test_duplicate_table_raises():
    db = DatabaseURO("app")
    db.create_table("users")
    with pytest.raises(ConnectorError):
        db.create_table("users")


def test_insert_select_delete():
    db = DatabaseURO("app")
    t = db.create_table("users").add_column(ColumnURO("name", "str"))
    row = URO.new(payload={"name": "alice"})
    t.insert(row)
    assert t.select() == [row]
    assert t.select(where=lambda p: p["name"] == "alice") == [row]
    t.delete(row)
    assert t.select() == []


def test_missing_table_raises():
    db = DatabaseURO("app")
    with pytest.raises(ConnectorError):
        db.table("nope")
