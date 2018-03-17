import json
from typing import Dict, List

import colormath.color_conversions
import colormath.color_diff
import colormath.color_objects


class ColorTable:
    def __init__(self, filename_lab: str = 'out_lab.txt', filename_rgb: str = 'out_rgb.txt'):
        self.file_lab = filename_lab
        self.file_rgb = filename_rgb
        self.color_table_lab = self._load_colors_table_lab()
        self.color_table_rgb = None

    def _load_colors_table_lab(self) -> Dict[str, colormath.color_objects.LabColor]:
        with open(file=self.file_lab, mode="r") as file:
            lab_colors = json.load(fp=file)
            return {name: colormath.color_objects.LabColor(*values) for name, values in lab_colors.items()}

    def calculate_deltas(self, pic_clr: "Color") -> List[Dict[str, colormath.color_objects.LabColor]]:
        calculated_deltas = [{name: colormath.color_diff.delta_e_cie1976(pic_clr, value)}
                             for name, value in self.color_table_lab.items()
                             ]
        return sorted(calculated_deltas, key=lambda x: list(x.values())[0])

    @staticmethod
    def __generate_files_with_color_tables():
        rgb_colors = {}
        lab_colors = {}
        with open(file="colors.txt", mode='r') as inp, \
                open(file="out_lab.txt", mode="w") as out_lab, \
                open(file="out_rgb.txt", mode="w") as out_rgb:
            for line in inp:
                line = line.rstrip('\n')
                name, r, g, b = line.split('	')
                rgb = colormath.color_objects.AdobeRGBColor(rgb_r=int(r), rgb_g=int(g), rgb_b=int(b))
                lab = colormath.color_conversions.convert_color(
                    color=rgb,
                    target_cs=colormath.color_objects.LabColor)
                rgb_colors[name] = rgb.get_value_tuple()
                lab_colors[name] = lab.get_value_tuple()
            json.dump(lab_colors, fp=out_lab)
            json.dump(rgb_colors, fp=out_rgb)


class Color:
    def __init__(self, r: int, g: int, b: int):
        self.rgb = colormath.color_objects.AdobeRGBColor(rgb_r=r, rgb_g=g, rgb_b=b)
        self.lab = colormath.color_conversions.convert_color(
            color=self.rgb,
            target_cs=colormath.color_objects.LabColor)


if __name__ == '__main__':
    # generate_files_with_color_tables()
    table = ColorTable()
    my_color = Color(0, 0, 0)
    nearest_color = table.calculate_deltas(my_color.lab)[0]
    print(nearest_color)
