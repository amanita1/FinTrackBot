# app/bot/instance.py
from aiogram import Bot, Dispatcher
from ..config import settings  # или откуда ты берёшь токен

bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
