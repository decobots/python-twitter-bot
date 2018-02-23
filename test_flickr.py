import pytest

from flickr import Flickr
from unittest import mock


def get_photos_list_correct_mock_request(*args, **kwargs):
    m = mock.MagicMock()
    m.text = '<photos><photo id="2636" secret="a123456" server="2" title="test_04" /></photos>'
    return m


def test_flickr_get_photos_list_correct():
    """
    check that returned value is list and attributes farm, server, id, secret exist for each list item
    """
    flickr = Flickr(get_photos_list_correct_mock_request)
    flickr_get_photos_result = flickr.get_photos()
    assert isinstance(flickr_get_photos_result, list)
    for photo in flickr_get_photos_result:
        assert isinstance(photo, dict)
        assert photo["farm"] is not None
        assert photo["server"] is not None
        assert photo["id"] is not None
        assert photo["secret"] is not None


def get_photo_correct_mock_request(*args, **kwargs):
    m = mock.MagicMock()
    m.content = b"/ff/ff"
    return m


def test_flickr_get_photo_correct():
    """
    check that returned value exist and have types bytes and string
    """
    flickr = Flickr(get_photo_correct_mock_request)
    test_flickr_get_photo_result_binary, test_flickr_get_photo_result_name = flickr.get_photo(
        {"farm": "5", "server": "4504", "id": "24003882568", "secret": "ca14f88bec", "title": "test"})
    assert test_flickr_get_photo_result_binary is not None
    assert test_flickr_get_photo_result_name is not None
    assert isinstance(test_flickr_get_photo_result_binary, bytes)
    assert isinstance(test_flickr_get_photo_result_name, str)


def get_photo_incorrect_mock_request(*args, **kwargs):
    raise ValueError


def test_flickr_get_photo_incorrect():
    flickr = Flickr(get_photo_incorrect_mock_request)
    with pytest.raises(ValueError):
        flickr.get_photo(
            {"farm": "5", "server": "450904", "id": "24003882568", "secret": "ca14f88bec", "title": "test"})
        # invalid server
