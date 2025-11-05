from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal

from fastapi import APIRouter, Depends

from ..config import get_settings
from ..schemas import CSVResponse, GoalStatusSchema, PeriodSchema, ReportSchema, SummarySchema

router = APIRouter()


@router.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/me/summary", response_model=SummarySchema)
async def me_summary(settings=Depends(get_settings)):
    now = datetime.now(tz=ZoneInfo(settings.timezone))
    return SummarySchema(
        period=PeriodSchema(start=now.date(), end=now.date()),
        planned=Decimal("0"),
        spent=Decimal("0"),
        rest=Decimal("0"),
        days_left=1,
        daily_limit=Decimal("0"),
    )


@router.get("/me/report", response_model=ReportSchema)
async def me_report(range_name: str = "month"):
    range_value = range_name if range_name in {"week", "month"} else "month"
    return ReportSchema(
        range=range_value,
        categories=[],
        total_expenses=Decimal("0"),
        total_income=Decimal("0"),
    )


@router.post("/export/csv", response_model=CSVResponse)
async def export_csv(range_name: str = "month"):
    content = "date,type,amount,category,note\n"
    safe_name = range_name if range_name in {"week", "month"} else "month"
    return CSVResponse(filename=f"fintrack-{safe_name}.csv", content=content)


@router.get("/goal/status", response_model=GoalStatusSchema)
async def goal_status():
    return GoalStatusSchema(
        target=Decimal("0"),
        total=Decimal("0"),
        progress_percent=Decimal("0"),
        eta_days=None,
        recent=[],
    )
