import asyncio
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from db_handler import db_creation as db

async def get_user_data(user_id: int):      #example: asyncio.run(get_user_data(123))
        user_info = db.collection.find_one({"_id": user_id})
        if user_info:
            return user_info
        else:
            return "None"

async def save_user_data(user_id: int, name: str, username: str, created_at: int):
    user_data = {
        "_id": user_id,  # Используем user_id как уникальный идентификатор
        "name": name,
        "username": username,
        "created_at": created_at
    }
    await asyncio.to_thread(db.collection.update_one, {"_id": user_id}, {"$set": user_data}, upsert=True)

async def is_user_in_db(user_id: int) -> bool:
    user = await asyncio.to_thread(db.collection.find_one, {"_id": user_id})
    return user is not None

async def add_balance_in_db(user_id:int, balance):
    # user = await asyncio.to_thread(db.collection.find_one, {"_id": user_id})
    await asyncio.to_thread(
        db.collection.update_one,
        {"_id": user_id},
        {"$set": {"balance": balance}},
        upsert=True
    )


async def add_goal_in_db(user_id:int, goal):
    # user = await asyncio.to_thread(db.collection.find_one, {"_id": user_id})
    await asyncio.to_thread(
        db.collection.update_one,
        {"_id": user_id},
        {"$set": {"goal": goal}},
        upsert=True
    )

def get_all_users():
    #Получает всех пользователей из MongoDB.
    return db.collection.find({})

def update_user_limits(user_id, new_limit):
    #Обновляет лимит пользователя в базе.
    db.collection.update_one({"_id": user_id}, {"$set": {"today_limit": new_limit}})

def calculate_new_limit(user_id):
    # Логика расчета нового лимита
    balance = db.collection.find_one({"_id": user_id})
    return   # Например, оставляем лимит прежним или устанавливаем 100
