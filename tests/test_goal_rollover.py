from __future__ import annotations

from decimal import Decimal

from app.models import GoalReserveMode, GoalRolloverRule
from app.services.goals import calculate_income_split, calculate_rollover


def test_income_percent_split():
    split = calculate_income_split(Decimal("100000"), GoalReserveMode.PERCENT, Decimal("10"))
    assert split.stash_amount == Decimal("10000.00")
    assert split.wallet_amount == Decimal("90000.00")


def test_income_fixed_split():
    split = calculate_income_split(Decimal("5000"), GoalReserveMode.FIXED, Decimal("2000"))
    assert split.stash_amount == Decimal("2000")
    assert split.wallet_amount == Decimal("3000")


def test_rollover_all():
    moved = calculate_rollover(Decimal("15000"), GoalRolloverRule.ALL, Decimal("0"))
    assert moved == Decimal("15000")


def test_rollover_percent():
    moved = calculate_rollover(Decimal("20000"), GoalRolloverRule.PERCENT, Decimal("25"))
    assert moved == Decimal("5000.00")


def test_rollover_fixed_cap():
    moved = calculate_rollover(Decimal("3000"), GoalRolloverRule.FIXED, Decimal("5000"))
    assert moved == Decimal("3000")


def test_negative_leftover():
    moved = calculate_rollover(Decimal("-1000"), GoalRolloverRule.ALL, Decimal("0"))
    assert moved == Decimal("0")
