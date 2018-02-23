import pytest

from flickr import Flickr
from unittest import mock


def test_flickr_get_photos_list_correct():
    """
    check that returned value is list and attributes farm, server, id, secret exist for each list item
    """
    m = mock.MagicMock()
    m.return_value = mock.MagicMock()
    m.return_value.text = '<photos><photo id="2636" secret="a123456" server="2" title="test_04" /></photos>'
    flickr = Flickr(m)
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
    m = mock.MagicMock()
    m.return_value = mock.MagicMock()
    m.return_value.content = b"/ff/ff"
    flickr = Flickr(m)
    test_flickr_get_photo_result_binary, test_flickr_get_photo_result_name = flickr.get_photo(
        {"farm": "5", "server": "4504", "id": "24003882568", "secret": "ca14f88bec", "title": "test"})
    assert test_flickr_get_photo_result_binary is not None
    assert test_flickr_get_photo_result_name is not None
    assert isinstance(test_flickr_get_photo_result_binary, bytes)
    assert isinstance(test_flickr_get_photo_result_name, str)
