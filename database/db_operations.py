import logging
from dotenv import load_dotenv
from database.db_start import get_db_pool
from horoscope_maker.core.consts import SIGNS


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
            logger.info(f"User [{username}] added into TABLE [users] successfully!")
        else:
            logger.warning(f"User [{username}] already exist in TABLE [users]!")
        
        records = await conn.fetch(
            'SELECT id FROM zodiac_signs WHERE name = ANY($1)', SIGNS
        )
        zodiac_ids = [record['id'] for record in records]

        for zodiac_id in zodiac_ids:
            await conn.execute('''
                INSERT INTO user_zodiac_signs (user_id, zodiac_sign_id) VALUES ($1, $2)
                ON CONFLICT DO NOTHING
            ''', user_id, zodiac_id)

async def get_all_chat_ids():
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        records = await conn.fetch("SELECT chat_id FROM users")
        return [record['chat_id'] for record in records]

async def get_zodiac_signs_for_user(user_id):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        records = await conn.fetch(f'''
                                    SELECT zodiac_signs.name AS zodiac_sign
                                    FROM user_zodiac_signs
                                    INNER JOIN zodiac_signs 
                                    ON user_zodiac_signs.zodiac_sign_id = zodiac_signs.id
                                    WHERE user_id = $1
                                    ''', user_id)
        return [record['zodiac_sign'] for record in records]

async def save_selected_signs(user_id, selected_signs):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        #Сначала удаляем все записи для пользователя
        await conn.execute('DELETE FROM user_zodiac_signs WHERE user_id = $1', user_id)
        
        #Получаем id знаков по их именам
        records = await conn.fetch('SELECT id FROM zodiac_signs WHERE name = ANY($1)', selected_signs)
        zodiac_ids = [record['id'] for record in records]

        # Вставляем новые записи
        for zodiac_id in zodiac_ids:
            await conn.execute('''
                               INSERT INTO user_zodiac_signs (user_id, zodiac_sign_id)
                               VALUES ($1, $2)
                               ON CONFLICT DO NOTHING
                               ''', user_id, zodiac_id)

