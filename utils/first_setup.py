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
    CurrentBallance = State()
    goal = State()


questionnaire_router = Router()


@questionnaire_router.message(F.text == f'Начать работу')
async def start_questionnaire_process(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer(f'Для начала укажи свой текущий баланс (просто отправь число. Пример: 350000)')
    await state.set_state(Form.CurrentBallance)


@questionnaire_router.message(F.text, Form.CurrentBallance)
async def capture_balance(message: Message, state: FSMContext):
    await state.update_data(CurrentBalance=message.text)
    balance = int(message.text)
    await db_func.add_balance_in_db(user_id=message.from_user.id, balance = balance)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Ого, да ты богат! Напиши, сколько ты хочешь сохранить к концу месяца (оставь 0, если не хочешь сохранять что-либо): ')
    await state.set_state(Form.goal)


@questionnaire_router.message(F.text, Form.goal)
async def capture_goal(message: Message, state: FSMContext):
    goal = int(message.text)
    await db_func.add_goal_in_db(user_id=message.from_user.id, goal = goal)
    data = await db_func.get_user_data(message.from_user.id)
    if goal == 0:
        msg_text = f'И так, сейчас у тебя <b>{data.get("balance")}</b> денег и ты не хочешь откладывать. Отлично. Теперь пропиши /start для вывода основной клавиатуры или нажми на кнопку ниже, чтобы начать сначала.'
        await message.answer(msg_text)
        await state.clear()
    else:
        msg_text = f'И так, сейчас у тебя <b>{data.get("balance")}</b> денег и ты хочешь отложить <b>{data.get("goal")}</b>. Отлично. Теперь пропиши /start для вывода основной клавиатуры или нажми на кнопку ниже, чтобы начать сначала..'
        await message.answer(msg_text)
        await state.clear()
