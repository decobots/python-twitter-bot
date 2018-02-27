import os

import pytest

from src.environment_variables import get_env


@pytest.fixture
def global_variable():
    key = "TEST_VARIABLE"
    value = "TEST_VALUE"
    os.environ[key] = value
    yield key, value
    os.environ.pop(key)


def test_environment_variables_correct(global_variable):
    assert get_env(global_variable[0]) == global_variable[1]


def test_environment_variables_not_defined():
    with pytest.raises(OSError):
        get_env("undefined_variable_name")
