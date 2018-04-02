import logging
import os
from collections import namedtuple
from typing import List, Tuple

import colormath.color_conversions
import colormath.color_diff
import colormath.color_objects

log = logging.getLogger()

DATA_DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
colors_delta = namedtuple('colors_delta', ('color', 'delta'))


class Color:
    def __init__(self, r: int, g: int, b: int, name: str = None):
        self.__rgb_check(r, g, b)
        self.name = name
        self.rgb = colormath.color_objects.AdobeRGBColor(rgb_r=r, rgb_g=g, rgb_b=b, is_upscaled=True)
        self.lab = colormath.color_conversions.convert_color(
            color=self.rgb,
            target_cs=colormath.color_objects.LabColor)

    @staticmethod
    def __rgb_check(r, g, b):
        if not (0 <= r <= 256 and 0 <= g <= 256 and 0 <= b <= 256):
            message = f"each of r, g, and, b values should be between 0 and 256. \nYour values r={r} g={g} b={b}"
            log.error(message)
            raise ValueError(message)

    @property
    def rgb_values(self) -> Tuple[int, int, int]:
        return self.rgb.get_upscaled_value_tuple()

    @property
    def lab_values(self) -> Tuple[int, int, int]:
        return self.lab.get_value_tuple()

    @property
    def hex(self) -> str:
        return self.rgb.get_rgb_hex()

    def __eq__(self, other):
        # name not considered
        return self.rgb_values == other.rgb_values

    def __repr__(self):
        return ','.join([str(v) for v in self.rgb_values])


class ColorTable:
    def __init__(self, path_to_raw_data: os.path = os.path.join(DATA_DEFAULT_PATH, 'colors.txt')):
        self.path_to_raw = path_to_raw_data
        self.color_table = self._create_colors_table()

    def _create_colors_table(self) -> List["Color"]:
        colors = []
        with open(file=self.path_to_raw, mode='r') as inp:
            for line in inp.read().splitlines():
                name, r, g, b = line.split('	')
                colors.append(Color(int(r), int(g), int(b), name))
            log.info(f"Created color table for {len(colors)} colors")
            return colors

    def calculate_deltas(self, clr_lab: colormath.color_objects.LabColor) -> List['colors_delta']:
        calculated_deltas = [colors_delta(color, colormath.color_diff.delta_e_cie1976(clr_lab, color.lab))
                             for color in self.color_table
                             ]
        return sorted(calculated_deltas, key=lambda x: x.delta)

    def nearest_color(self, clr: colormath.color_objects.LabColor) -> 'colors_delta':
        return self.calculate_deltas(clr_lab=clr)[0]
