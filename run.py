import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import router
from database.db_start import init_db_pool, create_tables


load_dotenv()  # Загрузит переменные из .env


TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


logging.basicConfig(
    level=logging.INFO,  # минимальный уровень сообщений (INFO и выше)
    format='%(asctime)s %(levelname)s %(message)s',  # формат вывода: время, уровень, сообщение
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

async def main():
    await init_db_pool()
    await create_tables()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logger.info('Succesfully started!')
    asyncio.run(main())
    

    