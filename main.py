import random
import time

from flickr import Flickr
from twitter import Twitter

if __name__ == "__main__":
    will_be_uploaded_N_photos = 3
    twitter = Twitter()
    flickr = Flickr()
    while will_be_uploaded_N_photos > 0:
        pictures_list = flickr.get_photos()
        random_photo = random.choice(pictures_list)

        photo_flickr_binary, photo_flickr_name = flickr.get_photo(random_photo)

        photo_twitter_id, photo_twitter_name = twitter.upload_photo(data=photo_flickr_binary, name=photo_flickr_name)
        twitter.create_post(photo_twitter_name, photo_twitter_id)
        time.sleep(10)
        will_be_uploaded_N_photos -= 1
