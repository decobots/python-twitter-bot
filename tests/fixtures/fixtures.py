import os
from unittest import mock

import pytest

from src.data_base import DataBase
from src.photo import Photo


@pytest.fixture()
def global_variable():
    key = "TEST_VARIABLE"
    value = "TEST_VALUE"
    os.environ[key] = value
    yield key, value
    os.environ.pop(key)


@pytest.fixture
def photo():
    photo_mock = Photo(id_flickr="2636", secret="a123456",
                       server="2",
                       title="test_04",
                       farm="5")
    pic_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_pic.jpg")
    with open(pic_path, "br") as f:
        photo_mock.data = f.read()

    return photo_mock


@pytest.fixture
def mock_requester():
    req = mock.MagicMock()
    req.request_json = mock.MagicMock()
    req.request_xml = mock.MagicMock()
    req.request_binary = mock.MagicMock()
    req.request_json.return_value = mock.MagicMock()
    req.request_xml.return_value = mock.MagicMock()
    req.request_binary.return_value = mock.MagicMock()
    req.__class__ = "mock_requester"
    return req


@pytest.fixture
def mock_request_response():
    import requests
    requests.request = mock.MagicMock()
    requests.request.return_value = mock.MagicMock()

    return requests.request.return_value


@pytest.fixture
def mock_db():
    dbs = mock.MagicMock()
    dbs.photos_table_name = "mock_table"
    return dbs


TEST_IDS = "42", "43", "44"


@pytest.fixture()
def db(request):
    name = getattr(request.module, "TABLE_NAME", None)
    database = DataBase(name)
    yield database
    database.close()


@pytest.fixture
def empty_table(db):
    db._clear_table(db.photos_table_name)
    yield db
    db._clear_table(db.photos_table_name)


@pytest.fixture
def table_with_test_data(db):
    db._clear_table(db.photos_table_name)
    db.add_photos(TEST_IDS)
    yield db
    db._clear_table(db.photos_table_name)
