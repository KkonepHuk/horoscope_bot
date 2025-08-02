import asyncpg
import os
import logging
from dotenv import load_dotenv


load_dotenv()  # Загружаем переменные из .env
logger = logging.getLogger(__name__)

db_pool = None
async def init_db_pool():
    global db_pool
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT") or '5432'
    dbname = os.getenv("DB_NAME")

    dsn = f"postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode=disable"

    db_pool = await asyncpg.create_pool(dsn)
    logger.info("Connection to the DB via the pool has been established")

def get_db_pool():
    if db_pool is None:
        raise RuntimeError("DB pool is not initialized yet")
    return db_pool

async def create_tables():
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                first_name TEXT NOT NULL,
                username TEXT,
                user_id BIGINT UNIQUE NOT NULL,
                chat_id BIGINT NOT NULL,
                horoscope_time TIME NOT NULL
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users_info (
                id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                first_name TEXT UNIQUE NOT NULL,
                username TEXT,
                user_id BIGINT UNIQUE NOT NULL,
                chat_id BIGINT NOT NULL,
                horoscope_time TIME NOT NULL
            )
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS zodiac_signs (
                id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(255) UNIQUE NOT NULL
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_zodiac_signs (
                user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
                zodiac_sign_id INT REFERENCES zodiac_signs(id) ON DELETE SET NULL,
                PRIMARY KEY (user_id, zodiac_sign_id)
            )
        """)
        await conn.execute("""
            INSERT INTO zodiac_signs (name) VALUES
            ('Овен'), ('Телец'), ('Близнецы'), ('Рак'), ('Лев'), ('Дева'),
            ('Весы'), ('Скорпион'), ('Стрелец'), ('Козерог'), ('Водолей'), ('Рыбы')
            ON CONFLICT (name) DO NOTHING
        """)
        logger.info("DB schema and zodiac signs ready.")
        

