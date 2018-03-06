import logging
import time

from src.data_base import DataBase
from src.flickr import Flickr
from src.logger import init_logging
from src.twitter import Twitter

log = logging.getLogger()

if __name__ == "__main__":
    init_logging("log.log")
    will_be_uploaded_N_photos = 3

    with DataBase(photos_table_name="photos_list") as db:
        twitter = Twitter(database=db)
        flickr = Flickr(database=db)
        for _ in range(will_be_uploaded_N_photos):
            pictures = flickr.get_photos()
            photo = flickr.random_photo(pictures)
            photo = flickr.get_photo(photo)
            photo = twitter.upload_photo(photo)
            twitter.create_post(photo.title, photo)
            time.sleep(2)
