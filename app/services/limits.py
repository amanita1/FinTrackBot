from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP

from .periods import Period, days_left


@dataclass(slots=True)
class DailyLimitResult:
    rest: Decimal
    days_left: int
    daily_limit: Decimal
    adjustment_percent: Decimal


def calculate_daily_limit(
    *,
    planned_amount: Decimal,
    expenses_total: Decimal,
    extra_income_total: Decimal,
    mandatory_future: Decimal,
    today: date,
    period: Period,
    yesterday_delta: Decimal = Decimal("0"),
) -> DailyLimitResult:
    if planned_amount <= 0:
        return DailyLimitResult(
            rest=Decimal("0"),
            days_left=days_left(today, period),
            daily_limit=Decimal("0"),
            adjustment_percent=Decimal("0"),
        )

    rest = planned_amount - (expenses_total - extra_income_total) - mandatory_future
    remaining_days = days_left(today, period)
    per_day = (rest / remaining_days) if remaining_days else Decimal("0")
    base_limit = per_day.to_integral_value(rounding=ROUND_FLOOR)

    adjustment = Decimal("0")
    if yesterday_delta < 0:
        overspend = abs(yesterday_delta)
        ratio = min(Decimal("0.10"), (overspend / planned_amount).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
        adjusted_limit = (base_limit * (Decimal("1") - ratio)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        adjustment = -ratio
    elif yesterday_delta > 0:
        underspend = yesterday_delta
        ratio = min(Decimal("0.05"), (underspend / planned_amount).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
        adjusted_limit = (base_limit * (Decimal("1") + ratio)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        adjustment = ratio
    else:
        adjusted_limit = base_limit

    return DailyLimitResult(
        rest=rest.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        days_left=remaining_days,
        daily_limit=adjusted_limit,
        adjustment_percent=(adjustment * Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
    )


__all__ = ["DailyLimitResult", "calculate_daily_limit"]
