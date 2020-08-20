import random
from PIL import Image, ImageDraw, ImageFont
#
#
# def random_char():
#     return chr(random.randint(65, 90))
#
#
# def random_bac_color():
#     return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
#
#
# def random_bac_font_color():
#     return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
#
#
# def art_board():
#     width = 60 * 4
#     height = 60
#     im = Image.new('RGB', (width, height), (255, 255, 255))
#
#     # create drawObject
#     draw = ImageDraw.Draw(im)
#
#     # create background color
#     for x in range(0, width):
#         for y in range(0, height):
#             draw.point([x, y], fill=random_bac_color())
#
#     # create fontObject
#     font = ImageFont.truetype('/home/wong/PycharmProjects/xfz/utils/captcha/ARIALN.TTF', 36)
#
#     # create board filled of font and background
#     for i in range(4):
#         draw.text([50*i+10, 10], text=random_char(), font=font, fill=random_bac_font_color())
#
#     # save board
#     im.save('./captcha.jpg', 'jpeg')


class ImgCaptcha:
    width = 140
    height = 40

    @classmethod
    def __random_char(cls):
        # random.seed(int(time.time()))
        return chr(random.randint(65, 90))

    @classmethod
    def _random_char(cls):
        text = list()
        for k in range(5):
            char = cls.__random_char()
            text.append(char)
        return text

    @classmethod
    def __random_bac_color(cls):
        return (random.randint(64, 200), random.randint(64, 100), random.randint(64, 100))

    @classmethod
    def __random_bac_font_color(cls):
        return (random.randint(0, 100), random.randint(100, 255), random.randint(100, 255))

    @classmethod
    def __draw_line(cls):
        start = (random.randint(0, cls.width), random.randint(0, cls.height))
        end = (random.randint(0, cls.width), random.randint(0, cls.height))
        return [start, end]

    @classmethod
    def art_board(cls):
        im = Image.new('RGB', (cls.width, cls.height), (255, 255, 255))
        # create drawObject
        draw_img = ImageDraw.Draw(im)

        # create background color
        for x in range(cls.width):
            for y in range(cls.height):
                draw_img.point([x, y], fill=cls.__random_bac_color())

        # create fontObject
        font = ImageFont.truetype('/home/wong/PycharmProjects/xfz/utils/captcha/ARIALN.TTF', 30)

        # get random char text
        text = cls._random_char()

        # create board filled for font and background
        for i in range(len(text)):
            draw_img.text([25*i+4, 0], text=text[i], font=font, fill=cls.__random_bac_font_color())
            draw_img.line(cls.__draw_line(), fill=cls.__random_bac_font_color())
        return (im, text)
