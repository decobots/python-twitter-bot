import base64
import logging
from unittest import mock

from src.flickr import Flickr
from src.logger import init_logging, log_func_name_ended, log_func_name_started
from src.photo import Photo

log = logging.getLogger()


def setup_module():
    init_logging("test_log.log")
    log.debug("Flickr test started")


def teardown_module():
    log.debug("flickr test ended")


def setup_function(func):
    log_func_name_started(func)


def teardown_function(func):
    log_func_name_ended(func)


def test_flickr_get_photos_list_correct(requester, db):
    """
    check that returned value is dict of photos and attributes farm, server, id, secret exist and correct for each photo
    """
    requester.return_value.text = """<rsp stat="ok"><photos>
                                    <photo id="2636" secret="a123456" server="2" title="test_04" farm="5"/>
                                    </photos></rsp>"""
    db.add_photo = mock.MagicMock()
    flickr = Flickr(requester=requester, database=db)
    flickr_get_photos_result = flickr.get_photos()
    assert isinstance(flickr_get_photos_result, dict)
    assert flickr_get_photos_result != {}
    for photo_id, photo in flickr_get_photos_result.items():
        assert isinstance(photo, Photo)
        assert photo.farm == "5"
        assert photo.server == "2"
        assert photo.id_flickr == "2636"
        assert photo.secret == "a123456"
        assert photo_id == photo.id_flickr


def test_flickr_get_photo_correct(requester, db):
    """
    check that returned value exist and correct
    """
    requester.return_value.content = b"/ff/ff"
    flickr = Flickr(requester=requester, database=db)
    photo = flickr.get_photo(Photo(id_flickr="2636", secret="a123456",
                                   server="2",
                                   title="test_04",
                                   farm="5"))
    assert photo is not None
    assert photo.data == base64.b64encode(b"/ff/ff")


def test_random_photo_correct(requester, db):
    db.unposted_photos = mock.MagicMock()
    db.unposted_photos.return_value = ['1', '2']
    flickr = Flickr(requester=requester, database=db)
    photos = {"1": Photo(id_flickr="1", farm="1", server="1", secret="1", title="1"),
              "2": Photo(id_flickr="2", farm="2", server="2", secret="2", title="2")}
    result = flickr.random_photo(photos)
    assert isinstance(result, Photo)
