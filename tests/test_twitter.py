import json
import logging
from unittest import mock

import pytest

from src.logger import init_logging, log_func_name_ended, log_func_name_started
from src.photo import Photo
from src.twitter import Twitter

log = logging.getLogger()


def setup_module():
    init_logging("test_log.log")
    log.info("unit test Twitter started")


def teardown_module():
    log.info("unit test Twitter ended")


def setup_function(func):
    log_func_name_started(func)


def teardown_function(func):
    log_func_name_ended(func)


def test_upload_photo_correct(photo, mock_requester, mock_db):
    mock_requester.request_json.return_value = {"media_id": 710511363345354753}
    twitter = Twitter(requester=mock_requester, database=mock_db)
    result = twitter.upload_photo(photo=photo)
    assert isinstance(result, Photo)
    assert result.id_twitter == 710511363345354753


def test_upload_photo_incorrect(photo, mock_requester, mock_db):
    twitter = Twitter(requester=mock_requester, database=mock_db)
    photo.data = "string"
    with pytest.raises(TypeError):  # raised by base64
        twitter.upload_photo(photo=photo)


def test_create_post_text_and_photo_correct(photo, mock_requester, mock_db):
    mock_requester.request_json.return_value = {"id": 243145735212777472}
    mock_db.post_photo = mock.MagicMock()
    twitter = Twitter(requester=mock_requester, database=mock_db)
    result = twitter.create_post(status="Test_status", photo=photo)
    assert result == 243145735212777472


def test_create_post_text_only_correct(mock_requester, mock_db):
    mock_requester.request_json.return_value = {"id": 243145735212777472}
    mock_db.post_photo = mock.MagicMock()
    twitter = Twitter(requester=mock_requester, database=mock_db)
    result = twitter.create_post(status="Test_status")
    assert result == 243145735212777472


def test_create_post_photo_only_correct(photo, mock_requester, mock_db):
    mock_requester.request_json.return_value = {"id": 243145735212777472}
    mock_db.post_photo = mock.MagicMock()
    twitter = Twitter(requester=mock_requester, database=mock_db)
    result = twitter.create_post(photo=photo)
    assert result == 243145735212777472


def test_get_users_posts_correct(mock_requester, mock_db):
    mock_requester.request_json.return_value = [
        {"id": 850007368138018817},
        {"id": 848930551989915648}
    ]
    twitter = Twitter(requester=mock_requester, database=mock_db)
    number_of_posts = 2
    result = twitter.get_user_posts(number_of_posts)
    assert len(result) == number_of_posts
    assert result[0] == 850007368138018817
    assert result[1] == 848930551989915648


def test_delete_tweet_by_id_correct(mock_requester, mock_db):
    mock_db.delete_photo_from_twitter = mock.MagicMock()
    mock_db.delete_photo_from_twitter.return_value = 0
    twitter = Twitter(requester=mock_requester, database=mock_db)
    twitter._delete_tweet_by_id(tweet_id=123456)
