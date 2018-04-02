import os
import random
from typing import List

import svgwrite

from src.color_table import Color, ColorTable, colors_delta

DATA_DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
W = 200
H = 200


def create_svg(color: Color, filename: str):
    with open(os.path.join(DATA_DEFAULT_PATH, filename), mode='w') as f:
        dwg = svgwrite.Drawing(size=(f'{W}px', f'{H}px'))
        rect = dwg.rect(insert=(0, 0), size=(W, H), fill=color.hex)
        dwg.add(rect)
        dwg.write(f)


def generate_colors(number_of_colors: int = 10, number_of_additional_colors: int = 1):
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
