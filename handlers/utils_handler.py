#TODO: Доделать операции, сделать перезапись общего баланса при операциях, добавить высчитывание лимита на день и обработку минусовых значений лимита.

import aiogram.types
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import db_handler
from keyboards.operations_kb import *
from keyboards.user_kb import *
from utils import my_utils
from db_handler import db_func
import asyncio
from create_bot import bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db_handler import db_func
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
import re


class Form(StatesGroup):
    waitingForPlus = State()
    waitingForMinus = State()

utils_router = Router()
@utils_router.message(F.text == '⚙️ Действия')
async def cmd_operation(message: Message, state: FSMContext):
    await message.answer(f'Выбери операцию',
                         reply_markup=operations_kb(message.from_user.id))

@utils_router.message(F.text == '📝 Лимит')
async def cmd_limit(message: Message, state: FSMContext):
    balance = (await db_func.get_user_data(message.from_user.id)).get("balance")
    limit = await my_utils.calculateLimitTillNextMonth(balance)
    await message.answer(f'У тебя: {balance}'
                         f'Твой ежедневный лимит: {limit}')

@utils_router.message(F.text == '➖ Трата')
async def cmd_minus(message: Message, state: FSMContext):
    await message.answer(f'Выбери операцию',
                         reply_markup=operations_equals_kb(message.from_user.id))
    await state.set_state(Form.waitingForMinus)

@utils_router.message(F.text == '➕ Пополнение')
async def cmd_plus(message: Message, state: FSMContext):
    await message.answer(f'Выбери операцию',
                         reply_markup=operations_equals_kb(message.from_user.id))
    await state.set_state(Form.waitingForPlus)



@utils_router.message(F.text, Form.waitingForPlus)
async def cmd_equals(message: Message, state: FSMContext):
    balance = (await db_func.get_user_data(message.from_user.id)).get("balance")
    limit = await my_utils.calculateLimitTillNextMonth(balance)
    value = int(message.text)
    newbalance = await my_utils.plus(balance, value)
    db_handler.db_func.db.collection.update_one({"_id": message.from_user.id}, {"$set": {"balance": newbalance}})
    await message.answer(f'Готово. Твой баланс: {newbalance}.',
                         reply_markup=start_kb(message.from_user.id))
    await state.clear()



@utils_router.message(F.text, Form.waitingForMinus)
async def cmd_equals(message: Message, state: FSMContext):
    balance = (await db_func.get_user_data(message.from_user.id)).get("balance")
    limit = await my_utils.calculateLimitTillNextMonth(balance)
    value = int(message.text)
    newbalance = await my_utils.minus(balance, value)
    db_handler.db_func.db.collection.update_one({"_id": message.from_user.id}, {"$set": {"balance": newbalance}})
    await message.answer(f'Готово. Твой баланс: {newbalance}.',
                         reply_markup=start_kb(message.from_user.id))
    await state.clear()