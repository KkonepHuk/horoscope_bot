import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboard import *
from datetime import time
from dotenv import load_dotenv
from album_creator import create_album
from database.db_operations import add_user, get_zodiac_signs_for_user



load_dotenv()  # Загружаем переменные из .env
logger = logging.getLogger(__name__)


router = Router()

#start-хендлер
@router.message(Command('start'))
async def cmd_start(message: types.Message):

    keyboard = daily_keyboard()
    await message.answer(f'Добро пожаловать в <b>HOROSCOPE BOT</b>, {message.from_user.first_name}!\nМы предоставляем возможность получать ежедневный гороскоп!\nНажми на кнопку и получи его уже сейчас!',
                         parse_mode='HTML',
                         reply_markup=keyboard
    )

    deafoult_time_obj = time.fromisoformat('09:00:00')
    await add_user(message.from_user.first_name, message.from_user.username, message.from_user.id, message.chat.id, deafoult_time_obj)


@router.message(F.text == 'Получить сегодняшний гороскоп!')
async def daily_horoscope(message: types.Message):
    zodiacs = await get_zodiac_signs_for_user(message.from_user.id)
    logger.info(f'Zodiacs of user {message.from_user.id}: {zodiacs}')
    albums = create_album(zodiacs)
    for album in albums:
        await message.answer_media_group(album)
    await message.answer('Вот ваш гороскоп!', reply_markup=menu_keyboard())

@router.message(F.text == 'Установить время')
async def change_time(message: types.Message):
    await message.answer('Просим прощения, данная функция находится в разработке.', reply_markup=menu_keyboard())

@router.message(F.text == 'Выбрать знаки')
async def change_time(message: types.Message):
    await message.answer('Просим прощения, данная функция находится в разработке.', reply_markup=menu_keyboard())





