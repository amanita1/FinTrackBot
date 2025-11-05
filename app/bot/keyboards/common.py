from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def export_csv_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Экспорт CSV", callback_data="export_csv")]]
    )


__all__ = ["export_csv_keyboard"]
