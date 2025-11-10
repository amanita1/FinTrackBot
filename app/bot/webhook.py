from __future__ import annotations

from fastapi import APIRouter, Request

from .loader import feed_webhook_update

router = APIRouter()


@router.post("/webhook/telegram")
async def telegram_webhook(request: Request) -> dict[str, bool]:
    data = await request.json()
    await feed_webhook_update(data)
    return {"ok": True}


__all__ = ["router", "telegram_webhook"]
