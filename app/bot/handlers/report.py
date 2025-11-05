from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

router = Router(name="report")


@router.message(Command(commands=["report"]))
async def cmd_report(message: Message, command: CommandObject) -> None:
    period = command.args or "month"
    await message.answer(
        f"Отчёт за {period}: пока что данных нет. Используйте /export csv для выгрузки."
    )
