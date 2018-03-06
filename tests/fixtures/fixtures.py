import os
from unittest import mock

import pytest
from psycopg2 import sql

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
def requester():
    req = mock.MagicMock()
    req.return_value = mock.MagicMock()
    req.__name__ = "mock_requester"
    return req


@pytest.fixture
def db():
    dbs = mock.MagicMock()
    dbs.photos_table_name = "mock_table"
    return dbs


TABLE_NAME = "test_data_base"
TEST_IDS = "42", "43", "44"


@pytest.fixture(scope="module")
def db():
    database = DataBase(TABLE_NAME)
    yield database
    database.close()


@pytest.fixture
def empty_table(db):
    yield db
    s = sql.SQL("DELETE FROM {}").format(sql.Identifier(TABLE_NAME))
    db.cursor.execute(s)
    db.connection.commit()


@pytest.fixture
def table_with_test_data(db):
    for t_id in TEST_IDS:  # add photos
        db.add_photo(t_id)
    yield db
    s = sql.SQL("DELETE FROM {}").format(sql.Identifier(TABLE_NAME))
    db.cursor.execute(s)
    db.connection.commit()
