import os
from unittest import mock

import pytest

from src.photo import Photo


@pytest.fixture
def photo():
    photo_mock = Photo(id_flickr="2636", secret="a123456",
                       server="2",
                       title="test_04",
                       farm="5")
    with open(os.path.join(os.getcwd(), "tests", "test_pic.jpg"), "br") as f:
        photo_mock.data = f.read()

    return photo_mock


@pytest.fixture
def requester():
    requester = mock.MagicMock()
    requester.return_value = mock.MagicMock()
    return requester

@pytest.fixture
def db():
    db = mock.MagicMock()
    return db
