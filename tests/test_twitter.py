import json
from unittest import mock

import pytest

from src.photo import Photo
from src.twitter import Twitter
import os


@pytest.fixture
def photo():
    print("----------------------------------------------------")
    print(os.getcwd())
    photo_mock = Photo(id_flickr="2636", secret="a123456",
                       server="2",
                       title="test_04",
                       farm="5")
    with open(os.path.join(os.getcwd(),"test_pic.jpg"), "br") as f:
        photo_mock.data = f.read()

    return photo_mock


def test_upload_photo_correct(photo):
    requester = mock.MagicMock()
    requester.return_value = mock.MagicMock()
    requester.return_value.text = json.dumps({"media_id": 710511363345354753})
    db = mock.MagicMock()
    twitter = Twitter(requester=requester, database=db)
    result = twitter.upload_photo(photo=photo)
    assert isinstance(result, Photo)
    assert result.id_twitter == 710511363345354753


def test_upload_photo_incorrect(photo):
    db = mock.MagicMock()
    twitter = Twitter(requester=mock.MagicMock(), database=db)
    photo.data = "string"
    with pytest.raises(TypeError):  # raised by base64
        twitter.upload_photo(photo=photo)


def test_create_post_text_and_photo_correct(photo):
    requester = mock.MagicMock()
    requester.return_value = mock.MagicMock
    requester.return_value.content = json.dumps({"id": 243145735212777472})
    db = mock.MagicMock()
    db.post_photo = mock.MagicMock()
    twitter = Twitter(requester=requester, database=db)
    result = twitter.create_post(status="Test_status", photo=photo)
    assert result == 243145735212777472


def test_create_post_text_only_correct():
    requester = mock.MagicMock()
    requester.return_value = mock.MagicMock
    requester.return_value.content = json.dumps({"id": 243145735212777472})
    db = mock.MagicMock()
    db.post_photo = mock.MagicMock()
    twitter = Twitter(requester=requester, database=db)
    result = twitter.create_post(status="Test_status")
    assert result == 243145735212777472


def test_create_post_photo_only_correct(photo):
    requester = mock.MagicMock()
    requester.return_value = mock.MagicMock
    requester.return_value.content = json.dumps({"id": 243145735212777472})
    db = mock.MagicMock()
    db.post_photo = mock.MagicMock()
    twitter = Twitter(requester=requester, database=db)
    result = twitter.create_post(photo=photo)
    assert result == 243145735212777472


def test_get_users_posts_correct():
    requester = mock.MagicMock()
    requester.return_value = mock.MagicMock
    requester.return_value.content = json.dumps([
        {"id": 850007368138018817},
        {"id": 848930551989915648}
    ])
    db = mock.MagicMock()
    twitter = Twitter(requester=requester, database=db)
    number_of_posts = 2
    result = twitter.get_user_posts(number_of_posts)
    assert len(result) == number_of_posts
    assert result[0] == 850007368138018817
    assert result[1] == 848930551989915648


def test_delete_tweet_by_id_correct():
    db = mock.MagicMock()
    db.delete_photo_from_twitter = mock.MagicMock()
    twitter = Twitter(requester=mock.MagicMock(), database=db)
    twitter._delete_tweet_by_id(tweet_id=123456)
