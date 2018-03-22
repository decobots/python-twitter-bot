import os
import random
from typing import List

import svgwrite

from src.color_table import Color, ColorTable

DATA_DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
W = 140
H = 40


def create_svg(color_groups: List[List['Color']]):
    with open(os.path.join(DATA_DEFAULT_PATH, "test.svg"), mode='w') as f:
        dwg = svgwrite.Drawing(size=(f'{W * len(color_groups[0])}px',
                                     f'{H * len(color_groups)}px'
                                     ))
        for group, y in zip(color_groups, range(0, len(color_groups) * H, H)):
            for x, color in enumerate(group):
                rect = dwg.rect(insert=(x * W, y), size=(W, H), fill=color.hex)
                dwg.add(rect)
                text = dwg.text([int(v) for v in color.lab_values],
                                insert=(x * W, y),
                                dy=[H / 2],
                                style=f'font-size:{H/2.2}px'
                                )
                dwg.add(text)
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


if __name__ == '__main__':
    create_svg(generate_colors(number_of_colors=19, number_of_additional_colors=10))
