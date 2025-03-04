from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins

def firststart_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Начать работу")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Жми:"
    )
    return keyboard
