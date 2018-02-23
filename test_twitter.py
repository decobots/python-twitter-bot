import json
from unittest import mock

import pytest

from twitter import Twitter


@pytest.fixture
def local_picture():
    with open("test_pic.jpg", "br") as f:
        return f.read()


def test_upload_photo_correct(local_picture):
    m = mock.MagicMock()
    m.return_value = mock.MagicMock()
    m.return_value.text = json.dumps({"media_id": 710511363345354753})
    twitter = Twitter(m)
    returned_id, returned_name = twitter.upload_photo(name="Test_name", data=local_picture)
    assert returned_id is not None
    assert returned_name is not None
    assert isinstance(returned_id, int)
    assert isinstance(returned_name, str)
    assert returned_id != ''
    assert returned_name != ''


def test_upload_photo_incorrect():
    twitter = Twitter(mock.MagicMock())
    not_picture = "string"
    with pytest.raises(TypeError):  # raised by base64
        twitter.upload_photo(name="Test_name", data=not_picture)


def test_create_post_correct():
    m = mock.MagicMock()
    m.return_value = mock.MagicMock
    m.return_value.content = json.dumps({"id": 243145735212777472})
    twitter = Twitter(m)
    result = twitter.create_post(status="Test_status", id_of_photo=1234567)
    assert isinstance(result, int)


def test_get_users_posts_correct():
    m = mock.MagicMock()
    m.return_value = mock.MagicMock
    m.return_value.content = json.dumps([
        {"id": 850007368138018817},
        {"id": 848930551989915648}
    ])
    twitter = Twitter(m)
    number_of_posts = 2
    result = twitter.get_users_posts(number_of_posts)
    assert len(result) == number_of_posts
    for item in result:
        assert isinstance(item, int)


def test_delete_tweet_by_id_correct():
    twitter = Twitter(mock.MagicMock())
    twitter.delete_tweet_by_id(tweet_id=123456)
