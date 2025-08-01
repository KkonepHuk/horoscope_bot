import requests
from bs4 import BeautifulSoup
from core.text_formatting import format
#from core.consts import RUS_TO_ENG, ENG_TO_RUS

'''
#перевод с одного языка на другой
def translate(sign):
    sign = sign.lower() #приводим знак к нижнему регистру
    if sign in RUS_TO_ENG:
        return RUS_TO_ENG[sign]
    elif sign in ENG_TO_RUS:
        return ENG_TO_RUS[sign]
    else:
        raise ValueError('Unknown zodiac sign')'''


#получение гороскопа по знаку зодиака
def get_horoscope_text(sign):
    sign = sign.lower() #приводим знак к нижнему регистру
    #sign = translate(sign)
    URL = f"https://horoscopes.rambler.ru/{sign}/" #вставляем в ссылку нужный знак зодиака
    response = requests.get(URL) #отправляем запрос на страничку сайта
    soup = BeautifulSoup(response.text, "html.parser") #получаем html страничку
    article = soup.find('p', class_="UqoHt aTWfO") #ищем гороскоп на этой страничке
    text = article.get_text() #забираем текст гороскопа(избавляемся от html разметки)
    text = format(text)
    return text #возвращаем чистый текст гороскопа

if __name__ == '__main__':
    sign = input('Введите ваш знак зодиака: ')
    horoscope = get_horoscope_text(sign)
    print(f'Вот ваш гороскоп на сегодняшний день:\n{horoscope}')




    