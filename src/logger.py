import logging
import os


def init_logging(filename):
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
    log = logging.getLogger()
    handler = logging.FileHandler(filename=log_path)
    formatter = logging.Formatter(fmt="%(asctime)s:%(levelname)s: %(message)s")
    log.addHandler(handler)
    handler.setFormatter(formatter)
    log.setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("oauthlib").setLevel(logging.WARNING)
    logging.getLogger("requests_oauthlib.oauth1_auth").setLevel(logging.WARNING)
