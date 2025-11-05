from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from calendar import monthrange

from ..models import PeriodMode


@dataclass(slots=True)
class Period:
    start: date
    end: date

    @property
    def days(self) -> int:
        return (self.end - self.start).days + 1


def _clamp_day(year: int, month: int, desired_day: int) -> date:
    last_day = monthrange(year, month)[1]
    return date(year, month, min(desired_day, last_day))


def calculate_period(current_date: date, mode: PeriodMode, payday: int | None) -> Period:
    if mode == PeriodMode.CALENDAR:
        start = current_date.replace(day=1)
        last_day = monthrange(current_date.year, current_date.month)[1]
        end = current_date.replace(day=last_day)
        return Period(start=start, end=end)

    if payday is None:
        raise ValueError("payday must be provided for salary mode")

    if payday < 1 or payday > 31:
        raise ValueError("payday must be between 1 and 31")

    if current_date.day >= payday:
        start_month = current_date.month
        start_year = current_date.year
    else:
        if current_date.month == 1:
            start_month = 12
            start_year = current_date.year - 1
        else:
            start_month = current_date.month - 1
            start_year = current_date.year

    start = _clamp_day(start_year, start_month, payday)

    if start.month == 12:
        end_year = start.year + 1
        end_month = 1
    else:
        end_year = start.year
        end_month = start.month + 1

    end = _clamp_day(end_year, end_month, payday) - timedelta(days=1)
    return Period(start=start, end=end)


def days_left(current_date: date, period: Period) -> int:
    remaining = (period.end - current_date).days + 1
    return max(1, remaining)


__all__ = ["Period", "calculate_period", "days_left"]
