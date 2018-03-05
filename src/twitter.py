import collections
import json
from typing import Any, Optional, List

from requests_oauthlib import OAuth1

from src.data_base import DataBase
from src.environment_variables import get_env
from src.photo import Photo
from src.request import request

endpoint = collections.namedtuple('endpoint', ["url", "type"])

from src.logger import init_logging
import logging

log = logging.getLogger()


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
        log.debug(
            f"class Twitter initialized with requester={requester.__name__} and table={database.photos_table_name}")

    def upload_photo(self, photo: Photo) -> Photo:

        upload_photo_result = self.request(self.twitter_upload_pic.type,
                                           self.twitter_upload_pic.url,
                                           payload={"name": photo.title, "media_data": photo.data},
                                           auth=self.auth)
        photo.id_twitter = json.loads(upload_photo_result.text)['media_id']
        log.info(f"Photo with flickr id '{photo.id_flickr}' uploaded to twitter with id '{photo.id_twitter}'")
        return photo

    def create_post(self, status: Any = "_", photo: Optional[Photo] = None) -> str:
        media_ids = photo.id_twitter if photo else None
        created_post = self.request(self.twitter_create_post.type,
                                    self.twitter_create_post.url,
                                    payload={"status": status, "media_ids": media_ids},
                                    auth=self.auth)
        id_of_post = json.loads(created_post.content)["id"]
        if photo != {} and media_ids:
            self.db.post_photo(photo_id=photo.id_flickr, post_id=id_of_post)
        log.info(f"Post with text '{status}' and photos '{photo}' uploaded to twitter with id '{id_of_post}'")
        return id_of_post

    def get_user_posts(self, amount: int) -> List[str]:
        get_users_posts_request = self.request(self.twitter_get_users_posts.type,
                                               self.twitter_get_users_posts.url,
                                               payload={"count": amount},
                                               auth=self.auth)
        result = [tweet["id"] for tweet in json.loads(get_users_posts_request.content)]
        log.debug(f"received {len(result)} user messages from twitter")
        return result

    def _delete_tweet_by_id(self, tweet_id: str):
        self.request(self.twitter_delete_tweet_by_id.type,
                     self.twitter_delete_tweet_by_id.url.format(tweet_id),
                     auth=self.auth)
        try:
            self.db.delete_photo_from_twitter(post_id=tweet_id)
            log.debug(f"deleted twitter message with id '{tweet_id}', and photos marked as unposted")
        except:
            log.debug(f"deleted twitter message with id '{tweet_id}', NO photos marked as unposted")


if __name__ == '__main__':
    init_logging("log.log")
    with DataBase("twitter") as db:
        t = Twitter(database=db)
        t.get_user_posts(1)
