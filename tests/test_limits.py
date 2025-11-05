from __future__ import annotations

from datetime import date
from decimal import Decimal

from app.services.limits import calculate_daily_limit
from app.services.periods import Period


def test_classic_limit():
    period = Period(start=date(2024, 3, 1), end=date(2024, 3, 31))
    result = calculate_daily_limit(
        planned_amount=Decimal("310000"),
        expenses_total=Decimal("100000"),
        extra_income_total=Decimal("20000"),
        mandatory_future=Decimal("5000"),
        today=date(2024, 3, 10),
        period=period,
    )
    assert result.rest == Decimal("225000.00")
    assert result.days_left == 22
    assert result.daily_limit == Decimal("10227")


def test_overspend_adjustment():
    period = Period(start=date(2024, 3, 1), end=date(2024, 3, 31))
    result = calculate_daily_limit(
        planned_amount=Decimal("100000"),
        expenses_total=Decimal("50000"),
        extra_income_total=Decimal("0"),
        mandatory_future=Decimal("0"),
        today=date(2024, 3, 15),
        period=period,
        yesterday_delta=Decimal("-5000"),
    )
    assert result.daily_limit < Decimal("5000")
    assert result.adjustment_percent < 0


def test_underspend_adjustment():
    period = Period(start=date(2024, 3, 1), end=date(2024, 3, 31))
    result = calculate_daily_limit(
        planned_amount=Decimal("100000"),
        expenses_total=Decimal("30000"),
        extra_income_total=Decimal("0"),
        mandatory_future=Decimal("0"),
        today=date(2024, 3, 10),
        period=period,
        yesterday_delta=Decimal("2000"),
    )
    assert result.daily_limit > Decimal("3180")
    assert result.adjustment_percent > 0
