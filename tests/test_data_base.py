import psycopg2
import pytest
from psycopg2 import sql

from src.data_base import DataBase

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


def test_db_context_manager():
    with DataBase(TABLE_NAME) as db:
        assert db.photos_table_name == TABLE_NAME
        assert isinstance(db.connection, psycopg2.extensions.connection)
        assert isinstance(db.cursor, psycopg2.extensions.cursor)
        assert not db.cursor.closed
        assert not db.connection.closed

    assert db.cursor.closed
    assert db.connection.closed


def test_add_photo(empty_table):
    for t_id in TEST_IDS:
        empty_table.add_photo(t_id)
    empty_table.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    assert empty_table.cursor.fetchall() == [(p_id, False) for p_id in TEST_IDS]


def test_add_photo_duplicate(empty_table):
    for t_id in TEST_IDS:  # add photos
        empty_table.add_photo(t_id)
    for t_id in TEST_IDS:  # add duplicates
        empty_table.add_photo(t_id)
    empty_table.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    assert empty_table.cursor.fetchall() == [(p_id, False) for p_id in TEST_IDS]


def test_post_photo(table_with_test_data):
    table_with_test_data.post_photo(TEST_IDS[0])
    table_with_test_data.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    list_ids = [(p_id, False) for p_id in TEST_IDS]
    list_ids[0] = (TEST_IDS[0], True)
    assert set(table_with_test_data.cursor.fetchall()) == set(list_ids)


def test_unposted_photos(table_with_test_data):
    table_with_test_data.post_photo(TEST_IDS[0])  # preparing test data
    unposted = table_with_test_data.unposted_photos()
    assert unposted == list(TEST_IDS[1:])


def test_unposted_photos_no_left(table_with_test_data):
    for t_id in TEST_IDS:  # preparing test data
        table_with_test_data.post_photo(t_id)
    unposted = table_with_test_data.unposted_photos()
    assert unposted == []
