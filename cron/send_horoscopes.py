import random
from bot_instance import bot
from cron.daily_messages import DAILY_MESSAGES
from database.db_operations import get_all_chat_ids, get_zodiac_signs_for_user
from album_creator import create_album


async def send_all_horoscopes_to_all_users():
    chat_ids = await get_all_chat_ids()
    for chat_id in chat_ids:
        zodiacs = await get_zodiac_signs_for_user(chat_id)
        albums = create_album(zodiacs)

        daily_message = random.choice(DAILY_MESSAGES)
        await bot.send_message(chat_id=chat_id, text=daily_message)
        
        if len(albums) == 2:
            for album in albums:
                await bot.send_media_group(chat_id=chat_id, media=album)
        else:
            await bot.send_media_group(chat_id=chat_id, media=albums)