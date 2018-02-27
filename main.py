import time

from src.data_base import DataBase
from src.flickr import Flickr
from src.twitter import Twitter

if __name__ == "__main__":
    will_be_uploaded_N_photos = 3

    with DataBase() as db:
        twitter = Twitter(database=db)
        flickr = Flickr(database=db)
        pictures = flickr.get_photos()
        for _ in range(will_be_uploaded_N_photos):
            photo = flickr.random_photo(pictures)
            photo = flickr.get_photo(photo)
            photo = twitter.upload_photo(photo)
            twitter.create_post(photo.title, photo)
            time.sleep(2)
