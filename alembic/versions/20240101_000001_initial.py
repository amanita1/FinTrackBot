from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20240101_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tg_user_id", sa.BigInteger(), nullable=False, unique=True),
        sa.Column("currency", sa.String(length=8), nullable=False, server_default="KZT"),
        sa.Column("payday", sa.Integer(), nullable=True),
        sa.Column("period_mode", sa.Enum("calendar", "salary", name="periodmode"), nullable=False, server_default="calendar"),
        sa.Column("tz", sa.String(length=64), nullable=False, server_default="Asia/Almaty"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "budgets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("planned_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "period_start"),
    )

    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("type", sa.Enum("expense", "income", name="transactiontype"), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("meta", sa.JSON(), nullable=True),
    )
    op.create_index("ix_transactions_user_ts", "transactions", ["user_id", "ts"])

    op.create_table(
        "recurrings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("cron", sa.String(length=64), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("type", sa.Enum("expense", "income", name="recurringtype"), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "goal_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True),
        sa.Column("target_amount", sa.Numeric(14, 2), nullable=False, server_default="0"),
        sa.Column("reserve_mode", sa.Enum("none", "percent", "fixed", name="goalreservemode"), nullable=False, server_default="none"),
        sa.Column("reserve_value", sa.Numeric(14, 2), nullable=False, server_default="0"),
        sa.Column("rollover_rule", sa.Enum("none", "all", "percent", "fixed", name="goalrolloverrule"), nullable=False, server_default="none"),
        sa.Column("rollover_value", sa.Numeric(14, 2), nullable=False, server_default="0"),
    )

    op.create_table(
        "goal_ledger",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("ts", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("direction", sa.Enum("in", "out", name="goalledgerdirection"), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
    )

    op.create_table(
        "bot_dedup",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tg_chat_id", sa.BigInteger(), nullable=False),
        sa.Column("tg_message_id", sa.BigInteger(), nullable=False),
        sa.Column("handled_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("tg_chat_id", "tg_message_id"),
    )


def downgrade() -> None:
    op.drop_table("bot_dedup")
    op.drop_table("goal_ledger")
    op.drop_table("goal_settings")
    op.drop_table("recurrings")
    op.drop_index("ix_transactions_user_ts", table_name="transactions")
    op.drop_table("transactions")
    op.drop_table("budgets")
    op.drop_table("users")
    sa.Enum(name="periodmode").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="transactiontype").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="recurringtype").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="goalreservemode").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="goalrolloverrule").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="goalledgerdirection").drop(op.get_bind(), checkfirst=False)
