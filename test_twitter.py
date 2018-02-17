import pytest

from twitter import Twitter


@pytest.fixture
def local_picture():
    with open("test_pic.jpg", "br") as f:
        return f.read()


@pytest.fixture
def picture_id(local_picture):
    twitter = Twitter()
    pic_id, pic_name = twitter.upload_photo("test", local_picture)
    return pic_id


@pytest.fixture
def tweet_id():
    twitter = Twitter()
    tw_id = twitter.create_post("test")
    return tw_id


def test_upload_photo_correct(local_picture):
    twitter = Twitter()
    returned_id, returned_name = twitter.upload_photo(name="Test_name", data=local_picture)
    assert returned_id is not None
    assert returned_name is not None
    assert isinstance(returned_id, int)
    assert isinstance(returned_name, str)
    assert returned_id != ''
    assert returned_name != ''


def test_upload_photo_incorrect(local_picture):
    twitter = Twitter()
    not_picture = "string"
    with pytest.raises(TypeError):
        twitter.upload_photo(name="Test_name", data=not_picture)
    with pytest.raises(TypeError):
        twitter.upload_photo(name=78.6765, data=local_picture)


def test_create_post_correct(picture_id):
    twitter = Twitter()
    twitter.create_post(status="Test_status", id_of_photo=picture_id)


def test_get_users_posts_correct():
    twitter = Twitter()
    number_of_posts = 10
    result = twitter.get_users_posts(number_of_posts)
    assert len(result) == number_of_posts
    for item in result:
        assert isinstance(item, int)


def test_delete_tweet_by_id_correct(tweet_id):
    twitter = Twitter()
    twitter.delete_tweet_by_id(tweet_id)


def setup_module():
    twitter = Twitter()
    for n in range(0, 13):
        twitter.create_post(status=n)


def teardown_module():
    twitter = Twitter()
    posts = twitter.get_users_posts(100)
    for post in posts:
        twitter.delete_tweet_by_id(post)
