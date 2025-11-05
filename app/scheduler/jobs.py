from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..config import get_settings

logger = logging.getLogger(__name__)


async def morning_digest() -> None:
    logger.info("Running morning digest at %s", datetime.utcnow())


async def evening_reminder() -> None:
    logger.info("Running evening reminder at %s", datetime.utcnow())


async def period_rollover() -> None:
    logger.info("Running period rollover at %s", datetime.utcnow())


def setup_scheduler(scheduler: AsyncIOScheduler) -> None:
    settings = get_settings()
    scheduler.add_job(morning_digest, "cron", hour=settings.digest_hour)
    scheduler.add_job(evening_reminder, "cron", hour=settings.reminder_hour)
    scheduler.add_job(period_rollover, "cron", hour=0)


async def _startup() -> None:
    scheduler = AsyncIOScheduler(timezone=get_settings().timezone)
    setup_scheduler(scheduler)
    scheduler.start()
    logger.info("Scheduler started")

    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        scheduler.shutdown()
        raise


def main() -> None:
    asyncio.run(_startup())


if __name__ == "__main__":
    main()


__all__ = [
    "setup_scheduler",
    "morning_digest",
    "evening_reminder",
    "period_rollover",
    "main",
]
