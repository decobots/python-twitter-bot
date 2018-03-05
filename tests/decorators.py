import logging
from functools import wraps

log = logging.getLogger()


def log_test_name(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        log.debug(f"==================================================== started {func.__name__}")
        func(*args, **kwargs)
        log.debug(f"==================================================== ended {func.__name__}")

    return decorator
