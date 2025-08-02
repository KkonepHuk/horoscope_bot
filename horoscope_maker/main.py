from horoscope_maker.core.horoscope_text import get_horoscope_text
from horoscope_maker.core.horoscope_img import get_horoscope_img
from horoscope_maker.core.consts import SIGNS


def get_all_horoscopes():
    for sign in SIGNS:
        text = get_horoscope_text(sign)
        get_horoscope_img(sign, text)


if __name__ == '__main__':
    print("Succesfully started!")
    get_all_horoscopes()
    print("Done!")