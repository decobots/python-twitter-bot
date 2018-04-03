import io
import os
import random
from typing import List

from PIL import ImageDraw, Image, ImageFont

from src.color_table import Color, ColorTable
from src.photo import Photo

DATA_DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
W = 200
H = 200


def create_svg(color: Color) -> Photo:
    canvas = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, W, H), fill=color.rgb_values)
    f_color = (30, 30, 30) if color.lab_values[0] > 50 else (230, 230, 230)
    font = ImageFont.truetype(os.path.join(DATA_DEFAULT_PATH, 'Monotony.ttf'))
    draw.text((10, 50), color.name, fill=f_color, font=font, layout_engine=ImageFont.LAYOUT_BASIC)
    buffer = io.BytesIO()
    canvas.save(buffer, format='JPEG')
    p = Photo("", '', '', '', '')
    p.data = buffer.getvalue()
    return p


def __generate_colors(number_of_colors: int = 10, number_of_additional_colors: int = 1) -> List[Color]:
    tab = ColorTable()
    lst = []
    for n in range(number_of_colors):
        random_color = Color(r=random.randint(0, 255), g=random.randint(0, 255), b=random.randint(0, 255))
        near = tab.nearest_color(random_color.lab).color
        delta = tab.calculate_deltas(random_color.lab)

        res = [random_color, near]
        for item in delta[1:number_of_additional_colors]:
            res.append(item.color)
        lst.append(res)
    return lst
