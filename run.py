import asyncio
import logging
from dotenv import load_dotenv
from bot_instance import bot
from aiogram import Dispatcher
from handlers import router
from database.db_start import init_db_pool, create_tables
from cron.cron_jobs import setup_cron_jobs


load_dotenv()  # Загрузит переменные из .env

dp = Dispatcher()


logging.basicConfig(
    filename='horoscope_bot.log',
    level=logging.INFO,  # минимальный уровень сообщений (INFO и выше)
    format='%(asctime)s %(levelname)s %(message)s',  # формат вывода: время, уровень, сообщение
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

async def main():
    await init_db_pool()
    await create_tables()
    setup_cron_jobs()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logger.info('Succesfully started!')
    asyncio.run(main())
    

    