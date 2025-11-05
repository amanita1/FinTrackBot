from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from ...services.parsing import parse_add_command

router = Router(name="income")


@router.message(Command(commands=["income"]))
async def cmd_income(message: Message, command: CommandObject) -> None:
    if not command.args:
        await message.answer("Используйте: /income <сумма> <описание>")
        return
    try:
        parsed = parse_add_command(command.args)
    except ValueError as exc:
        await message.answer(str(exc))
        return
    await message.answer(
        f"Записал доход {parsed.amount:.2f}. Заметка: {parsed.note or '—'}"
    )
