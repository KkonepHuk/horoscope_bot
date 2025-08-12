#from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
from horoscope_maker.core.consts import SIGNS, ENG_TO_RUS
from database.db_operations import get_zodiac_signs_for_user

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

async def zodiac_keyboard(user_id):
    #Создаёт клавиатуру с выделением выбранных знаков
    user_selected_signs = await get_zodiac_signs_for_user(user_id)
    buttons = []
    for sign in SIGNS:  # список всех знаков зодиака
        russion_sign = ENG_TO_RUS[sign].capitalize()
        if sign in user_selected_signs:
            button_text = f"✅ {russion_sign}"
        else:
            button_text = f"  {russion_sign}"
        buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=f"toggle_{sign}"))
    
    buttons.append(types.InlineKeyboardButton(text="Выбрать все", callback_data="select_all"))
    buttons.append(types.InlineKeyboardButton(text="Сбросить все", callback_data="deselect_all"))

    kb = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard