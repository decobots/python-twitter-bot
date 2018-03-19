import logging
import os

import pytest

from src.color_table import Color, ColorTable, colors_delta
from src.logger import init_logging

log = logging.getLogger()

TEST_DATA_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'test_data')

COLORS_FILE = "colors_test.txt"


def setup_module():
    init_logging("test_log.log")


def test_color_correct():
    c = Color(0, 0, 0)
    assert c.rgb_values == (0, 0, 0)
    assert c.lab_values == (0, 0, 0)
    assert c.hex == '#000000'

    c = Color(255, 255, 255)
    assert c.rgb_values == (255, 255, 255)
    assert c.hex == '#ffffff'
    assert tuple(int(v) for v in c.lab_values) == (100, 0, 0)  # library returns floats that not exactly the 100,0,0


def test_color_incorrect():
    with pytest.raises(ValueError):
        Color(300, 125, 125)


def test_eq_correct():
    # color names not used in comparison
    c1 = Color(0, 0, 0)
    c2 = Color(0, 0, 0, 'Black')
    c3 = Color(0, 0, 0, 'Red')

    c4 = Color(100, 100, 100)
    c5 = Color(100, 100, 100, 'Black')
    assert c1 == c2 == c3
    assert c1 != c4
    assert c2 != c5


def test_rgb_values():
    c = Color(125, 125, 125)
    assert c.rgb_values == (125, 125, 125)


def test_lab_values():
    c = Color(0, 0, 0)
    assert c.lab_values == (0, 0, 0)


def test_color_table_if_lab_and_rdb_files_deleted():
    test_table = ColorTable(path_to_raw_data=os.path.join(TEST_DATA_DEFAULT_PATH, COLORS_FILE), )
    # can't actually compare LAB colors
    assert len(test_table.color_table) == 3
    assert test_table.color_table[0].lab_values == Color(206, 151, 50).lab_values
    assert test_table.color_table[1].lab_values == Color(176, 172, 174).lab_values
    assert test_table.color_table[2].lab_values == Color(190, 178, 154).lab_values


def test_nearest_color():
    color1 = Color(0, 0, 0)
    color2 = Color(255, 255, 255)
    test_table = ColorTable(path_to_raw_data=os.path.join(TEST_DATA_DEFAULT_PATH, COLORS_FILE))
    assert test_table.nearest_color(color1.lab) == colors_delta(Color(176, 172, 174, 'Ajay'), 71.44594936202925)
    assert test_table.nearest_color(color2.lab) == colors_delta(Color(176, 172, 174, 'Ajay'), 28.693146244154423)
