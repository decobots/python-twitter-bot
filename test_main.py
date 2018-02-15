import os
import pytest

from environment_variables import get_env
from flickr import Flickr
import twitter


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


def test_flickr_get_photos_list_correct():
    """
    check that returned value is list and attributes farm, server, id, secret exist for each list item
    """
    flickr = Flickr()
    flickr_get_photos_result = flickr.get_photos()
    assert isinstance(flickr_get_photos_result, list)
    for photo in flickr_get_photos_result:
        assert isinstance(photo, dict)
        assert photo["farm"] is not None
        assert photo["server"] is not None
        assert photo["id"] is not None
        assert photo["secret"] is not None


def test_flickr_get_photo_correct():
    """
    check that returned value exist and have types bytes and string
    """
    flickr = Flickr()
    test_flickr_get_photo_result_binary, test_flickr_get_photo_result_name = flickr.get_photo(
        {"farm": "5", "server": "4368", "id": "372637598620", "secret": "5bc41f375d", "title": "test"})
    assert test_flickr_get_photo_result_binary is not None
    assert test_flickr_get_photo_result_name is not None
    assert test_flickr_get_photo_result_binary, bytes is not None
    assert test_flickr_get_photo_result_name, str is not None


def _test_flickr_get_photo_empty_input():
    with pytest.raises(ValueError):
        flickr = Flickr()
        flickr.get_photo()


def _test_flickr_get_photo_with_incorrect_input_type():
    with pytest.raises(ValueError):
        flickr = Flickr()
        flickr.get_photo([])


def _test_flickr_get_photo_incorrect_input():
    test_flickr_get_photo_result_binary2, test_flickr_get_photo_result_name2 = flickr_get_photo(
        {"farm": "7", "server": "7", "id": "7", "secret": "7", "title": "7"})
    assert test_flickr_get_photo_result_binary2 is not None
    assert test_flickr_get_photo_result_name2 is not None
