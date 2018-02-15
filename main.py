import random
import time
from xml.etree import ElementTree as etree

import requests

from environment_variables import FLICKR_API_KEY
from twitter import Twitter


def flickr_get_photos_list():
    payload = {'method': 'flickr.people.getPublicPhotos',
               'api_key': FLICKR_API_KEY,
               'user_id': '76163487@N05'
               }
    photos_list_response = requests.post('https://api.flickr.com/services/rest', data=payload)
    return [tag.attrib for tag in etree.fromstring(photos_list_response.text)[0]]


def flickr_get_photo(photo_attributes):
    flickr_binary_file = requests.get('https://farm{}.staticflickr.com/{}/{}_{}.jpg'.format(
        photo_attributes["farm"], photo_attributes["server"], photo_attributes['id'], photo_attributes["secret"]))
    return flickr_binary_file.content, photo_attributes["title"]


if __name__ == "__main__":
    will_be_uploaded_N_photos = 3
    twitter = Twitter()
    while will_be_uploaded_N_photos > 0:
        pictures_list = flickr_get_photos_list()
        random_photo = random.choice(pictures_list)
        photo_flickr_binary, photo_flickr_name = flickr_get_photo(random_photo)
        photo_twitter_id, photo_twitter_name = twitter.upload_photo(data=photo_flickr_binary, name=photo_flickr_name)
        twitter.create_post(photo_twitter_name, photo_twitter_id)
        time.sleep(10)
        will_be_uploaded_N_photos -= 1
