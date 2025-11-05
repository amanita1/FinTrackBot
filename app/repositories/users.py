from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_tg_id(self, tg_user_id: int) -> User | None:
        stmt = select(User).where(User.tg_user_id == tg_user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user


__all__ = ["UserRepository"]
