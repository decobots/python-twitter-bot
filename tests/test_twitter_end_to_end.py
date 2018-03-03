import random

import pytest

from src.data_base import DataBase
from src.photo import Photo
from src.twitter import Twitter


@pytest.fixture
def photo():
    photo_mock = Photo(id_flickr="2636", secret="a123456",
                       server="2",
                       title="test_04",
                       farm="5")
    with open("test_pic.jpg", "br") as f:
        photo_mock.data = f.read()

    return photo_mock


@pytest.fixture
def tweet_id():
    db = DataBase(photos_table_name="test_twitter_table")
    twitter = Twitter(database=db)
    tw_id = twitter.create_post(f"test{random.random()}")
    return tw_id


@pytest.mark.end_to_end
def test_upload_photo_correct(photo):
    db = DataBase(photos_table_name="test_twitter_table")
    twitter = Twitter(database=db)
    result = twitter.upload_photo(photo)
    assert isinstance(result, Photo)
    assert isinstance(result.id_twitter, int)
    assert result.id_twitter != ''


@pytest.mark.end_to_end
def test_upload_photo_incorrect(photo):
    db = DataBase(photos_table_name="test_twitter_table")
    twitter = Twitter(database=db)
    photo.data = "string"
    with pytest.raises(TypeError):
        twitter.upload_photo(photo)


@pytest.mark.end_to_end
def test_create_post_correct(photo):
    db = DataBase(photos_table_name="test_twitter_table")
    twitter = Twitter(database=db)
    result = twitter.create_post(status=photo.title, photo=photo)
    assert isinstance(result, int)
    result = twitter.create_post(status="test")
    assert isinstance(result, int)
    result = twitter.create_post(photo=photo)
    assert isinstance(result, int)


@pytest.mark.end_to_end
def test_get_users_posts_correct():
    db = DataBase(photos_table_name="test_twitter_table")
    twitter = Twitter(database=db)
    number_of_posts = 10
    result = twitter.get_user_posts(number_of_posts)
    assert len(result) == number_of_posts
    for item in result:
        assert isinstance(item, int)


@pytest.mark.end_to_end
def test_delete_tweet_by_id_correct(tweet_id):
    db = DataBase(photos_table_name="test_twitter_table")
    twitter = Twitter(database=db)
    twitter._delete_tweet_by_id(tweet_id)


@pytest.mark.end_to_end
def setup_module():
    db = DataBase(photos_table_name="test_twitter_table")
    twitter = Twitter(database=db)
    posts = twitter.get_user_posts(100)
    for post in posts:
        twitter._delete_tweet_by_id(post)
    for n in range(0, 13):
        twitter.create_post(status=n)


@pytest.mark.end_to_end
def teardown_module():
    db = DataBase(photos_table_name="test_twitter_table")
    twitter = Twitter(database=db)
    posts = twitter.get_user_posts(300)
    for post in posts:
        twitter._delete_tweet_by_id(post)
