import pytest

from flickr import Flickr


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
        {"farm": "5", "server": "4504", "id": "24003882568", "secret": "ca14f88bec", "title": "test"})
    assert test_flickr_get_photo_result_binary is not None
    assert test_flickr_get_photo_result_name is not None
    assert isinstance(test_flickr_get_photo_result_binary, bytes)
    assert isinstance(test_flickr_get_photo_result_name, str)

def test_flickr_get_photo_incorrect():
    flickr = Flickr()
    with pytest.raises(ValueError):
        flickr.get_photo(
            {"farm": "5", "server": "450904", "id": "24003882568", "secret": "ca14f88bec", "title": "test"})
        # invalid server


def _test_flickr_get_photo_with_incorrect_input_type():
    with pytest.raises(ValueError):
        flickr = Flickr()
        flickr.get_photo([])


def _test_flickr_get_photo_incorrect_input():
    flickr = Flickr()
    test_flickr_get_photo_result_binary2, test_flickr_get_photo_result_name2 = flickr.get_photo(
        {"farm": "7", "server": "7", "id": "7", "secret": "7", "title": "7"})
    assert test_flickr_get_photo_result_binary2 is not None
    assert test_flickr_get_photo_result_name2 is not None
