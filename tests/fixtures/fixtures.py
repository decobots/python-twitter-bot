import os
from unittest import mock

import pytest

from src.data_base import DataBase, PhotoTable
from src.photo import Photo


@pytest.fixture(scope="session")
def global_variable():
    key = "TEST_VARIABLE"
    value = "TEST_VALUE"
    os.environ[key] = value
    yield key, value
    os.environ.pop(key)


@pytest.fixture(scope="session")
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
    req.__class__.return_value = "mock_requester"
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


@pytest.fixture(scope="session")
def db():
    database = DataBase()
    yield database
    database.close()


@pytest.fixture(scope="module")
def table(db, request):
    tb = PhotoTable(db=db, table_name=getattr(request.module, "TABLE_NAME", None))
    yield tb
    tb._delete()


@pytest.fixture
def empty_table(table):
    table._clear()
    yield table
    table._clear()


@pytest.fixture
def table_with_test_data(table, request):
    table._clear()
    table.add_photos(getattr(request.module, "TEST_IDS", None))
    yield table
    table._clear()
