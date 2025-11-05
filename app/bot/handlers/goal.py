from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

router = Router(name="goal")


def _help() -> str:
    return (
        "Команды цели:\n"
        "/goal set percent <p>\n"
        "/goal set fixed <amount>\n"
        "/goal set rollover all|percent:<p>|fixed:<amount>\n"
        "/goal target <amount>\n"
        "/goal status\n"
        "/goal withdraw <amount> [note]"
    )


@router.message(Command(commands=["goal"]))
async def cmd_goal(message: Message, command: CommandObject) -> None:
    if not command.args:
        await message.answer(_help())
        return
    await message.answer("Настройки цели обновлены (демо режим).")
