import sqlite3


class DataBase:
    def __init__(self, file="test.db"):
        self.file = file
        self.db = sqlite3.connect(self.file)
        self.db.cursor()
        self.db.execute('''CREATE TABLE IF NOT EXISTS photos_list 
                        (id VARCHAR, 
                        posted BOOL, 
                        UNIQUE(id) )''')

    def __enter__(self):
        return self

    def __exit__(self):
        self.db.close()

    def add_photo(self, id_photo):
        self.db.execute("INSERT OR IGNORE INTO photos_list(id, posted) VALUES(?,0)", (id_photo,))
        self.db.commit()

    def unposted_photos(self):
        a = self.db.execute("SELECT id FROM photos_list WHERE posted = 0")
        return [row[0] for row in a]

    # def posted_photos(self):
    #     a = self.db.execute("SELECT id FROM photos_list WHERE posted = 1")
    #     return [row[0] for row in a]

    def post_photo(self, post_id):
        self.db.execute("UPDATE photos_list SET posted = 1 WHERE id = ?", (post_id,))
        self.db.commit()

    # def delete_photo(self, photo_id):
    #     self.db.execute("DELETE FROM photos_list WHERE id = ? ", (photo_id,))
    #     self.db.commit()

    def _print_db(self):
        a = self.db.execute("SELECT * FROM photos_list")
        for r in a:
            print(r)

    def _print_db_posted(self):
        a = self.db.execute("SELECT * FROM photos_list WHERE posted = 1")
        for r in a:
            print(r)


if __name__ == '__main__':
    dbe = DataBase()
    print(dbe.unposted_photos())
