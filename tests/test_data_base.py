import psycopg2
import pytest
from psycopg2 import sql

from src.data_base import DataBase


@pytest.fixture
def table_name():
    return "test_data_base"


@pytest.fixture
def db(table_name):
    database = DataBase(table_name)
    yield database
    database.connection.close()


@pytest.fixture
def test_ids():
    return "42", "43", "44"


def test_db_context_manager(table_name):
    with DataBase(table_name) as db:
        assert db.table_name == table_name
        assert isinstance(db.connection, psycopg2.extensions.connection)
        assert isinstance(db.cursor, psycopg2.extensions.cursor)
        assert db.cursor.closed is False
        assert db.connection.closed == 0

    assert db.cursor.closed is True
    assert db.connection.closed == 1


def test_add_photo(db, table_name, test_ids):
    test_id = test_ids[0]
    db.add_photo(test_id)
    db.cursor.execute(sql.SQL("SELECT * FROM {} WHERE id = %s").format(sql.Identifier(table_name)), (test_id,))
    assert db.cursor.fetchall() == [(test_id, False)]

    db.add_photo(test_id)
    db.cursor.execute(sql.SQL("SELECT * FROM {} WHERE id = %s").format(sql.Identifier(table_name)), (test_id,))
    assert db.cursor.fetchall() == [(test_id, False)]  # duplicate id's handled correctly
    for t_id in test_ids:
        db.add_photo(t_id)
    db.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
    assert db.cursor.fetchall() == [(p_id, False) for p_id in test_ids]


def test_post_photo(db, table_name, test_ids):
    db.post_photo(test_ids[0])
    db.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
    list_ids = [(p_id, False) for p_id in test_ids]
    list_ids[0] = (test_ids[0], True)
    assert set(db.cursor.fetchall()) == set(list_ids)


def test_unposted_photos(db, test_ids):
    unposted = db.unposted_photos()
    assert unposted == list(test_ids[1:])


def test_unposted_photos_no_left(db, test_ids):
    for t_id in test_ids:
        db.post_photo(t_id)
    unposted = db.unposted_photos()
    assert unposted == []


def teardown_module():
    name = table_name()
    with DataBase(name) as db:
        s = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(name))
        db.cursor.execute(s)
        db.connection.commit()
