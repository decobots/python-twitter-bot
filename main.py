import logging
import time

from src.data_base import DataBase, PhotoTable
from src.flickr import Flickr
from src.logger import init_logging
from src.twitter import Twitter

log = logging.getLogger()

if __name__ == "__main__":
    init_logging("log.log")
    will_be_uploaded_N_photos = 3

    with DataBase() as db:
        table = PhotoTable(db=db, table_name="main_photos")
        twitter = Twitter(table=table)
        flickr = Flickr(table=table)
        for _ in range(will_be_uploaded_N_photos):
            pictures = flickr.get_photos()
            photo = flickr.random_photo(pictures)
            photo = flickr.get_photo(photo)
            photo = twitter.upload_photo(photo)
            twitter.create_post(photo.title, photo)
            time.sleep(2)
