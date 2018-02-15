import json
import base64
import requests
from requests_oauthlib import OAuth1

from environment_variables import get_env


class Twitter:
    method = {"twitter_upload_pic": "https://upload.twitter.com/1.1/media/upload.json",
              "twitter_create_post": "https://api.twitter.com/1.1/statuses/update.json",
              "twitter_get_users_posts": "https://api.twitter.com/1.1/statuses/user_timeline.json",
              "delete_tweet_by_id": "https://api.twitter.com/1.1/statuses/destroy/{}.json"}

    methodType = {"twitter_upload_pic": "post",
                  "twitter_create_post": "post",
                  "twitter_get_users_posts": "get",
                  "delete_tweet_by_id": "post"}

    auth = OAuth1(get_env("TWITTER_CONSUMER_KEY"),
                  client_secret=get_env("TWITTER_CONSUMER_SECRET"),
                  resource_owner_key=get_env("TWITTER_ACCESS_KEY"),
                  resource_owner_secret=get_env("TWITTER_ACCESS_SECRET"),signature_type="body")

    def request(self, method_name, **kwargs):
        params = {}
        result = None
        for key in kwargs:
            params[key] = kwargs[key]
        if self.methodType[method_name] == "post":
            if method_name == "delete_tweet_by_id":  # that method has different query structure than others
                result = requests.post(self.method[method_name].format(kwargs["tweet_id"]), data=params, auth=self.auth)
            else:
                result = requests.post(self.method[method_name], data=params, auth=self.auth)
        elif self.methodType[method_name] == "get":
            result = requests.get(self.method[method_name], params=params, auth=self.auth)
        return result

    def upload_photo(self, name, data):
        data = base64.b64encode(data)
        upload_photo_result = self.request("twitter_upload_pic", name=name, media_data=data)
        return json.loads(upload_photo_result.text)['media_id'], name

    def create_post(self, status, id_of_photo=[]):
        self.request("twitter_create_post", status=status, media_ids=id_of_photo)

    def get_users_posts(self, number_of_tweets_to_delete):
        get_users_posts_request = self.request("get_users_posts", count=number_of_tweets_to_delete)
        return [tweet["id"] for tweet in json.loads(get_users_posts_request.content)]

    def delete_tweet_by_id(self, tweet_id):
        self.request("delete_tweet_by_id", tweet_id=tweet_id)


if __name__ == '__main__':
    t = Twitter()
    t.create_post("hello")
