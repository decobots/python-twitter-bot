import math
import os
from typing import List, Callable

import colormath.color_diff
import colormath.color_objects

from src.color_table import Color, ColorTable, DATA_DEFAULT_PATH, colors_delta
from src.svgmaker import create_svg



def nearest_color(clr: colormath.color_objects.LabColor, method: Callable) -> 'colors_delta':
    return method(clr_lab=clr)


def colormath_cie1976(color_table, input_color: 'Color') -> List['colors_delta']:
    calculated_deltas = []
    for table_color in color_table:
        delta = colormath.color_diff.delta_e_cie1976(input_color.lab, table_color.lab)
        calculated_deltas.append(colors_delta(table_color, delta))
    return sorted(calculated_deltas, key=lambda x: x.delta)


def colormath_cie1994(color_table, input_color: 'Color') -> List['colors_delta']:
    calculated_deltas = []
    for table_color in color_table:
        delta = colormath.color_diff.delta_e_cie1994(input_color.lab, table_color.lab)
        calculated_deltas.append(colors_delta(table_color, delta))
    return sorted(calculated_deltas, key=lambda x: x.delta)


def colormath_cie2000(color_table, input_color: 'Color') -> List['colors_delta']:
    calculated_deltas = []
    for table_color in color_table:
        delta = colormath.color_diff.delta_e_cie2000(input_color.lab, table_color.lab)
        calculated_deltas.append(colors_delta(table_color, delta))
    return sorted(calculated_deltas, key=lambda x: x.delta)


def colormath_cms(color_table, input_color: 'Color') -> List['colors_delta']:
    calculated_deltas = []
    for table_color in color_table:
        delta = colormath.color_diff.delta_e_cmc(input_color.lab, table_color.lab)
        calculated_deltas.append(colors_delta(table_color, delta))
    return sorted(calculated_deltas, key=lambda x: x.delta)


def simple_Euclidean_distance(color_table, input_color: 'Color'): # I will use it
    lc, ac, bc = input_color.lab_values  # lab of Color
    calculated_deltas = []
    for table_color in color_table:
        lt, at, bt = table_color.lab_values  # lab of cilor in Table
        delta = math.sqrt(pow(lt - lc, 2) + pow(at - ac, 2) + pow(bt - bc, 2))
        calculated_deltas.append(colors_delta(table_color, delta))
    return sorted(calculated_deltas, key=lambda x: x.delta)


def lab_weighted_Euclidean_distance(color_table, input_color: 'Color'):
    lc, ac, bc = input_color.lab_values  # lab of Color
    calculated_deltas = []
    for table_color in color_table:
        lt, at, bt = table_color.lab_values  # lab of cilor in Table
        delta = math.sqrt(2 * pow(lt - lc, 2) + pow(at - ac, 2) + pow(bt - bc, 2))
        calculated_deltas.append(colors_delta(table_color, delta))
    return sorted(calculated_deltas, key=lambda x: x.delta)





def generate_colors(color_table: ColorTable, methods: List[Callable] = None, number_of_colors: int = 10) -> List[
    List['colors_delta']]:
    lst = []
    colors = [Color(0, 0, 0)]
    print('modulate_colors')
    modulate_color(stop_color=(255, 0, 0), arr=colors)  # red
    modulate_color(stop_color=(255, 255, 255), arr=colors)
    modulate_color(stop_color=(255, 255, 0), arr=colors)  # cyan
    modulate_color(stop_color=(0, 0, 0), arr=colors)
    modulate_color(stop_color=(0, 255, 0), arr=colors)  # green
    modulate_color(stop_color=(255, 255, 255), arr=colors)
    modulate_color(stop_color=(0, 255, 255), arr=colors)  # magenta
    modulate_color(stop_color=(0, 0, 0), arr=colors)
    modulate_color(stop_color=(0, 0, 255), arr=colors)  # blue
    modulate_color(stop_color=(255, 255, 255), arr=colors)
    modulate_color(stop_color=(255, 255, 0), arr=colors)  # yellow
    modulate_color(stop_color=(0, 0, 0), arr=colors)
    print('start count deltas')
    for selected_color in colors:
        print(selected_color)
        res = [colors_delta(selected_color, 0)]
        for func in methods:
            near = func(color_table=color_table.color_table, input_color=selected_color)[0]
            res.append(near)
        lst.append(res)

    return lst


def modulate_color(stop_color, arr, step=10, start_color=None):
    if not start_color:
        start_color = arr[-1].rgb_values
    fs = [None] * 3
    for start, stop, num in zip(start_color, stop_color, range(3)):
        if abs(start - stop) <= step:
            f = gen_n(start)
        elif start + step < stop:
            f = gen_up(step)
        else:
            f = gen_down(step)

        fs[num] = f
    for red, green, blue in zip(fs[0], fs[1], fs[2]):
        color = Color(r=red, g=green, b=blue)
        arr.append(color)


def gen_up(step=1):
    for _ in range(0, 256, step):
        yield _


def gen_down(step=1):
    for _ in range(255, -1, -step):
        yield _


def gen_n(n):
    while True:
        yield n


if __name__ == '__main__':
    tab = ColorTable(path_to_raw_data=os.path.join(DATA_DEFAULT_PATH, 'colors3.txt'))

    # colors = generate_colors(color_table=tab, number_of_colors=1000, methods=[
    #     simple_Euclidean_distance,
    # ]
    #                          )

    colors = generate_colors(color_table=tab, number_of_colors=300, methods=[colormath_cie1976,
                                                                             colormath_cie1994,
                                                                             colormath_cie2000,
                                                                             colormath_cms,
                                                                             simple_Euclidean_distance,
                                                                             lab_weighted_Euclidean_distance,
                                                                             ]
                             )
    # create_svg(colors, filename='test_deltas_colors2.svg')

    # cd = [[colors_delta(c, 0)] for c in tab.color_table]
    #
    # print(colors)
    create_svg(colors, "colors2_tests.svg")
