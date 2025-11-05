from __future__ import annotations

from decimal import Decimal

import pytest

from app.services.parsing import parse_add_command


def test_parse_simple():
    parsed = parse_add_command("1900 кофе")
    assert parsed.amount == Decimal("1900.00")
    assert parsed.category == "coffee"
    assert parsed.note == "кофе"


def test_parse_with_decimal():
    parsed = parse_add_command("1200,50 такси")
    assert parsed.amount == Decimal("1200.50")
    assert parsed.category == "taxi"


def test_parse_requires_amount():
    with pytest.raises(ValueError):
        parse_add_command("кофе 1900")
