import logging

import pytest

from src.data_base import DataBase
from src.flickr import Flickr
from src.logger import init_logging, log_func_name_ended, log_func_name_started
from src.photo import Photo

TABLE_NAME = "test_flickr_end_to_end"

log = logging.getLogger()


@pytest.mark.end_to_end
def setup_module():
    init_logging("test_log.log")
    log.debug("Flickr end to end test started")


@pytest.mark.end_to_end
def teardown_module():
    db = DataBase(TABLE_NAME)
    db._delete_table(TABLE_NAME)
    log.debug("Flickr end to end test ended")


def setup_function(func):
    log_func_name_started(func)


def teardown_function(func):
    log_func_name_ended(func)


@pytest.mark.end_to_end
def test_flickr_get_photos_list_correct(db):
    """
    check that returned value is list and attributes farm, server, id, secret exist for each list item
    """
    flickr = Flickr(database=db)
    result = flickr.get_photos()
    assert isinstance(result, dict)
    assert result != {}
    for photo_id, photo in result.items():
        assert isinstance(photo, Photo)
        assert photo.farm is not None
        assert photo.server is not None
        assert photo.id_flickr is not None
        assert photo.secret is not None
        assert photo_id == photo.id_flickr


@pytest.mark.end_to_end
def test_flickr_get_photo_correct(db):
    """
    check that returned value exist and have types bytes and string
    """
    flickr = Flickr(database=db)
    photo = flickr.get_photo(Photo(id_flickr="24003882568",
                                   secret="ca14f88bec",
                                   server="4504",
                                   title="test",
                                   farm="5"))
    assert photo is not None
    # assert photo.data == b"/ff/ff"
    assert isinstance(photo.data, bytes)


@pytest.mark.end_to_end
def test_flickr_get_photo_incorrect(db):
    flickr = Flickr(database=db)
    with pytest.raises(ValueError):
        flickr.get_photo(Photo(id_flickr="24003882568",
                               secret="ca14f88bec",
                               server="45004",
                               title="test",
                               farm="5"))
        # invalid server
