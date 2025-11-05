from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Iterable

from ..models import Transaction, TransactionType


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


__all__ = ["ReportBuilder", "range_to_dates"]
