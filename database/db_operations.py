import logging
from dotenv import load_dotenv
from database.db_start import get_db_pool


load_dotenv()  # Загружаем переменные из .env
logger = logging.getLogger(__name__)



async def add_user(username, chat_id, horoscope_time):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        result = await conn.execute(
            "INSERT INTO users (username, chat_id, horoscope_time) VALUES ($1, $2, $3)" \
            "ON CONFLICT (username) DO NOTHING",
            username,
            chat_id,
            horoscope_time
        )
        if result == "INSERT 0 1":
            logger.info(f"[CORRECT] User [{username}] added successfully!")
        else:
            logger.warning(f"User [{username}] already exist!")