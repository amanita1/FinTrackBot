from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from ..bot.loader import feed_webhook_update
from ..config import get_settings

router = APIRouter()


@router.post("/telegram")
async def telegram_webhook(request: Request, settings=Depends(get_settings)) -> dict[str, str]:
    data = await request.json()
    await feed_webhook_update(data)
    return {"status": "accepted"}
