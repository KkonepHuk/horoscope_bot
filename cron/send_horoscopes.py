import logging
import random
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from bot_instance import bot
from cron.daily_messages import DAILY_MESSAGES
from database.db_operations import get_all_chat_ids, get_zodiac_signs_for_user
from album_creator import create_album


async def send_all_horoscopes_to_all_users():
    chat_ids = await get_all_chat_ids()
    

    for chat_id in chat_ids:
        try:
            zodiacs = await get_zodiac_signs_for_user(chat_id)
            albums = create_album(zodiacs)

            daily_message = random.choice(DAILY_MESSAGES)
            await bot.send_message(chat_id=chat_id, text=daily_message)

            if isinstance(albums, tuple):  # Если 2 альбома
                for album in albums:
                    await bot.send_media_group(chat_id=chat_id, media=album)
            else:
                await bot.send_media_group(chat_id=chat_id, media=albums)

            logging.info(f"Daily horoscopes sent successfully to [{chat_id}]")
        except TelegramForbiddenError:
            logging.warning(f"User [{chat_id}] blocked bot.")
            #await remove_user_from_db(chat_id)

        except Exception as e:
            logging.error(f"Error sending to user {chat_id}: {e}")
