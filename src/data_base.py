import logging
from typing import List
from urllib import parse

import psycopg2
from psycopg2 import sql

from src.environment_variables import get_env
from src.logger import init_logging

log = logging.getLogger()


class DataBase:
    def __init__(self, photos_table_name: str = None):
        self.photos_table_name = photos_table_name
        parse.uses_netloc.append("postgres")
        url = parse.urlparse(get_env("HEROKU_DATABASE_URL"))
        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.connection.cursor()
        log.debug("connection to database opened")
        self.create_table(self.photos_table_name)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        self.cursor.close()
        self.connection.close()
        log.debug("connection to database closed")

    def create_table(self, table_name: str):
        self.photos_table_name = table_name
        with self.connection as connection:
            connection.cursor().execute(sql.SQL('''CREATE TABLE IF NOT EXISTS {}
                                                    (id VARCHAR,
                                                    posted BOOL,
                                                    UNIQUE(id) )''').format(sql.Identifier(table_name)))
        log.debug(f"created (if not exist) table {table_name}")

    def add_photo(self, id_photo: str):
        with self.connection as connection:
            try:
                connection.cursor().execute(
                    sql.SQL("INSERT INTO {}(id, posted) VALUES(%s, 'FALSE')").format(
                        sql.Identifier(self.photos_table_name)),
                    (id_photo,))
                log.debug(f"photo with flickr id={id_photo} written to db")
            except psycopg2.IntegrityError:
                log.debug(f"photo with flickr id={id_photo} not written to db (already exists)")

    def post_photo(self, post_id: str):
        with self.connection as connection:
            connection.cursor().execute(
                sql.SQL("UPDATE {} SET posted = 'TRUE' WHERE id = %s").format(sql.Identifier(self.photos_table_name)),
                (post_id,))
            log.info(f"photo with flickr id={post_id} updated, marked as posted to twitter")

    def unposted_photos(self) -> List[str]:
        self.cursor.execute(
            sql.SQL("SELECT id FROM {} WHERE posted = 'FALSE'").format(sql.Identifier(self.photos_table_name)))
        result = [row[0] for row in self.cursor.fetchall()]
        log.debug(f"in database {len(result)} unposted photos")
        return result

    def delete_photo_from_twitter(self, post_id: str):
        with self.connection as connection:
            connection.cursor().execute(
                sql.SQL("UPDATE {} SET posted = 'FALSE' WHERE id = %s").format(
                    sql.Identifier(self.photos_table_name)),
                (post_id,))
            log.info(f"photo with flickr id={post_id} updated, marked as UNposted to twitter")

    def _print_db(self):
        self.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.photos_table_name)))
        for r in self.cursor.fetchall():
            print(r)

    def _print_db_posted(self):
        self.cursor.execute(
            sql.SQL("SELECT * FROM {} WHERE posted = 'TRUE'").format(sql.Identifier(self.photos_table_name)))
        for r in self.cursor.fetchall():
            print(r)


if __name__ == '__main__':
    init_logging("test_log.log")
    with DataBase() as dbe:
        print("hi")
        dbe._print_db()
        print("hi")
