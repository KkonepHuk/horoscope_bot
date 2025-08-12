import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboard import *
from datetime import time
from dotenv import load_dotenv
from album_creator import create_album
from database.db_operations import add_user, get_zodiac_signs_for_user, save_selected_signs
from horoscope_maker.core.consts import SIGNS



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
    if len(albums) == 2:
        for album in albums:
            await message.answer_media_group(album)
    else:
        await message.answer_media_group(albums)
    await message.answer('Вот ваш гороскоп!', reply_markup=menu_keyboard())

@router.message(F.text == 'Установить время')
async def change_time(message: types.Message):
    await message.answer('Просим прощения, данная функция находится в разработке.', reply_markup=menu_keyboard())

@router.message(F.text == 'Выбрать знаки')
async def change_zodiac_signs(message: types.Message):
    user_id = message.from_user.id
    keyboard = await zodiac_keyboard(user_id)
    
    await message.answer("Выберите ваши предпочтительные знаки зодиака:", reply_markup=keyboard)
    

@router.callback_query(F.data.startswith("toggle_"))
async def toggle_sign(callback: types.CallbackQuery):
    sign = callback.data.replace("toggle_", "")
    user_id = callback.from_user.id
    
    #Читаем из БД
    selected = await get_zodiac_signs_for_user(user_id)
    
    #Добавляем или убираем
    if sign in selected:
        selected.remove(sign)
    else:
        selected.append(sign)

    #Обновляем данные БД
    await save_selected_signs(user_id, selected)

    #Перерисовываем клавиатуру
    keyboard = await zodiac_keyboard(user_id)


    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "select_all")
async def select_all_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    selected = SIGNS
    await save_selected_signs(user_id, selected)
    keyboard = await zodiac_keyboard(user_id)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "deselect_all")
async def deselect_all_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    selected = []
    await save_selected_signs(user_id, selected)
    keyboard = await zodiac_keyboard(user_id)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()