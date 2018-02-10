import base64
import httplib2
import oauth2
import random
from xml.etree import ElementTree as etree
from urllib.parse import urlencode
import json
import pickle

with open("keys.txt", "rb") as file:
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET = pickle.load(file)


def flickr_query_to_get_list_of_pictures(request_h):
    """
    function to get list of photos
    :param request_h: http stream
    :return: list of bytestrings for each photo
    """
    payload = {'method': 'flickr.people.getPublicPhotos',
               'api_key': '1a19ecf3ddf46b3323bca01dc8afbd81',
               'user_id': '76163487@N05'
               }
    resp, content = request_h.request('https://api.flickr.com/services/rest/?&{}'.format(urlencode(payload)), "POST")
    xml = etree.fromstring(content.decode('utf-8'))
    xml = xml[0]  # get child of root (list of <photo> tags)
    photos = [{'id': tag.attrib['id'], 'secret': tag.attrib['secret'],
               "farm": tag.attrib["farm"], "server": tag.attrib["server"]} for tag in xml]
    return photos


def flickr_query2(request_h2, photo_index):
    """
    function to load photo from server
    :rtype: object
    """
    resp2, content2 = request_h2.request('https://farm{}.staticflickr.com/{}/{}_{}.jpg'.format(
        photo_index["farm"], photo_index["server"], photo_index['id'], photo_index["secret"]))
    return content2


def twitter_query(media_id):
    # return 1
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    access_token = oauth2.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    client = oauth2.Client(consumer, access_token)
    endpoint = "https://api.twitter.com/1.1/statuses/update.json"
    params = urlencode({'status': 'Hello from Python 2nd attempt',
                        'media_ids': media_id})
    r, c = client.request(endpoint, "POST", params)
    print(c)


def upload_picture_to_twitter(bin_pic):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    access_token = oauth2.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    client = oauth2.Client(consumer, access_token)
    endpoint = "https://upload.twitter.com/1.1/media/upload.json"
    b64_pic = base64.b64encode(bin_pic)
    params = urlencode({'name': 'picture',
                        'media_data': b64_pic})
    status, content = client.request(endpoint, "POST", params,
                                     urlencode({'Content-Type': 'multipart/form-data'}))
    return json.loads(content)['media_id']


if __name__ == "__main__":
    h = httplib2.Http(".cache")
    pictures_list = flickr_query_to_get_list_of_pictures(h)
    indexes = random.sample(range(0, len(pictures_list)), len(pictures_list))
    pic = flickr_query2(h, pictures_list[0])
    pic_id = upload_picture_to_twitter(pic)
    twitter_query(pic_id)
    '''for index in indexes:
        pic = flickr_query2(h, pictures_list[index])
        with open("pic{}.jpg".format(index), "wb") as file:
            file.write(pic)
    '''
