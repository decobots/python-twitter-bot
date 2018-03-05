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
            log.debug(f"==================================================== started cycle {_}")
            pictures = flickr.get_photos()
            log.debug(f"==================================================== flickr.get_photos ended")
            photo = flickr.random_photo(pictures)
            log.debug(f"==================================================== flickr.random_photo ended")
            photo = flickr.get_photo(photo)
            log.debug(f"==================================================== flickr.get_photo ended")
            photo = twitter.upload_photo(photo)
            log.debug(f"==================================================== flickr.upload_photo ended")
            twitter.create_post(photo.title, photo)
            log.debug(f"==================================================== flickr.create_post ended")
            time.sleep(2)
