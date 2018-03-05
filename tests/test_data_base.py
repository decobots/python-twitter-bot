import logging

import psycopg2
from psycopg2 import sql
from psycopg2 import extensions

from src.data_base import DataBase
from src.logger import init_logging, log_func_name_ended, log_func_name_started

log = logging.getLogger()
TABLE_NAME = "test_data_base"
TEST_IDS = "42", "43", "44"


def setup_module():
    init_logging("test_log.log")
    log.info("unit test DataBase started")


def teardown_module():
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
    empty_table.add_photo(TEST_IDS)
    empty_table.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    assert empty_table.cursor.fetchall() == [(p_id, False, None) for p_id in TEST_IDS]


def test_add_photo_duplicate(empty_table):
    empty_table.add_photo(TEST_IDS)# add photos
    empty_table.add_photo(TEST_IDS)# add duplicates
    empty_table.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    assert empty_table.cursor.fetchall() == [(p_id, False, None) for p_id in TEST_IDS]


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
