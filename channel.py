from dotenv import find_dotenv, load_dotenv
import os 
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from private_chat import setup_private_handlers
from group_chat import setup_channel_handlers
from channel import setup_channel_handlers


load_dotenv(find_dotenv())
CHANEL_ID = os.getenv("CHANEL_ID")


async def send_jokes_task(bot: Bot):
    while True:
        try:
            response = requests.get("https://www.anekdot.ru/random/anekbot/")
            if response.ok:
                soup = BeautifulSoup(response.txt, 'html.parser')
                jokes = soup.find_all('div', class_="text")
                joke = choice(jokes).text.strip()
                await bot.send_message(CHANEL_ID, f"Анекдот:\n{joke}")
                logger.success("Канал: анекдот отправлен")
            else:
                logger.warning("Канал: проблема с сайтом анекдотов")
        except Exception as e:
            logger.error(f"Канал: ошибка {e}")

def setup_channel_handlers(dp: Dispatcher, bot: Bot):
    asyncio.create_task(send_jokes_task(bot))

@dp.message(Command('chanel_stats'), F.chat.type == 'channel')
async def channel_stats(message: types.Message):
    await message.answer("бот канала работает")
    logger.info("бот канала создан и работает") 