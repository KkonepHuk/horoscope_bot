#from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types

def daily_keyboard():
    kb = [
        [types.KeyboardButton(text="Получить сегодняшний гороскоп!")]
    ]
    daily = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return daily

def menu_keyboard():
    kb = [
        [types.KeyboardButton(text="Получить сегодняшний гороскоп!")],
        [types.KeyboardButton(text="Установить время"), types.KeyboardButton(text="Выбрать знаки")]
    ]
    menu = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return menu

