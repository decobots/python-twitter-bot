from contextlib import suppress
from typing import List
from urllib import parse

import psycopg2
from psycopg2 import sql

from src.environment_variables import get_env


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
        self.create_table(self.photos_table_name)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def create_table(self, table_name: str):
        self.photos_table_name = table_name
        with self.connection as connection:
            connection.cursor().execute(sql.SQL('''CREATE TABLE IF NOT EXISTS {}
                                                    (id VARCHAR,
                                                    posted BOOL,
                                                    UNIQUE(id) )''').format(sql.Identifier(table_name)))

    def add_photo(self, id_photo: str):
        with self.connection as connection:
            with suppress(psycopg2.IntegrityError):
                connection.cursor().execute(
                    sql.SQL("INSERT INTO {}(id, posted) VALUES(%s, 'FALSE')").format(sql.Identifier(self.photos_table_name)),
                    (id_photo,))

    def post_photo(self, post_id: str):
        with self.connection as connection:
            connection.cursor().execute(
                sql.SQL("UPDATE {} SET posted = 'TRUE' WHERE id = %s").format(sql.Identifier(self.photos_table_name)),
                (post_id,))

    def unposted_photos(self) -> List[str]:
        self.cursor.execute(sql.SQL("SELECT id FROM {} WHERE posted = 'FALSE'").format(sql.Identifier(self.photos_table_name)))
        return [row[0] for row in self.cursor.fetchall()]

    def _print_db(self):
        self.cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.photos_table_name)))
        for r in self.cursor.fetchall():
            print(r)

    def _print_db_posted(self):
        self.cursor.execute(sql.SQL("SELECT * FROM {} WHERE posted = 'TRUE'").format(sql.Identifier(self.photos_table_name)))
        for r in self.cursor.fetchall():
            print(r)


if __name__ == '__main__':
    with DataBase() as dbe:
        print("hi")
        dbe._print_db()
        print("hi")
