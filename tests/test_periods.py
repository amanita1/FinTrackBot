from __future__ import annotations

from datetime import date

import pytest

from app.models import PeriodMode
from app.services.periods import Period, calculate_period


@pytest.mark.parametrize(
    "today,mode,payday,expected",
    [
        (date(2024, 1, 15), PeriodMode.CALENDAR, None, Period(date(2024, 1, 1), date(2024, 1, 31))),
        (date(2024, 2, 10), PeriodMode.CALENDAR, None, Period(date(2024, 2, 1), date(2024, 2, 29))),
        (date(2024, 3, 2), PeriodMode.SALARY, 1, Period(date(2024, 3, 1), date(2024, 3, 31))),
        (date(2024, 3, 30), PeriodMode.SALARY, 5, Period(date(2024, 3, 5), date(2024, 4, 4))),
        (date(2024, 2, 29), PeriodMode.SALARY, 31, Period(date(2024, 1, 31), date(2024, 2, 28))),
    ],
)
def test_calculate_period(today, mode, payday, expected):
    period = calculate_period(today, mode, payday)
    assert period.start == expected.start
    assert period.end == expected.end


def test_salary_requires_payday():
    with pytest.raises(ValueError):
        calculate_period(date(2024, 1, 1), PeriodMode.SALARY, None)


def test_payday_bounds():
    with pytest.raises(ValueError):
        calculate_period(date(2024, 1, 1), PeriodMode.SALARY, 0)
    with pytest.raises(ValueError):
        calculate_period(date(2024, 1, 1), PeriodMode.SALARY, 32)
