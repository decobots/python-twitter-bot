import logging

import psycopg2
from psycopg2 import sql

from src.data_base import DataBase
from src.logger import init_logging
from tests.decorators import log_test_name

log = logging.getLogger()
TABLE_NAME = "test_data_base"
TEST_IDS = "42", "43", "44"


def setup_module():
    init_logging("test_log.log")
    log.info("unit test DataBase started")


def teardown_module():
    log.info("unit test DataBase ended")


@log_test_name
def test_db_context_manager():
    with DataBase(TABLE_NAME) as db:
        assert db.photos_table_name == TABLE_NAME
        assert isinstance(db.connection, psycopg2.extensions.connection)
        assert isinstance(db.cursor, psycopg2.extensions.cursor)
        assert not db.cursor.closed
        assert not db.connection.closed

    assert db.cursor.closed
    assert db.connection.closed

@log_test_name
def test_add_photo(empty_table):
    for t_id in TEST_IDS:
        empty_table.add_photo(t_id)
    empty_table.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    assert empty_table.cursor.fetchall() == [(p_id, False) for p_id in TEST_IDS]

@log_test_name
def test_add_photo_duplicate(empty_table):
    for t_id in TEST_IDS:  # add photos
        empty_table.add_photo(t_id)
    for t_id in TEST_IDS:  # add duplicates
        empty_table.add_photo(t_id)
    empty_table.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    assert empty_table.cursor.fetchall() == [(p_id, False) for p_id in TEST_IDS]

@log_test_name
def test_post_photo(table_with_test_data):
    log.debug(TEST_IDS[0])
    table_with_test_data.post_photo(TEST_IDS[0])
    table_with_test_data.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(TABLE_NAME)))
    list_ids = [(p_id, False) for p_id in TEST_IDS]
    list_ids[0] = (TEST_IDS[0], True)
    assert set(table_with_test_data.cursor.fetchall()) == set(list_ids)

@log_test_name
def test_unposted_photos(table_with_test_data):
    table_with_test_data.post_photo(TEST_IDS[0])  # preparing test data
    unposted = table_with_test_data.unposted_photos()
    assert unposted == list(TEST_IDS[1:])

@log_test_name
def test_unposted_photos_no_left(table_with_test_data):
    for t_id in TEST_IDS:  # preparing test data
        table_with_test_data.post_photo(t_id)
    unposted = table_with_test_data.unposted_photos()
    assert unposted == []
