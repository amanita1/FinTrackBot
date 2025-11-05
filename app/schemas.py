from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

from .models import GoalLedgerDirection, GoalReserveMode, GoalRolloverRule, TransactionType


class PeriodSchema(BaseModel):
    start: date
    end: date


class SummarySchema(BaseModel):
    period: PeriodSchema
    planned: Decimal
    spent: Decimal
    rest: Decimal
    days_left: int
    daily_limit: Decimal


class CategoryReportItem(BaseModel):
    category: str
    total: Decimal


class ReportSchema(BaseModel):
    range: Literal["week", "month"]
    categories: list[CategoryReportItem]
    total_expenses: Decimal
    total_income: Decimal


class GoalStatusLedgerItem(BaseModel):
    ts: datetime
    amount: Decimal
    direction: GoalLedgerDirection
    note: str | None = None


class GoalStatusSchema(BaseModel):
    target: Decimal
    total: Decimal
    progress_percent: Decimal
    eta_days: int | None
    recent: list[GoalStatusLedgerItem] = Field(default_factory=list)


class GoalUpdateRequest(BaseModel):
    mode: GoalReserveMode
    value: Decimal
    rollover_rule: GoalRolloverRule | None = None
    rollover_value: Decimal | None = None


class GoalWithdrawRequest(BaseModel):
    amount: Decimal
    note: str | None = None


class TransactionCreateRequest(BaseModel):
    amount: Decimal
    note: str
    type: TransactionType
    category: str | None = None


class CSVResponse(BaseModel):
    filename: str
    content: str


__all__ = [
    "SummarySchema",
    "ReportSchema",
    "GoalStatusSchema",
    "GoalUpdateRequest",
    "GoalWithdrawRequest",
    "TransactionCreateRequest",
    "CSVResponse",
]
