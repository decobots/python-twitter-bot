import logging
import os
from contextlib import suppress
from pathlib import Path

import pytest

from src.color_table import Color, ColorTable
from src.logger import init_logging

log = logging.getLogger()

COLORS_FILE = "colors_test.txt"
LAB_FILE = "lab_test_txt"
RGB_FILE = "rgb_test.txt"


def setup_module():
    init_logging("test_log.log")
    test_table = ColorTable(path_to_raw_data=os.path.join(os.path.dirname(__file__), COLORS_FILE),
                            path_to_lab_out=os.path.join(os.path.dirname(__file__), LAB_FILE),
                            path_to_rgb_out=os.path.join(os.path.dirname(__file__), RGB_FILE))


def test_color_correct():
    c = Color(0, 0, 0)
    assert c.rgb_values == (0, 0, 0)
    assert c.lab_values == (0, 0, 0)

    c = Color(255, 255, 255)
    assert c.rgb_values == (255, 255, 255)
    assert tuple(int(v) for v in c.lab_values) == (100, 0, 0)  # library returns floats that not exactly the 100,0,0


def test_color_incorrect():
    with pytest.raises(ValueError):
        Color(300, 125, 125)


def test_rgb_values():
    c = Color(125, 125, 125)
    assert c.rgb_values == (125, 125, 125)


def test_lab_values():
    c = Color(0, 0, 0)
    assert c.lab_values == (0, 0, 0)


def test_color_table_if_lab_and_rdb_files_deleted():
    with suppress(FileNotFoundError):
        os.remove(os.path.join(os.path.dirname(__file__), "lab_test_txt"))
    with suppress(FileNotFoundError):
        os.remove(os.path.join(os.path.dirname(__file__), "rgb_test.txt"))
    test_table = ColorTable(path_to_raw_data=os.path.join(os.path.dirname(__file__), COLORS_FILE),
                            path_to_lab_out=os.path.join(os.path.dirname(__file__), LAB_FILE),
                            path_to_rgb_out=os.path.join(os.path.dirname(__file__), RGB_FILE))
    assert Path(os.path.join(os.path.dirname(__file__), "lab_test_txt")).exists() is True
    assert Path(os.path.join(os.path.dirname(__file__), "rgb_test.txt")).exists() is True
    # can't actually compare LAB colors
    assert len(test_table.color_table_lab) == 3
    assert test_table.color_table_lab['Afterglow'].get_value_tuple() == Color(206, 151, 50).lab_values
    assert test_table.color_table_lab['Ajay'].get_value_tuple() == Color(176, 172, 174).lab_values
    assert test_table.color_table_lab['Akaroa'].get_value_tuple() == Color(190, 178, 154).lab_values


def test_calculate_deltas():
    color1 = Color(0, 0, 0)
    color2 = Color(255, 255, 255)
    test_table = ColorTable(path_to_raw_data=os.path.join(os.path.dirname(__file__), COLORS_FILE),
                            path_to_lab_out=os.path.join(os.path.dirname(__file__), LAB_FILE),
                            path_to_rgb_out=os.path.join(os.path.dirname(__file__), RGB_FILE))
    assert test_table.calculate_deltas(color1.lab)[0] == {'Ajay': 71.44594936202925}
    assert test_table.calculate_deltas(color2.lab)[0] == {'Ajay': 28.693146244154423}
