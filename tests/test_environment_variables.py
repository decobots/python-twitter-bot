import logging

import pytest

from src.environment_variables import get_env
from src.logger import init_logging, log_func_name_ended, log_func_name_started

log = logging.getLogger()


def setup_module():
    init_logging("test_log.log")
    log.debug("environment_variables test started")


def teardown_module():
    log.debug("environment_variables test ended")


def setup_function(func):
    log_func_name_started(func)


def teardown_function(func):
    log_func_name_ended(func)


def test_environment_variables_correct(global_variable):
    assert get_env(global_variable[0]) == global_variable[1]


def test_environment_variables_not_defined():
    with pytest.raises(OSError):
        get_env("undefined_variable_name")
