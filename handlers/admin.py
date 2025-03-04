import aiogram.types
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.admin_kb import *

admin_router = Router()

@admin_router.message(F.text == '⚙️ Админ панель')
async def cmd_admin(message: Message):
    await message.answer(f'Админ панель',
                         reply_markup=admin_kb(message.from_user.id))
