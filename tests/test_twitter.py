import json
import logging
from unittest import mock

import pytest

from src.logger import init_logging
from src.photo import Photo
from src.twitter import Twitter
from tests.decorators import log_test_name

log = logging.getLogger()


@log_test_name
def setup_module():
    init_logging("test_log.log")
    log.info("unit test Twitter started")


@log_test_name
def teardown_module():
    log.info("unit test Twitter ended")


@log_test_name
def test_upload_photo_correct(photo, requester, db):
    requester.return_value.text = json.dumps({"media_id": 710511363345354753})
    twitter = Twitter(requester=requester, database=db)
    result = twitter.upload_photo(photo=photo)
    assert isinstance(result, Photo)
    assert result.id_twitter == 710511363345354753


@log_test_name
def test_upload_photo_incorrect(photo, requester, db):
    twitter = Twitter(requester=requester, database=db)
    photo.data = "string"
    with pytest.raises(TypeError):  # raised by base64
        twitter.upload_photo(photo=photo)


@log_test_name
def test_create_post_text_and_photo_correct(photo, requester, db):
    requester.return_value.content = json.dumps({"id": 243145735212777472})
    db.post_photo = mock.MagicMock()
    twitter = Twitter(requester=requester, database=db)
    result = twitter.create_post(status="Test_status", photo=photo)
    assert result == 243145735212777472


@log_test_name
def test_create_post_text_only_correct(requester, db):
    requester.return_value.content = json.dumps({"id": 243145735212777472})
    db.post_photo = mock.MagicMock()
    twitter = Twitter(requester=requester, database=db)
    result = twitter.create_post(status="Test_status")
    assert result == 243145735212777472


@log_test_name
def test_create_post_photo_only_correct(photo, requester, db):
    requester.return_value.content = json.dumps({"id": 243145735212777472})
    db.post_photo = mock.MagicMock()
    twitter = Twitter(requester=requester, database=db)
    result = twitter.create_post(photo=photo)
    assert result == 243145735212777472


@log_test_name
def test_get_users_posts_correct(requester, db):
    requester.return_value.content = json.dumps([
        {"id": 850007368138018817},
        {"id": 848930551989915648}
    ])
    twitter = Twitter(requester=requester, database=db)
    number_of_posts = 2
    result = twitter.get_user_posts(number_of_posts)
    assert len(result) == number_of_posts
    assert result[0] == 850007368138018817
    assert result[1] == 848930551989915648


@log_test_name
def test_delete_tweet_by_id_correct(requester, db):
    db.delete_photo_from_twitter = mock.MagicMock()
    db.delete_photo_from_twitter.return_value = 0
    twitter = Twitter(requester=requester, database=db)
    twitter._delete_tweet_by_id(tweet_id=123456)
