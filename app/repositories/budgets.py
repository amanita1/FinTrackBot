from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Budget


class BudgetRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_for_period(self, user_id: int, period_start: date) -> Budget | None:
        stmt = select(Budget).where(
            Budget.user_id == user_id, Budget.period_start == period_start
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, budget: Budget) -> Budget:
        self.session.add(budget)
        await self.session.flush()
        return budget


__all__ = ["BudgetRepository"]
