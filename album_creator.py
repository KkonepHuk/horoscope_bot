from aiogram.types import FSInputFile, InputMediaPhoto
from horoscope_maker.core.consts import SIGNS
import os


def create_album():
    img_paths = []
    for sign in SIGNS:
        IMAGE_PATH = f'horoscope_maker/images/{sign}.jpg'
        if os.path.exists(IMAGE_PATH):
            img_paths.append(IMAGE_PATH)
        else:
            print(f"Файл не найден: {IMAGE_PATH}")

    album1 = []
    album2 = []
    for path in img_paths[:6]:
        try:
            input_file = FSInputFile(path)
            album1.append(InputMediaPhoto(media=input_file))
        except Exception as e:
            print(f"Ошибка при обработке файла {path}: {e}")

    for path in img_paths[6:]:
        try:
            input_file = FSInputFile(path)
            album2.append(InputMediaPhoto(media=input_file))
        except Exception as e:
            print(f"Ошибка при обработке файла {path}: {e}")

    return (album1, album2)