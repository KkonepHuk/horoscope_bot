from PIL import Image, ImageDraw, ImageFont


FONT_PATH = '/Users/nikitos/Desktop/code/telegram_bots/horoscope_bot/horoscope_maker/assets/fonts/ArchiveUkr.ttf'
IMG_WIDTH, IMG_HEIGHT = 1080, 1080
FONT_SIZE = 45

def get_horoscope_img(name, text):
    NEW_IMAGE_PATH = f'/Users/nikitos/Desktop/code/telegram_bots/horoscope_bot/horoscope_maker/images/{name}.jpg'
    SIGN_IMAGE_PATH = f'/Users/nikitos/Desktop/code/telegram_bots/horoscope_bot/horoscope_maker/assets/signs_imgs/{name}.png'
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), 'white')
    idraw = ImageDraw.Draw(img)
    overlay = Image.open(SIGN_IMAGE_PATH)
    overlay = overlay.resize((IMG_WIDTH, IMG_HEIGHT))
    img.paste(overlay, (0, 0), mask=overlay)
    fnt = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    x, y = IMG_WIDTH // 2, IMG_HEIGHT // 2 - 300
    for string in text:
        idraw.text((x, y), string, font=fnt, anchor='ms', fill=(0, 0, 0))
        y += 60
    img.save(NEW_IMAGE_PATH)

if __name__ == '__main__':
    a = get_horoscope_img('Привет')