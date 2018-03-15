import logging
from typing import List, Dict, Tuple
from urllib import parse

import psycopg2
from psycopg2 import extras, sql

from src.environment_variables import get_env
from src.logger import init_logging
from src.photo import Photo

log = logging.getLogger()


class DataBase:
    def __init__(self):
        parse.uses_netloc.append("postgres")
        url = parse.urlparse(get_env("HEROKU_DATABASE_URL"))
        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        log.debug("connection to database opened")

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        self.connection.close()
        log.debug("connection to database closed")

    @staticmethod
    def _make_sql(query: str, identifiers: list = None):
        return sql.SQL(query).format(sql.SQL(', ').join(map(sql.Identifier, identifiers)))

    def execute(self, query: str, identifiers: list = None, arguments: tuple = None):
        """
        :param query: postgresSQL string with {} for SQL names and %s for values
        :param identifiers: SQL names (names of tables, columns)
        :param arguments: Values, that will be inserted into sql
        """
        s = self._make_sql(query=query, identifiers=identifiers)
        with self.connection as con:
            with con.cursor() as cursor:
                cursor.execute(query=s, vars=arguments)

    def execute_batch(self, query: str, identifiers: list = None, arglist: List[tuple] = None):
        """
        :param query: postgresSQL string with {} for SQL names and %s for values
        :param identifiers: SQL names (names of tables, columns)
        :param arglist: list of tuples with arguments for batch processing
        """
        s = self._make_sql(query=query, identifiers=identifiers)
        with self.connection as con:
            with con.cursor() as cursor:
                psycopg2.extras.execute_batch(
                    cur=cursor,
                    sql=s,
                    argslist=arglist
                )

    def select(self, query: str, identifiers: list = None, arguments: tuple = None) -> List[Tuple[str]]:
        """
        :param query: postgresSQL string with {} for SQL names and %s for values
        :param identifiers: SQL names (names of tables, columns)
        :param arguments: Values, that will be inserted into sql
        """
        s = self._make_sql(query=query, identifiers=identifiers)
        with self.connection as con:
            with con.cursor() as cursor:
                cursor.execute(
                    query=s,
                    vars=arguments
                )
                return [row for row in cursor.fetchall()]


class Table:
    def __init__(self, db, table_name: str):
        self.db = db
        self.table_name = table_name
        self.__create()

    def __create(self):
        self.db.execute(
            query='CREATE TABLE IF NOT EXISTS {} (id VARCHAR, posted BOOL, tweet_id VARCHAR, UNIQUE(id) )',
            identifiers=[self.table_name]
        )
        log.debug(f"created (if not exist) table {self.table_name}")

    def _clear(self):
        self.db.execute(
            query="DELETE FROM {}",
            identifiers=[self.table_name]
        )
        log.debug(f"cleared table {self.table_name}")

    def _delete(self):
        self.db.execute(
            query="DROP TABLE {}",
            identifiers=[self.table_name]
        )
        log.debug(f"deleted table {self.table_name}")

    # def __str__(self):
    #     result = self.db.select(
    #         query="SELECT * FROM {}",
    #         identifiers=[self.table_name]
    #     )
    #     return '\n'.join(result)


class PhotoTable(Table):
    def add_photos(self, photos: Dict[str, Photo]):
        ids = [(photo,) for photo in photos]
        try:
            self.db.execute_batch(
                query="INSERT INTO {}(id, posted) VALUES(%s, 'FALSE')",
                identifiers=[self.table_name],
                arglist=ids,
            )
            log.debug(f"photos written to table")
        except psycopg2.IntegrityError:
            log.debug(f"photos NOT written to table (already exists)")

    def post_photo(self, photo_id: str, post_id: str):
        self.db.execute(
            query="UPDATE {} SET posted = 'TRUE', tweet_id=%s WHERE id = %s",
            identifiers=[self.table_name],
            arguments=(post_id, photo_id)
        )
        log.info(f"photo with flickr id={post_id} updated, marked as posted to twitter")

    def unposted_photos(self) -> List[str]:
        result = self.db.select(
            query="SELECT id FROM {} WHERE posted = 'FALSE'",
            identifiers=[self.table_name]
        )
        log.debug(f"{len(result)} unposted photos in database")
        return [res[0] for res in result]

    def delete_photo_from_twitter(self, post_id: str):
        self.db.execute(
            query="UPDATE {} SET posted = 'FALSE', tweet_id=%s WHERE tweet_id = %s",
            identifiers=[self.table_name],
            arguments=(None, post_id)
        )

        log.info(f"photos from post with twitter id={post_id} updated, marked as UNposted to twitter")

    # def _print_db_posted(self):
    #     result = self.db.select(
    #         query="SELECT * FROM {} WHERE posted = 'TRUE'",
    #         identifiers=[self.table_name]
    #     )
    #     for r in result:
    #         print(r)


# if __name__ == '__main__':
#     init_logging("test_log.log")
    # with DataBase("test_twitter_table") as dbe:
    # dbe.add_photos("33")
    # dbe.post_photo("33","67")
    # dbe._print()
    # dbe.delete_photo_from_twitter("67")
    # dbe._print()
