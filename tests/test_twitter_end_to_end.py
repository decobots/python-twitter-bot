import logging
import random

import pytest

from src.data_base import DataBase
from src.logger import init_logging, log_func_name_ended, log_func_name_started
from src.photo import Photo
from src.twitter import Twitter

log = logging.getLogger()

TABLE_NAME = "test_Twitter_end_to_end"


def setup_function(func):
    log_func_name_started(func)


def teardown_function(func):
    log_func_name_ended(func)


@pytest.mark.end_to_end
def setup_module():
    db = DataBase(TABLE_NAME)
    init_logging("test_log.log")
    log.debug("Twitter end to end test started")
    twitter = Twitter(database=db)
    posts = twitter.get_user_posts(100)
    for post in posts:
        twitter._delete_tweet_by_id(post)
    for n in range(0, 13):
        twitter.create_post(status=n)


@pytest.mark.end_to_end
def teardown_module():
    db = DataBase(TABLE_NAME)
    twitter = Twitter(database=db)
    posts = twitter.get_user_posts(300)
    for post in posts:
        twitter._delete_tweet_by_id(post)
    db._delete_table(TABLE_NAME)
    log.debug("Twitter end to end test ended")


@pytest.mark.end_to_end
def test_upload_photo_correct(photo, empty_table):
    twitter = Twitter(database=empty_table)
    result = twitter.upload_photo(photo)
    assert isinstance(result, Photo)
    assert isinstance(result.id_twitter, int)
    assert result.id_twitter != ''


@pytest.mark.end_to_end
def test_upload_photo_incorrect(photo, empty_table):
    twitter = Twitter(database=empty_table)
    photo.data = "string"
    with pytest.raises(TypeError):
        twitter.upload_photo(photo)


@pytest.mark.end_to_end
def test_create_post_correct(photo, empty_table):
    twitter = Twitter(database=empty_table)
    result = twitter.create_post(status=photo.title, photo=photo)
    assert isinstance(result, int)
    result = twitter.create_post(status="test")
    assert isinstance(result, int)
    result = twitter.create_post(photo=photo)
    assert isinstance(result, int)


@pytest.mark.end_to_end
def test_get_users_posts_correct(empty_table):
    twitter = Twitter(database=empty_table)
    number_of_posts = 10
    result = twitter.get_user_posts(number_of_posts)
    assert len(result) == number_of_posts
    for item in result:
        assert isinstance(item, int)


@pytest.mark.end_to_end
def test_delete_tweet_by_id_no_photo_correct(empty_table):
    twitter = Twitter(database=empty_table)
    tw_id = twitter.create_post(f"test{random.random()}")
    twitter._delete_tweet_by_id(tweet_id=tw_id)
