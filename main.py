from dotenv import find_dotenv, load_dotenv
import os 
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from private_chat import setup_private_handlers
from group_chat import setup_channel_handlers
from channel import setup_channel_handlers


load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
CHANEL_ID = os.getenv("CHANEL_ID")



async def main():
    logger.add("file.log",
               format="{time: YYYY-MM-DD at HH:mm:ss} | {levl} | {message}",
               rotation="3 days",
               backtrace=True,
               diagnose=True)
    
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    setup_private_handlers(dp)
    setup_group_handlers(dp)
    setup_channel_handlers(dp)

    logger.info("бот запущен")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("бот остановился")

if __name__ == "__main__":
    asyncio.run(main())