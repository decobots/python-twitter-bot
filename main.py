import random
import time

from flickr import Flickr
from twitter import Twitter
from data_base import return_random_unposted_photo

if __name__ == "__main__":
    will_be_uploaded_N_photos = 3
    twitter = Twitter()
    flickr = Flickr()
    while will_be_uploaded_N_photos > 0:
        pictures_list = flickr.get_photos()
        random_photo_url, random_photo_name = return_random_unposted_photo()
        photo_flickr_binary, photo_flickr_name = flickr.get_photo(random_photo_url, random_photo_name)

        photo_twitter_id, photo_twitter_name = twitter.upload_photo(data=photo_flickr_binary, name=photo_flickr_name)
        twitter.create_post(photo_twitter_name, photo_twitter_id)
        time.sleep(10)
        will_be_uploaded_N_photos -= 1
