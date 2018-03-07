import logging

import psycopg2
from psycopg2 import extensions, sql

from src.data_base import DataBase
from src.logger import init_logging, log_func_name_ended, log_func_name_started
from tests.fixtures.fixtures import TEST_IDS

log = logging.getLogger()

TABLE_NAME = "test_data_base"


def setup_module():
    init_logging("test_log.log")
    log.info("unit test DataBase started")


def teardown_module():
    db = DataBase(TABLE_NAME)
    db._delete_table(TABLE_NAME)
    log.info("unit test DataBase ended")


def setup_function(func):
    log_func_name_started(func)


def teardown_function(func):
    log_func_name_ended(func)


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
    empty_table.add_photos(TEST_IDS)
    empty_table.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    assert empty_table.cursor.fetchall() == [(p_id, False, None) for p_id in TEST_IDS]


def test_add_photo_duplicate(empty_table):
    empty_table.add_photos(TEST_IDS)  # add photos
    empty_table.add_photos(TEST_IDS)  # add duplicates
    empty_table.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    assert set(empty_table.cursor.fetchall()) == {(p_id, False, None) for p_id in TEST_IDS}


def test_post_photo(table_with_test_data):
    table_with_test_data.post_photo(TEST_IDS[0], "67")
    table_with_test_data.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    list_ids = [(p_id, False, None) for p_id in TEST_IDS]
    list_ids[0] = (TEST_IDS[0], True, "67")
    assert set(table_with_test_data.cursor.fetchall()) == set(list_ids)


def test_delete_photo_from_twitter(table_with_test_data):
    table_with_test_data.post_photo(TEST_IDS[0], "78")
    table_with_test_data.delete_photo_from_twitter("78")
    table_with_test_data.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    list_ids = [(p_id, False, None) for p_id in TEST_IDS]
    assert set(table_with_test_data.cursor.fetchall()) == set(list_ids)


def test_unposted_photos(table_with_test_data):
    table_with_test_data.post_photo(TEST_IDS[0], "89")  # preparing test data
    unposted = table_with_test_data.unposted_photos()
    assert unposted == list(TEST_IDS[1:])


def test_unposted_photos_no_left(table_with_test_data):
    for t_id in TEST_IDS:  # preparing test data
        table_with_test_data.post_photo(t_id, "99")
    unposted = table_with_test_data.unposted_photos()
    assert unposted == []


def test_delete_table():
    table_name = "test_delete_table"
    db = DataBase(table_name)
    db.cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
    all_tables = set(db.cursor.fetchall())
    assert (table_name,) in all_tables  # explicit check better than implicit
    db._delete_table(table_name)
    db.cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
    all_tables = set(db.cursor.fetchall())
    assert (table_name,) not in all_tables


def test_clear_table():
    table_name = "test_clear_table"
    db = DataBase(table_name)
    db.add_photos(TEST_IDS)
    db._clear_table(table_name)
    db.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
    all_rows = db.cursor.fetchall()
    assert [] == all_rows
    db._delete_table(table_name)
