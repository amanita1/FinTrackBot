from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from .categorizer import guess_category


@dataclass(slots=True)
class ParsedCommand:
    amount: Decimal
    note: str
    category: str | None


_AMOUNT_RE = re.compile(r"^([0-9]+(?:[.,][0-9]+)?)\s*(.*)$", re.DOTALL)


def parse_amount_and_note(text: str) -> tuple[Decimal, str]:
    match = _AMOUNT_RE.match(text.strip())
    if not match:
        raise ValueError("Не удалось распознать сумму")
    amount_raw, note = match.groups()
    amount_raw = amount_raw.replace(",", ".")
    try:
        amount = Decimal(amount_raw)
    except InvalidOperation as exc:
        raise ValueError("Некорректная сумма") from exc
    return amount.quantize(Decimal("0.01")), note.strip()


def parse_add_command(text: str, *, last_category: str | None = None) -> ParsedCommand:
    amount, note = parse_amount_and_note(text)
    category = guess_category(note, last_category=last_category)
    return ParsedCommand(amount=amount, note=note, category=category)


__all__ = ["ParsedCommand", "parse_add_command", "parse_amount_and_note"]
