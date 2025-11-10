from __future__ import annotations
from fastapi import APIRouter, Request
from .loader import feed_webhook_update

router = APIRouter()

@router.post("/telegram")
async def telegram_webhook(request: Request):
    payload = await request.json()
    await feed_webhook_update(payload)
    return {"ok": True}



__all__ = ["router", "telegram_webhook"]
