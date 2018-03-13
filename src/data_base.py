import logging
from typing import List, Dict
from urllib import parse

import psycopg2
from psycopg2 import extras, sql

from src.environment_variables import get_env
from src.logger import init_logging
from src.photo import Photo

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

    def execute(self, query: str, identifiers: list = None, arguments: tuple = None, arglist: List[tuple] = None,
                batch: bool = False):
        """
        :param batch: flag, True for queries that should be done in butch
        :param query: postgresSQL string with {} for SQL names and %s for values
        :param identifiers: SQL names (names of tables, columns)
        :param arguments: Values, that will be inserted into sql
        :param arglist: list of tuples with arguments for batch processing
        """
        s = sql.SQL(query).format(
            sql.SQL(', ').join(map(sql.Identifier, identifiers))
        )
        log.debug(f"created query {s.as_string(self.connection)}")
        with self.connection as connection:
            if not batch:
                connection.cursor().execute(query=s,
                                            vars=arguments)
            else:
                psycopg2.extras.execute_batch(cur=connection.cursor(),
                                              sql=s,
                                              argslist=arglist)

    def fetch(self) -> List:
        return [row for row in self.connection.cursor().fetchall()]

    def create_table(self, table_name: str):
        self.photos_table_name = table_name
        self.execute(
            query='CREATE TABLE IF NOT EXISTS {} (id VARCHAR, posted BOOL, tweet_id VARCHAR, UNIQUE(id) )',
            identifiers=[table_name]
        )
        log.debug(f"created (if not exist) table {table_name}")

    def _clear_table(self, table_name: str):
        self.execute(
            query="DELETE FROM {}",
            identifiers=[table_name]
        )

    def _delete_table(self, table_name: str):
        self.execute(
            query="DROP TABLE {}",
            identifiers=[table_name]
        )

    def add_photos(self, photos: Dict[str, Photo]):
        ids = [(photo,) for photo in photos]
        try:
            self.execute(
                query="INSERT INTO {}(id, posted) VALUES(%s, 'FALSE')",
                identifiers=[self.photos_table_name],
                arglist=ids,
                batch=True
            )
            log.debug(f"photos written to db")
        except psycopg2.IntegrityError:
            log.debug(f"photos NOT written to db (already exists)")

    def post_photo(self, photo_id: str, post_id: str):
        self.execute(
            query="UPDATE {} SET posted = 'TRUE', tweet_id=%s WHERE id = %s",
            identifiers=[self.photos_table_name],
            arguments=(post_id, photo_id)
        )
        log.info(f"photo with flickr id={post_id} updated, marked as posted to twitter")

    def unposted_photos(self) -> List[str]:
        self.execute(
            query="SELECT id FROM {} WHERE posted = 'FALSE'",
            identifiers=[self.photos_table_name]
        )
        result = [row[0] for row in self.cursor.fetchall()]
        log.debug(f"{len(result)} unposted photos in database")
        return result

    def delete_photo_from_twitter(self, post_id: str):
        with self.connection as connection:
            self.execute(
                query="UPDATE {} SET posted = 'FALSE', tweet_id=%s WHERE tweet_id = %s",
                identifiers=[self.photos_table_name],
                arguments=(None, post_id)
            )
            log.info(f"photos from post with twitter id={post_id} updated, marked as UNposted to twitter")

    def _print_db(self):
        self.execute(
            query="SELECT * FROM {}",
            identifiers=[self.photos_table_name]
        )
        for r in self.cursor.fetchall():
            print(r)

    def _print_db_posted(self):
        self.execute(
            query="SELECT * FROM {} WHERE posted = 'TRUE'",
            identifiers=[self.photos_table_name]
        )
        for r in self.cursor.fetchall():
            print(r)


if __name__ == '__main__':
    init_logging("test_log.log")
    with DataBase("test_twitter_table") as dbe:
        # dbe.add_photos("33")
        # dbe.post_photo("33","67")
        dbe._print_db()
    dbe.delete_photo_from_twitter("67")
    dbe._print_db()
