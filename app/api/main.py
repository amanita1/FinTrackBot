from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config import get_settings
from .routes_public import router as public_router
from .webhook import router as webhook_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="FinTrack Bot API")

    if settings.allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(public_router)
    app.include_router(webhook_router, prefix="/webhook")
    return app


app = create_app()


__all__ = ["create_app", "app"]
