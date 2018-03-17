import json
import logging
from pathlib import Path
from typing import Dict, List

import colormath.color_conversions
import colormath.color_diff
import colormath.color_objects

from src.logger import init_logging

log = logging.getLogger()


class Color:
    def __init__(self, r: int, g: int, b: int):
        self.__rgb_checker(r, g, b)
        self.rgb = colormath.color_objects.AdobeRGBColor(rgb_r=r, rgb_g=g, rgb_b=b)
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
    def rgb_values(self):
        return self.rgb.get_value_tuple()

    @property
    def lab_values(self):
        return self.lab.get_value_tuple()


class ColorTable:
    def __init__(self,
                 filename_raw_data: str = 'colors.txt',
                 filename_lab_out: str = 'out_lab.txt',
                 filename_rgb_out: str = 'out_rgb.txt'):
        self.file_raw = filename_raw_data
        self.file_lab = filename_lab_out
        self.file_rgb = filename_rgb_out
        self.color_table_lab = self._load_colors_table_lab()
        # self.color_table_rgb = None TODO implement if needed

    def _load_colors_table_lab(self) -> Dict[str, colormath.color_objects.LabColor]:
        if not Path(self.file_lab).exists():  # generate files
            self.__generate_files_with_color_tables()
        with open(file=self.file_lab, mode="r") as file:
            lab_colors = json.load(fp=file)
            return {name: colormath.color_objects.LabColor(*values) for name, values in lab_colors.items()}

    def calculate_deltas(self, pic_clr: "Color") -> List[Dict[str, colormath.color_objects.LabColor]]:
        calculated_deltas = [{name: colormath.color_diff.delta_e_cie1976(pic_clr, value)}
                             for name, value in self.color_table_lab.items()
                             ]
        return sorted(calculated_deltas, key=lambda x: list(x.values())[0])

    def __generate_files_with_color_tables(self):
        rgb_colors = {}
        lab_colors = {}
        with open(file=self.file_raw, mode='r') as inp, \
                open(file=self.file_lab, mode="w") as out_lab, \
                open(file=self.file_rgb, mode="w") as out_rgb:
            for line in inp:
                line = line.rstrip('\n')
                name, r, g, b = line.split('	')
                c = Color(int(r), int(g), int(b))
                rgb_colors[name] = c.rgb_values
                lab_colors[name] = c.lab_values
            json.dump(lab_colors, fp=out_lab)
            json.dump(rgb_colors, fp=out_rgb)
        log.info(f"generated files for color tables {self.file_lab} and {self.file_rgb}")


# if __name__ == '__main__':
#     init_logging("log.log")
#     table = ColorTable()
#     my_color = Color(0, 0, 0)
#     nearest_color = table.calculate_deltas(my_color.lab)[0]
#     print(nearest_color)
