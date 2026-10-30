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


"""Tests for the AUPI translation layer."""
import pytest

from uro import AUPI, typed_uro
from uro.exceptions import TranslationError


def make_aupi():
    a = AUPI()
    a.register("number", "phone_number",
               lambda n: f"+1-555-{int(n):04d}")
    a.register("phone_number", "sms_uri",
               lambda p: f"sms:{p}")
    return a


def test_direct_translation():
    a = make_aupi()
    assert a.translate_value(42, "number", "phone_number") == "+1-555-0042"


def test_chained_translation():
    a = make_aupi()
    assert a.translate_value(7, "number", "sms_uri") == "sms:+1-555-0007"


def test_identity_translation():
    a = make_aupi()
    assert a.find_path("number", "number") == []


def test_no_path_raises():
    a = make_aupi()
    with pytest.raises(TranslationError):
        a.find_path("number", "email")


def test_translate_uro():
    a = make_aupi()
    src = typed_uro("number", 99)
    out = a.translate(src, "phone_number")
    assert out.payload == {"type": "phone_number", "value": "+1-555-0099"}


def test_translate_untyped_raises():
    from uro import URO
    a = make_aupi()
    with pytest.raises(TranslationError):
        a.translate(URO.new(payload="not typed"), "phone_number")


def test_translation_creates_relationship():
    a = make_aupi()
    src = typed_uro("number", 1)
    out = a.translate(src, "phone_number")
    assert len(src.associations) == 1
    assert out in [getattr(x, 'b', None) for x in src.associations]
