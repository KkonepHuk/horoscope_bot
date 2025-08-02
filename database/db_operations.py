import logging
from dotenv import load_dotenv
from database.db_start import get_db_pool


load_dotenv()  # Загружаем переменные из .env
logger = logging.getLogger(__name__)



async def add_user(first_name, username, user_id, chat_id, horoscope_time):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        result = await conn.execute(
            "INSERT INTO users (first_name, username, user_id, chat_id, horoscope_time) VALUES ($1, $2, $3, $4, $5)" \
            "ON CONFLICT (user_id) DO NOTHING",
            first_name,
            username,
            user_id,
            chat_id,
            horoscope_time
        )
        if result == "INSERT 0 1":
            logger.info(f"User [{username}] added successfully!")
        else:
            logger.warning(f"User [{username}] already exist!")

async def get_all_chat_ids():
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        records = await conn.fetch("SELECT chat_id FROM users")
        return [record['chat_id'] for record in records]
            

