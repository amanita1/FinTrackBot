from __future__ import annotations

from datetime import date
from decimal import Decimal

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ...services.limits import DailyLimitResult

router = Router(name="today")


@router.message(Command(commands=["today"]))
async def cmd_today(message: Message) -> None:
    result = DailyLimitResult(
        rest=Decimal("0"),
        days_left=1,
        daily_limit=Decimal("0"),
        adjustment_percent=Decimal("0"),
    )
    await message.answer(
        f"На сегодня лимит {result.daily_limit:.0f}, остаток {result.rest:.2f}. "
        "Продолжайте вести расходы!"
    )
