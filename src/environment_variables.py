import os


def get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise OSError(f"Global Variable {name} is not defined")
    elif value == "":
        raise ValueError(f"global variable {name} could not be empty string")
    return value
