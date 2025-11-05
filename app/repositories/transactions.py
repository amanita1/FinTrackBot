from __future__ import annotations

from datetime import datetime

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Transaction, TransactionType


class TransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, tx: Transaction) -> Transaction:
        self.session.add(tx)
        await self.session.flush()
        return tx

    async def totals_by_type(
        self,
        user_id: int,
        start: datetime,
        end: datetime,
        tx_type: TransactionType,
    ) -> float:
        stmt: Select = (
            select(func.coalesce(func.sum(Transaction.amount), 0))
            .where(
                Transaction.user_id == user_id,
                Transaction.type == tx_type,
                Transaction.ts >= start,
                Transaction.ts <= end,
            )
        )
        result = await self.session.execute(stmt)
        return float(result.scalar_one())


__all__ = ["TransactionRepository"]
