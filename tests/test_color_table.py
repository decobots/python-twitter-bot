import pytest

from src.color_table import Color, ColorTable
import colormath.color_objects
import colormath.color_conversions


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
    test_table = ColorTable(filename_raw_data="colors_test.txt",
                            filename_lab_out="lab_test_txt",
                            filename_rgb_out="rgb_test.txt")

