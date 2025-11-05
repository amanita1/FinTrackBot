from __future__ import annotations

from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from sqlalchemy import select

from ...db import session_scope
from ...models import BotDedup


class DedupMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data):  # type: ignore[override]
        if isinstance(event, Message):
            chat_id = event.chat.id
            message_id = event.message_id
            async with session_scope() as session:
                existing = await session.scalar(
                    select(BotDedup).where(
                        BotDedup.tg_chat_id == chat_id,
                        BotDedup.tg_message_id == message_id,
                    )
                )
                if existing:
                    return None
                session.add(BotDedup(tg_chat_id=chat_id, tg_message_id=message_id, handled_at=datetime.utcnow()))
        return await handler(event, data)


__all__ = ["DedupMiddleware"]
