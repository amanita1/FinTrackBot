from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins


def start_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="📝 Лимит"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="⚙️ Действия"), KeyboardButton(text="О создателе")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def req_admin_kb(user_telegram_id: int):
    if user_telegram_id in admins:
        kb_list = [
                [KeyboardButton(text="⚙️ Админ панель")]
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb_list,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Ку, Сашка"
        )
        return keyboard
    else:
        return