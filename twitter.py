import base64
import collections
import json

from requests_oauthlib import OAuth1

from environment_variables import get_env
from request import request

endpoint = collections.namedtuple('endpoint', ["url", "type"])


class Twitter:
    twitter_upload_pic = endpoint("https://upload.twitter.com/1.1/media/upload.json", "POST")
    twitter_create_post = endpoint("https://api.twitter.com/1.1/statuses/update.json", "POST")
    twitter_get_users_posts = endpoint("https://api.twitter.com/1.1/statuses/user_timeline.json", "GET")
    twitter_delete_tweet_by_id = endpoint("https://api.twitter.com/1.1/statuses/destroy/{}.json", "POST")

    auth = OAuth1(get_env("TWITTER_CONSUMER_KEY"),
                  client_secret=get_env("TWITTER_CONSUMER_SECRET"),
                  resource_owner_key=get_env("TWITTER_ACCESS_KEY"),
                  resource_owner_secret=get_env("TWITTER_ACCESS_SECRET"))

    def __init__(self, database, requester=request):
        self.request = requester
        self.db = database

    def upload_photo(self, photo):
        data = base64.b64encode(photo.data)
        upload_photo_result = self.request(self.twitter_upload_pic.type,
                                           self.twitter_upload_pic.url,
                                           payload={"name": photo.title, "media_data": data},
                                           auth=self.auth)
        photo.id_twitter = json.loads(upload_photo_result.text)['media_id']
        return photo

    def create_post(self, status, photo=None):
        created_post = self.request(self.twitter_create_post.type,
                                    self.twitter_create_post.url,
                                    payload={"status": status, "media_ids": photo.id_twitter},
                                    auth=self.auth)
        self.db.post_photo(photo.id_flickr)

        return json.loads(created_post.content)["id"]

    def get_users_posts(self, amount):
        get_users_posts_request = self.request(self.twitter_get_users_posts.type,
                                               self.twitter_get_users_posts.url,
                                               payload={"count": amount},
                                               auth=self.auth)
        return [tweet["id"] for tweet in json.loads(get_users_posts_request.content)]

    def delete_tweet_by_id(self, tweet_id):
        self.request(self.twitter_delete_tweet_by_id.type,
                     self.twitter_delete_tweet_by_id.url.format(tweet_id),
                     auth=self.auth)


if __name__ == '__main__':
    t = Twitter()
    t.create_post(status="9")
