import aiogram.types
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.user_kb import *
from keyboards.firststart_kb import *
from db_handler import db_func
from texts import text
start_router = Router()
from datetime import datetime

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    if  await db_func.is_user_in_db( message.from_user.id):
        await message.answer(f'И снова привет, {message.from_user.full_name}!',
                             reply_markup=start_kb(message.from_user.id))
    else:
        user_id = message.from_user.id
        name = message.from_user.full_name
        username = message.from_user.username or "Нет username"
        created_at = int(datetime.utcnow().timestamp())

        await db_func.save_user_data(user_id, name, username, created_at)  # Сохраняем данные
        await message.answer(f'Привет, {message.from_user.full_name}! {text.first_welcome}',
                             reply_markup=firststart_kb(message.from_user.id))

@start_router.message(F.text == '/admin')
async def cmd_admin(message: Message):
    await message.answer(f'Ура, админ',
                         reply_markup=req_admin_kb(message.from_user.id))

@start_router.message(F.text == '/help')
async def cmd_start_3(message: Message):
    await message.answer(f'{text.help_text}')



# @start_router.message(Command('start_2'))
# async def cmd_start_2(message: Message):
#     await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()')
#
# @start_router.message(F.text == '/start_3')
# async def cmd_start_3(message: Message):
#     await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!')