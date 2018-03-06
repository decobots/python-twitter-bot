import logging
import os

log = logging.getLogger()


def init_logging(filename):
    if hasattr(log, "initialized") and log.initialized:
        return

    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename=log_path)
    file_formatter = logging.Formatter(
        fmt="%(asctime)s [%(name)s:%(levelname)s:%(module)s:%(funcName)s] %(message)s")
    console_formatter = logging.Formatter(
        fmt="\n%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    log.addHandler(file_handler)
    log.addHandler(console_handler)
    log.setLevel(logging.DEBUG)
    for logger_name in ("urllib3", "requests", "oauthlib", "requests_oauthlib.oauth1_auth", "chardet"):
        logging.getLogger(logger_name).setLevel(logging.WARNING)
    log.initialized = True


def log_func_name_started(func):
    log.debug('=' * 10 + f" started {func.__name__}")


def log_func_name_ended(func):
    log.debug('=' * 10 + f" ended {func.__name__}")
