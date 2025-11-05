from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from ..models import GoalReserveMode, GoalRolloverRule


@dataclass(slots=True)
class GoalIncomeSplit:
    stash_amount: Decimal
    wallet_amount: Decimal


def calculate_income_split(amount: Decimal, mode: GoalReserveMode, value: Decimal) -> GoalIncomeSplit:
    if amount <= 0:
        return GoalIncomeSplit(stash_amount=Decimal("0"), wallet_amount=amount)

    if mode == GoalReserveMode.PERCENT:
        percent = max(Decimal("0"), value)
        stash = (amount * percent / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return GoalIncomeSplit(stash_amount=stash, wallet_amount=amount - stash)
    if mode == GoalReserveMode.FIXED:
        stash = min(amount, max(Decimal("0"), value))
        return GoalIncomeSplit(stash_amount=stash, wallet_amount=amount - stash)

    return GoalIncomeSplit(stash_amount=Decimal("0"), wallet_amount=amount)


def calculate_rollover(leftover: Decimal, rule: GoalRolloverRule, value: Decimal) -> Decimal:
    if leftover <= 0:
        return Decimal("0")

    if rule == GoalRolloverRule.ALL:
        return leftover
    if rule == GoalRolloverRule.PERCENT:
        percent = max(Decimal("0"), value)
        return (leftover * percent / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if rule == GoalRolloverRule.FIXED:
        return min(leftover, max(Decimal("0"), value))

    return Decimal("0")


__all__ = ["GoalIncomeSplit", "calculate_income_split", "calculate_rollover"]
