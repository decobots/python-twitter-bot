import sqlite3
from functools import wraps as wraps
import random


def work_with_db(file):
    def dec(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            with sqlite3.connect(file) as dbd:
                dbd.cursor()
                dbd.execute('''CREATE TABLE IF NOT EXISTS photos_list 
                                (id INTEGER, 
                                url VARCHAR,
                                name VARCHAR,
                                posted BOOL, 
                                UNIQUE(id) )''')
                return func(dbd, *args, **kwargs)

        return decorator

    return dec


@work_with_db("test.db")
def add_photo(db, attributes):
    url = "https://farm{}.staticflickr.com/{}/{}_{}.jpg".format(attributes['farm'], attributes['server'],
                                                                attributes['id'], attributes['secret'])
    db.execute("INSERT OR IGNORE INTO photos_list(id, url,name, posted) VALUES(?,?,?,0)",
               (attributes['id'], url, attributes['title']))


@work_with_db("test.db")
def return_random_unposted_photo(db):
    a = db.execute("SELECT url, name FROM photos_list WHERE posted = 0")
    a_list = [row for row in a]
    return random.choice(a_list)[0], random.choice(a_list)[1],


@work_with_db("test.db")
def post_photo(db, post_id):
    a = db.execute("UPDATE photos_list SET posted = 1 WHERE id = ?", (post_id,))


@work_with_db("test.db")
def delete_photo(db):
    pass


@work_with_db("test.db")
def print_db(db):
    a = db.execute("SELECT * FROM photos_list")
    for r in a:
        print(r)


@work_with_db("test.db")
def print_db_posted(db):
    a = db.execute("SELECT * FROM photos_list WHERE posted = 1")
    for r in a:
        print(r)


if __name__ == '__main__':
    photo_id = return_random_unposted_photo()
    post_photo(post_id=photo_id)
    print_db_posted()
