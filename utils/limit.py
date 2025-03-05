import asyncio
import datetime
from aiogram import Bot
from sqlalchemy.util import await_only

import db_handler.db_func
import utils.my_utils
from db_handler import db_func


async def update_limits():
    while True:
        now = datetime.datetime.now()
        next_update = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time.min)
        sleep_time = (next_update - now).total_seconds()

        await asyncio.sleep(sleep_time)  # Ждём до полуночи

        users = db_func.get_all_users()  # Получаем всех пользователей
        for user in users:
            new_limit = db_func.calculate_new_limit(user)  # Рассчитываем новый лимит
            db_func.update_user_limits(user["_id"], new_limit)  # Обновляем в MongoDB

#    asyncio.create_task(update_limits())


async def limitisnone():
    users = await db_func.get_all_users()
    for user in users:
        todayLimit = await db_func.get_user_data(user).get("today_limit")
        if todayLimit in [None, "None"]:
            balance = await db_func.calculate_new_limit()
            limit = await utils.my_utils.calculateLimitTillNextMonth()
