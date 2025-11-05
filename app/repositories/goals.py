from __future__ import annotations

from datetime import datetime

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import GoalLedger, GoalLedgerDirection, GoalSettings


class GoalRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_settings(self, user_id: int) -> GoalSettings | None:
        stmt = select(GoalSettings).where(GoalSettings.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_settings(self, settings: GoalSettings) -> GoalSettings:
        self.session.add(settings)
        await self.session.flush()
        return settings

    async def add_ledger_entry(self, entry: GoalLedger) -> GoalLedger:
        self.session.add(entry)
        await self.session.flush()
        return entry

    async def balance(self, user_id: int) -> float:
        stmt = select(
            func.coalesce(
                func.sum(
                    case(
                        (GoalLedger.direction == GoalLedgerDirection.IN, GoalLedger.amount),
                        else_=-GoalLedger.amount,
                    )
                ),
                0,
            )
        ).where(GoalLedger.user_id == user_id)
        result = await self.session.execute(stmt)
        return float(result.scalar_one())

    async def recent_entries(self, user_id: int, limit: int = 5) -> list[GoalLedger]:
        stmt = select(GoalLedger).where(GoalLedger.user_id == user_id).order_by(GoalLedger.ts.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars())


__all__ = ["GoalRepository"]
