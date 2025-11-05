from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Update

from ..config import get_settings
from .handlers import add_expense, budget, goal, income, report, settings as settings_handler, start, today
from .middlewares.dedup import DedupMiddleware

settings = get_settings()

bot = Bot(token=settings.bot_token, parse_mode="HTML")
dispatcher = Dispatcher()

dispatcher.include_router(start.router)
dispatcher.include_router(budget.router)
dispatcher.include_router(add_expense.router)
dispatcher.include_router(income.router)
dispatcher.include_router(today.router)
dispatcher.include_router(report.router)
dispatcher.include_router(goal.router)
dispatcher.include_router(settings_handler.router)

dispatcher.message.middleware.register(DedupMiddleware())


async def feed_webhook_update(data: dict) -> None:
    update = Update.model_validate(data)
    await dispatcher.feed_update(bot, update)


async def set_webhook(url: str) -> None:
    if not url:
        raise RuntimeError("WEBHOOK_BASE is not configured")
    webhook_url = f"{url.rstrip('/')}/webhook/telegram"
    await bot.set_webhook(webhook_url)
    logging.info("Webhook set to %s", webhook_url)


async def delete_webhook() -> None:
    await bot.delete_webhook()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="FinTrack bot utility")
    parser.add_argument("command", choices=["set-webhook", "delete-webhook"])
    parser.add_argument("url", nargs="?", default=settings.webhook_base)
    args = parser.parse_args()

    async def runner() -> None:
        if args.command == "set-webhook":
            await set_webhook(args.url)
        else:
            await delete_webhook()

    asyncio.run(runner())


if __name__ == "__main__":
    main()


__all__ = ["bot", "dispatcher", "feed_webhook_update", "set_webhook", "delete_webhook"]
