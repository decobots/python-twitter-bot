import pytest

from twitter import Twitter
from unittest import mock
import base64


@pytest.fixture
def local_picture():
    with open("test_pic.jpg", "br") as f:
        return f.read()


def upload_photo_mock_request(*args, **kwargs):
    m = mock.MagicMock()
    if kwargs['payload']['media_data'] == base64.b64encode(local_picture()):
        m.text = '''{"media_id": 710511363345354753}'''
    else:  # actually not used
        m.text = '{"errors":[{"code":215,"message":"Bad Authentication data."}]}'
    return m


def test_upload_photo_correct(local_picture):
    twitter = Twitter(upload_photo_mock_request)
    returned_id, returned_name = twitter.upload_photo(name="Test_name", data=local_picture)
    assert returned_id is not None
    assert returned_name is not None
    assert isinstance(returned_id, int)
    assert isinstance(returned_name, str)
    assert returned_id != ''
    assert returned_name != ''


def test_upload_photo_incorrect():
    twitter = Twitter(upload_photo_mock_request)
    not_picture = "string"
    with pytest.raises(TypeError):  # raised by base64
        twitter.upload_photo(name="Test_name", data=not_picture)


def create_post_mock_request(*args, **kwargs):
    m = mock.MagicMock()
    m.content = b'''{"id": 243145735212777472}'''
    return m


def test_create_post_correct():
    twitter = Twitter(create_post_mock_request)
    result = twitter.create_post(status="Test_status", id_of_photo=1234567)
    assert isinstance(result, int)


def get_users_posts_correct_mock_request(*args, **kwargs):
    m = mock.MagicMock()
    m.content = b'''[
                    {"id": 850007368138018817},
                    {"id": 848930551989915648}
                ]'''
    return m


def test_get_users_posts_correct():
    twitter = Twitter(get_users_posts_correct_mock_request)
    number_of_posts = 2
    result = twitter.get_users_posts(number_of_posts)
    assert len(result) == number_of_posts
    for item in result:
        assert isinstance(item, int)


def test_delete_tweet_by_id_correct():
    twitter = Twitter(mock.MagicMock())
    twitter.delete_tweet_by_id(tweet_id=123456)
