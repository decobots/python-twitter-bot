import os
from contextlib import suppress

import pytest

from src.color_table import Color, ColorTable


def test_color_incorrect():
    with pytest.raises(ValueError):
        c = Color(300, 125, 125)


def test_rgb_values():
    c = Color(125, 125, 125)
    assert c.rgb_values == (125, 125, 125)


def test_lab_values():
    c = Color(0, 0, 0)
    assert c.lab_values == (0, 0, 0)


def test_color_table():
    with suppress(FileNotFoundError):
        os.remove(os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests/lab_test_txt"))
    with suppress(FileNotFoundError):
        os.remove(os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests/rgb_test_txt"))
    test_table = ColorTable(filename_raw_data=os.path.join("tests", "colors_test.txt"),
                            filename_lab_out=os.path.join("tests", "lab_test_txt"),
                            filename_rgb_out=os.path.join("tests", "rgb_test.txt"))
    # can't actually compare LAB colors
    assert len(test_table.color_table_lab) == 3
    assert test_table.color_table_lab['Afterglow'].get_value_tuple() == Color(206, 151, 50).lab_values
    assert test_table.color_table_lab['Ajay'].get_value_tuple() == Color(176, 172, 174).lab_values
    assert test_table.color_table_lab['Akaroa'].get_value_tuple() == Color(190, 178, 154).lab_values
