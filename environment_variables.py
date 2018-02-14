import os


def get_env(name):
    value = os.getenv(name)
    if value is None:
        raise OSError(f"Global Variable {name} is not defined")
    elif value == "":
        raise ValueError(f"global variable {name} could not be empty string")
    return value


TWITTER_CONSUMER_KEY = get_env("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = get_env("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_KEY = get_env("TWITTER_ACCESS_KEY")
TWITTER_ACCESS_SECRET = get_env("TWITTER_ACCESS_SECRET")
FLICKR_API_KEY = get_env("FLICKR_API_KEY")
