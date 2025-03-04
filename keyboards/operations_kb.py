from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins

def operations_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="➕ Пополнение"), KeyboardButton(text="➖ Трата")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Какая была операция?"
    )
    return keyboard


def operations_equals_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="🟰 Готово")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Записал?"
    )
    return keyboard

