from __future__ import annotations

import enum
from datetime import datetime, date

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    JSON,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class PeriodMode(str, enum.Enum):
    CALENDAR = "calendar"
    SALARY = "salary"


class TransactionType(str, enum.Enum):
    EXPENSE = "expense"
    INCOME = "income"


class GoalReserveMode(str, enum.Enum):
    NONE = "none"
    PERCENT = "percent"
    FIXED = "fixed"


class GoalRolloverRule(str, enum.Enum):
    NONE = "none"
    ALL = "all"
    PERCENT = "percent"
    FIXED = "fixed"


class GoalLedgerDirection(str, enum.Enum):
    IN = "in"
    OUT = "out"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    currency: Mapped[str] = mapped_column(String(8), default="KZT")
    payday: Mapped[int | None]
    period_mode: Mapped[PeriodMode] = mapped_column(Enum(PeriodMode), default=PeriodMode.CALENDAR)
    tz: Mapped[str] = mapped_column(String(64), default="Asia/Almaty")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    budgets: Mapped[list["Budget"]] = relationship(back_populates="user")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")
    goal_settings: Mapped["GoalSettings | None"] = relationship(back_populates="user", uselist=False)


class Budget(Base):
    __tablename__ = "budgets"
    __table_args__ = (
        UniqueConstraint("user_id", "period_start"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    planned_amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="budgets")


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("ix_transactions_user_ts", "user_id", "ts"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    category: Mapped[str | None] = mapped_column(String(64))
    note: Mapped[str | None] = mapped_column(Text)
    meta: Mapped[dict | None] = mapped_column(JSON)

    user: Mapped[User] = relationship(back_populates="transactions")


class Recurring(Base):
    __tablename__ = "recurrings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    cron: Mapped[str] = mapped_column(String(64), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    category: Mapped[str | None] = mapped_column(String(64))
    note: Mapped[str | None] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class GoalSettings(Base):
    __tablename__ = "goal_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    target_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    reserve_mode: Mapped[GoalReserveMode] = mapped_column(Enum(GoalReserveMode), default=GoalReserveMode.NONE)
    reserve_value: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    rollover_rule: Mapped[GoalRolloverRule] = mapped_column(Enum(GoalRolloverRule), default=GoalRolloverRule.NONE)
    rollover_value: Mapped[float] = mapped_column(Numeric(14, 2), default=0)

    user: Mapped[User] = relationship(back_populates="goal_settings")


class GoalLedger(Base):
    __tablename__ = "goal_ledger"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    direction: Mapped[GoalLedgerDirection] = mapped_column(Enum(GoalLedgerDirection), nullable=False)
    note: Mapped[str | None] = mapped_column(Text)


class BotDedup(Base):
    __tablename__ = "bot_dedup"
    __table_args__ = (
        UniqueConstraint("tg_chat_id", "tg_message_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tg_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    handled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


__all__ = [
    "Base",
    "User",
    "Budget",
    "Transaction",
    "Recurring",
    "GoalSettings",
    "GoalLedger",
    "BotDedup",
    "PeriodMode",
    "TransactionType",
    "GoalReserveMode",
    "GoalRolloverRule",
    "GoalLedgerDirection",
]
