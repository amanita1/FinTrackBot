from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes_public import router as public_router
from .config import get_settings
from .bot.webhook import router as telegram_router
from .services.reports import (
    run_evening_reminder,
    run_morning_digest,
    run_period_rollover,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    scheduler = AsyncIOScheduler(timezone=settings.timezone)
    scheduler.add_job(run_morning_digest, "cron", hour=settings.digest_hour)
    scheduler.add_job(run_evening_reminder, "cron", hour=settings.reminder_hour)
    scheduler.add_job(run_period_rollover, "cron", hour=0, minute=5)

    scheduler.start()
    logger.info(
        "APScheduler started (timezone=%s, digest=%s, reminder=%s)",
        settings.timezone,
        settings.digest_hour,
        settings.reminder_hour,
    )

    app.state.scheduler = scheduler
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler stopped")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="FinTrack Bot", lifespan=lifespan)

    if settings.allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(public_router)
    app.include_router(telegram_router)
    return app


app = create_app()


__all__ = ["create_app", "app"]
