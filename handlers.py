from aiogram import Bot, Router, types, F
from aiogram.filters import Command
from keyboard import *
from album_creator import create_album


router = Router()

#start-хендлер
@router.message(Command('start'))
async def cmd_start(message: types.Message):

    keyboard = daily_keyboard()
    await message.answer(f'Добро пожаловать в <b>HOROSCOPE BOT</b>, {message.from_user.first_name}!\nМы предоставляем возможность получать ежедневный гороскоп!\nНажми на кнопку и получи его уже сейчас!',
                         parse_mode='HTML',
                         reply_markup=keyboard
    )


@router.message(F.text == 'Получить сегодняшний гороскоп!')
async def daily_horoscope(message: types.Message):
    album1, album2 = create_album()
    await message.answer_media_group(album1)
    await message.answer_media_group(album2)
    await message.answer('Вот ваш гороскоп!', reply_markup=menu_keyboard())

@router.message(F.text == 'Установить время')
async def change_time(message: types.Message):
    await message.answer('Просим прощения, данная функция находится в разработке.', reply_markup=menu_keyboard())

@router.message(F.text == 'Выбрать знаки')
async def change_time(message: types.Message):
    await message.answer('Просим прощения, данная функция находится в разработке.', reply_markup=menu_keyboard())





