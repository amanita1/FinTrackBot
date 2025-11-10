from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Iterable
from zoneinfo import ZoneInfo

from aiogram.exceptions import TelegramAPIError
from sqlalchemy import select

from ..bot.loader import bot
from ..config import get_settings
from ..db import session_scope
from ..models import Transaction, TransactionType, User
from ..repositories.transactions import TransactionRepository


class ReportBuilder:
    def __init__(self, transactions: Iterable[Transaction]) -> None:
        self.transactions = list(transactions)

    def totals_by_category(self, tx_type: TransactionType) -> dict[str, Decimal]:
        totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
        for tx in self.transactions:
            if tx.type != tx_type:
                continue
            category = tx.category or "other"
            totals[category] += Decimal(tx.amount)
        return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))

    def period_totals(self) -> dict[TransactionType, Decimal]:
        totals: dict[TransactionType, Decimal] = {
            TransactionType.EXPENSE: Decimal("0"),
            TransactionType.INCOME: Decimal("0"),
        }
        for tx in self.transactions:
            totals[tx.type] += Decimal(tx.amount)
        return totals


def range_to_dates(now: datetime, range_name: str) -> tuple[datetime, datetime]:
    if range_name == "week":
        start_date = (now - timedelta(days=now.weekday())).date()
        end_date = start_date + timedelta(days=6)
    else:
        start_date = now.replace(day=1).date()
        next_month = (now.replace(day=28) + timedelta(days=4)).replace(day=1).date()
        end_date = next_month - timedelta(days=1)
    start_dt = datetime.combine(start_date, datetime.min.time(), tzinfo=now.tzinfo)
    end_dt = datetime.combine(end_date, datetime.max.time(), tzinfo=now.tzinfo)
    return start_dt, end_dt


logger = logging.getLogger(__name__)
settings = get_settings()


def _user_timezone(user: User) -> ZoneInfo:
    try:
        return ZoneInfo(user.tz or settings.timezone)
    except Exception:  # pragma: no cover - fallback on invalid tz names
        logger.warning("Unknown timezone %s for user %s", user.tz, user.id)
        return ZoneInfo(settings.timezone)


async def _send_message(chat_id: int, text: str) -> None:
    try:
        await bot.send_message(chat_id, text)
    except TelegramAPIError as exc:  # pragma: no cover - depends on Telegram API
        logger.error("Failed to send message to %s: %s", chat_id, exc)


def _format_amount(amount: float, currency: str) -> str:
    value = Decimal(str(amount)).quantize(Decimal("0.01"))
    return f"{value} {currency}"


async def run_morning_digest() -> None:
    async with session_scope() as session:
        users = (await session.execute(select(User))).scalars().all()
        tx_repo = TransactionRepository(session)

        for user in users:
            tz = _user_timezone(user)
            now = datetime.now(tz=tz)
            start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1, microseconds=-1)

            expenses = await tx_repo.totals_by_type(user.id, start, end, TransactionType.EXPENSE)
            income = await tx_repo.totals_by_type(user.id, start, end, TransactionType.INCOME)

            text = (
                "Доброе утро!\n"
                f"Расходы за вчера: {_format_amount(expenses, user.currency)}.\n"
                f"Доходы за вчера: {_format_amount(income, user.currency)}.\n"
                "Желаем продуктивного дня!"
            )
            await _send_message(user.tg_user_id, text)


async def run_evening_reminder() -> None:
    async with session_scope() as session:
        users = (await session.execute(select(User))).scalars().all()
        tx_repo = TransactionRepository(session)

        for user in users:
            tz = _user_timezone(user)
            now = datetime.now(tz=tz)
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1, microseconds=-1)

            expenses = await tx_repo.totals_by_type(user.id, start, end, TransactionType.EXPENSE)

            text = (
                "Добрый вечер!\n"
                "Не забудьте записать расходы за сегодня.\n"
                f"Текущие расходы: {_format_amount(expenses, user.currency)}."
            )
            await _send_message(user.tg_user_id, text)


async def run_period_rollover() -> None:
    async with session_scope() as session:
        users = (await session.execute(select(User))).scalars().all()

        for user in users:
            tz = _user_timezone(user)
            now = datetime.now(tz=tz)
            if now.day != 1:
                continue

            text = (
                "Новый месяц — самое время пересмотреть бюджет.\n"
                "Обновите категории и цели, чтобы оставаться на курсе!"
            )
            await _send_message(user.tg_user_id, text)


__all__ = [
    "ReportBuilder",
    "range_to_dates",
    "run_evening_reminder",
    "run_morning_digest",
    "run_period_rollover",
]
