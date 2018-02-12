import base64
import random
from xml.etree import ElementTree as etree
import json
from environment_variables import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_KEY, \
    TWITTER_ACCESS_SECRET, FLICKR_API_KEY
import requests
from requests_oauthlib import OAuth1
import time


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
    return {"source": flickr_binary_file.content, "name": photo_attributes["title"]}


def upload_picture_to_twitter(pic):
    endpoint = "https://upload.twitter.com/1.1/media/upload.json"
    auth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=ACCESS_KEY,
                  resource_owner_secret=ACCESS_SECRET, signature_type='body')
    params = {'name': pic["name"], 'media_data': base64.b64encode(pic["source"])}
    content = requests.post(endpoint, params, auth=auth)
    return {"id": json.loads(content.text)['media_id'], "name": pic["name"]}


def post_to_twitter(text_to_tweet, id_of_photo):
    auth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=ACCESS_KEY,
                  resource_owner_secret=ACCESS_SECRET, signature_type='body')
    endpoint = "https://api.twitter.com/1.1/statuses/update.json"
    params = {'status': text_to_tweet, 'media_ids': id_of_photo}
    c = requests.post(endpoint, params, auth=auth)
    print(c)


if __name__ == "__main__":
    will_be_uploaded_N_photos = 10
    while (will_be_uploaded_N_photos > 0):
        pictures_list = flickr_get_photos_list()
        random_index = random.choice(range(0, len(pictures_list)))
        photo_flickr = flickr_get_photo(pictures_list[random_index])
        photo_twitter = upload_picture_to_twitter(photo_flickr)
        post_to_twitter(photo_twitter["name"], photo_twitter["id"])
        time.sleep(30)
        will_be_uploaded_N_photos -= 1
