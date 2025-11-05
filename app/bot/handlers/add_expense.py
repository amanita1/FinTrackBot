from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandObject, Command
from aiogram.types import Message

from ...services.parsing import parse_add_command

router = Router(name="add_expense")


@router.message(Command(commands=["add"]))
async def cmd_add(message: Message, command: CommandObject) -> None:
    if not command.args:
        await message.answer("Используйте: /add <сумма> <описание>")
        return
    try:
        parsed = parse_add_command(command.args)
    except ValueError as exc:
        await message.answer(str(exc))
        return
    category = parsed.category or "другое"
    await message.answer(
        f"Записал расход {parsed.amount:.2f} ({category}). Заметка: {parsed.note or '—'}"
    )
