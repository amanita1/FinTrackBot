# app/bot/loader.py
from __future__ import annotations

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update

from ..config import get_settings
from .handlers import (
    add_expense,
    budget,
    goal,
    income,
    report,
    settings as settings_handler,
    start,
    today,
)
from .middlewares.dedup import DedupMiddleware

logger = logging.getLogger(__name__)

# === CONFIG ===
settings = get_settings()

# === BOT & DISPATCHER ===
bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(parse_mode="HTML"),
)
dispatcher = Dispatcher()

# === ROUTERS ===
dispatcher.include_router(start.router)
dispatcher.include_router(budget.router)
dispatcher.include_router(add_expense.router)
dispatcher.include_router(income.router)
dispatcher.include_router(today.router)
dispatcher.include_router(report.router)
dispatcher.include_router(goal.router)
dispatcher.include_router(settings_handler.router)

# === MIDDLEWARES ===
dispatcher.message.middleware.register(DedupMiddleware())


# === WEBHOOK HANDLERS ===
async def feed_webhook_update(data: dict) -> None:
    """Feeds a Telegram update (JSON) into the dispatcher."""
    update = Update.model_validate(data)
    await dispatcher.feed_update(bot, update)


async def set_webhook(url: str | None = None) -> str:
    """Sets webhook to provided URL or WEBHOOK_BASE from settings."""
    base_url = url or settings.webhook_base
    if not base_url:
        raise RuntimeError("WEBHOOK_BASE is not configured")

    webhook_url = f"{base_url.rstrip('/')}/webhook/telegram"
    await bot.set_webhook(webhook_url)
    logger.info("Webhook set to %s", webhook_url)
    return webhook_url


async def get_webhook() -> str | None:
    """Returns currently active webhook URL."""
    info = await bot.get_webhook_info()
    logger.info("Current webhook: %s", info.url or "<not set>")
    return info.url or None


# === CLI UTILITY ===
def main() -> None:
    """Utility entry point for manual webhook management."""
    import argparse

    parser = argparse.ArgumentParser(description="FinTrack Bot Webhook Utility")
    parser.add_argument("command", choices=["set-webhook", "get-webhook"])
    parser.add_argument("url", nargs="?", default=None)
    args = parser.parse_args()

    async def runner() -> None:
        if args.command == "set-webhook":
            webhook_url = await set_webhook(args.url)
            print(webhook_url)
        else:
            current = await get_webhook()
            print(current or "")

    asyncio.run(runner())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()


__all__ = [
    "bot",
    "dispatcher",
    "feed_webhook_update",
    "get_webhook",
    "set_webhook",
]
