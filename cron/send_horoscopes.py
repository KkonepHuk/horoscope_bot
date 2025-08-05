import random
from bot_instance import bot
from cron.daily_messages import DAILY_MESSAGES
from database.db_operations import get_all_chat_ids
from album_creator import create_album


async def send_all_horoscopes_to_all_users():
    chat_ids = await get_all_chat_ids()
    album1, album2 = create_album()
    for chat_id in chat_ids:
        daily_message = random.choice(DAILY_MESSAGES)
        await bot.send_message(chat_id=chat_id, text=daily_message)
        await bot.send_media_group(chat_id=chat_id, media=album1)
        await bot.send_media_group(chat_id=chat_id, media=album2)