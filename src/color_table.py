import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Tuple

import colormath.color_conversions
import colormath.color_diff
import colormath.color_objects

log = logging.getLogger()


class Color:
    def __init__(self, r: int, g: int, b: int):
        self.__rgb_checker(r, g, b)

        self.rgb = colormath.color_objects.AdobeRGBColor(rgb_r=r, rgb_g=g, rgb_b=b, is_upscaled=True)
        self.lab = colormath.color_conversions.convert_color(
            color=self.rgb,
            target_cs=colormath.color_objects.LabColor)

    @staticmethod
    def __rgb_checker(r, g, b):
        if not (0 <= r <= 256 and 0 <= g <= 256 and 0 <= b <= 256):
            message = f"each of r, g, and, b values should be between 0 and 256. \nYour values r={r} g={g} b={b}"
            log.error(message)
            raise ValueError(message)

    @property
    def rgb_values(self) -> Tuple[int]:
        return self.rgb.get_upscaled_value_tuple()

    @property
    def lab_values(self) -> Tuple[int]:
        return self.lab.get_value_tuple()


class ColorTable:
    def __init__(self,
                 path_to_raw_data: os.path = os.path.join(
                     os.path.dirname(os.path.dirname(__file__)), 'src', 'colors.txt'),
                 path_to_lab_out: os.path = os.path.join(
                     os.path.dirname(os.path.dirname(__file__)), 'src', 'out_lab.txt'),
                 path_to_rgb_out: os.path = os.path.join(
                     os.path.dirname(os.path.dirname(__file__)), 'src', 'out_rgb.txt')):
        self.path_to_raw = path_to_raw_data
        self.path_to_lab = path_to_lab_out
        self.path_to_rgb = path_to_rgb_out
        self.color_table_lab = self._load_colors_table_lab()
        # self.color_table_rgb = None TODO implement if needed

    def _load_colors_table_lab(self) -> Dict[str, colormath.color_objects.LabColor]:
        if not Path(self.path_to_lab).exists():  # generate files
            self.__generate_files_with_color_tables()
        with open(file=self.path_to_lab, mode="r") as file:
            lab_colors = json.load(fp=file)
            return {name: colormath.color_objects.LabColor(*values) for name, values in lab_colors.items()}

    def calculate_deltas(self, clr_lab: colormath.color_objects.LabColor) -> List[
        Dict[str, colormath.color_objects.LabColor]]:
        calculated_deltas = [{name: colormath.color_diff.delta_e_cie1976(clr_lab, value)}
                             for name, value in self.color_table_lab.items()
                             ]
        return sorted(calculated_deltas, key=lambda x: list(x.values())[0])

    def __generate_files_with_color_tables(self):
        rgb_colors = {}
        lab_colors = {}
        with open(file=self.path_to_raw, mode='r') as inp, \
                open(file=self.path_to_lab, mode="w") as out_lab, \
                open(file=self.path_to_rgb, mode="w") as out_rgb:
            for line in inp.read().splitlines():
                name, r, g, b = line.split('	')
                color = Color(int(r), int(g), int(b))
                rgb_colors[name] = color.rgb_values
                lab_colors[name] = color.lab_values
            json.dump(lab_colors, fp=out_lab)
            json.dump(rgb_colors, fp=out_rgb)
        log.info(f"generated files for color tables {self.path_to_lab} and {self.path_to_rgb}")


if __name__ == '__main__':
    my_color = Color(150, 1, 1)
    tab = ColorTable()
