import logging

import pytest

from src.environment_variables import get_env
from src.logger import init_logging
from tests.decorators import log_test_name

log = logging.getLogger()


@log_test_name
def setup_module():
    init_logging("test_log.log")
    log.debug("DataBase test started")


@log_test_name
def teardown_module():
    log.debug("DataBase test ended")


@log_test_name
def test_environment_variables_correct(global_variable):
    assert get_env(global_variable[0]) == global_variable[1]


@log_test_name
def test_environment_variables_not_defined():
    with pytest.raises(OSError):
        get_env("undefined_variable_name")
