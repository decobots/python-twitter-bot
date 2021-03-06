import logging
import random

import pytest

from src.data_base import PhotoTable, DataBase
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
    init_logging("test_log.log")
    log.debug("Twitter end to end test started")
    db = DataBase()
    table = PhotoTable(db=db, table_name=TABLE_NAME)
    twitter = Twitter(table=table)
    posts = twitter.get_user_posts(100)
    for post in posts:
        twitter._delete_tweet_by_id(post)
    for n in range(0, 3):
        twitter.create_post(status=n)


@pytest.mark.end_to_end
def teardown_module():
    db = DataBase()
    table = PhotoTable(db=db, table_name=TABLE_NAME)
    twitter = Twitter(table=table)
    posts = twitter.get_user_posts(300)
    for post in posts:
        twitter._delete_tweet_by_id(post)
    table._delete()
    log.debug("Twitter end to end test ended")


@pytest.mark.end_to_end
def test_upload_photo_correct(photo, empty_table):
    twitter = Twitter(table=empty_table)
    empty_table.add_photos({photo.id_flickr:photo})
    result = twitter.upload_photo(photo)
    assert isinstance(result, Photo)
    assert isinstance(result.id_twitter, int)
    assert result.id_twitter != ''


@pytest.mark.end_to_end
def test_upload_photo_incorrect(photo, empty_table):
    twitter = Twitter(table=empty_table)
    photo.data = "string"
    with pytest.raises(TypeError):
        twitter.upload_photo(photo)


@pytest.mark.end_to_end
def test_create_post_correct(photo, empty_table):
    twitter = Twitter(table=empty_table)
    empty_table.add_photos({photo.id_flickr:photo})
    twitter.upload_photo(photo)
    result = twitter.create_post(status=photo.title, photo=photo)
    assert isinstance(result, str)
    result = twitter.create_post(status="test")
    assert isinstance(result, str)
    result = twitter.create_post(photo=photo)
    assert isinstance(result, str)


@pytest.mark.end_to_end
def test_get_users_posts_correct(empty_table):
    twitter = Twitter(table=empty_table)
    number_of_posts = 3
    result = twitter.get_user_posts(number_of_posts)
    assert len(result) == number_of_posts
    for item in result:
        assert isinstance(item, int)


@pytest.mark.end_to_end
def test_delete_tweet_by_id_no_photo_correct(empty_table):
    twitter = Twitter(table=empty_table)
    tw_id = twitter.create_post(f"test{random.random()}")
    twitter._delete_tweet_by_id(tweet_id=tw_id)


@pytest.mark.end_to_end
def test_delete_tweet_by_id_with_photo_correct(empty_table, photo):
    twitter = Twitter(table=empty_table)
    empty_table.add_photos({photo.id_flickr: photo})
    pic = twitter.upload_photo(photo)
    tw_id = twitter.create_post(status=f"test{random.random()}", photo=pic)
    twitter._delete_tweet_by_id(tweet_id=tw_id)
    posted = empty_table.db.select(
        query="SELECT * FROM {} WHERE id=%s",
        identifiers=[TABLE_NAME],
        arguments=(photo.id_flickr,))
    assert posted == [(photo.id_flickr, False, None)]
