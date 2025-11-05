from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Dict

DEFAULT_CATEGORY_MAP: Dict[str, str] = {
    "кофе": "coffee",
    "coffee": "coffee",
    "еда": "food",
    "lunch": "food",
    "такси": "taxi",
    "taxi": "taxi",
    "uber": "taxi",
    "аптека": "health",
    "лекарства": "health",
    "cinema": "entertainment",
    "кино": "entertainment",
    "зарплата": "salary",
    "зп": "salary",
    "бензин": "fuel",
    "fuel": "fuel",
}

TOKEN_RE = re.compile(r"[\wа-яА-ЯёЁ]+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def guess_category(note: str, *, last_category: str | None = None, mapping: Mapping[str, str] | None = None) -> str | None:
    tokens = tokenize(note)
    vocab = mapping or DEFAULT_CATEGORY_MAP
    for token in tokens:
        if token in vocab:
            return vocab[token]
    return last_category


__all__ = ["guess_category", "tokenize", "DEFAULT_CATEGORY_MAP"]
