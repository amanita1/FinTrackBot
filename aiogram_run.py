import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from handlers.admin import admin_router
from utils.first_setup import questionnaire_router
from handlers.utils_handler import utils_router
# from work_time.time_func import send_time_msg

async def main():
    print("Bot is running...")
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(questionnaire_router)
    dp.include_router(utils_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())