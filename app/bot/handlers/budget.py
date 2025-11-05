from __future__ import annotations

from decimal import Decimal, InvalidOperation

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="budget")


@router.message(Command(commands=["budget"]))
async def cmd_budget(message: Message) -> None:
    parts = message.text.split()
    if len(parts) < 3 or parts[1] != "set":
        await message.answer("Используйте: /budget set <сумма>")
        return
    amount_raw = parts[2].replace(",", ".")
    try:
        amount = Decimal(amount_raw)
    except InvalidOperation:
        await message.answer("Некорректная сумма")
        return
    await message.answer(f"План на период обновлён: {amount:.2f}")
