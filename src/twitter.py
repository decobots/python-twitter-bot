import collections
import logging
from typing import Any, Optional, List

from requests_oauthlib import OAuth1

from src.data_base import PhotoTable
from src.environment_variables import get_env
from src.logger import init_logging
from src.photo import Photo
from src.requester import Requester
import psycopg2
endpoint = collections.namedtuple('endpoint', ["url", "type"])

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

    def __init__(self, table: PhotoTable, requester: Requester = Requester()):
        self.requester = requester
        self.table = table
        log.debug(
            f"class Twitter initialized with requester={requester.__class__} and table={self.table.table_name}")

    def upload_photo(self, photo: Photo) -> Photo:
        log.info("started function Twitter upload_photo")
        uploaded_photo = self.requester.request_json(self.twitter_upload_pic.type,
                                                     self.twitter_upload_pic.url,
                                                     data={"name": photo.title, "media_data": photo.data_b64},
                                                     auth=self.auth)
        photo.id_twitter = uploaded_photo['media_id']
        log.info(f"Photo with flickr id '{photo.id_flickr}' uploaded to twitter with id '{photo.id_twitter}'")
        return photo

    def create_post(self, status: Any = "_", photo: Optional[Photo] = None) -> str:
        log.info("started function Twitter create_post")
        media_ids = photo.id_twitter if photo else None
        created_post = self.requester.request_json(self.twitter_create_post.type,
                                                   self.twitter_create_post.url,
                                                   payload={"status": status, "media_ids": media_ids},
                                                   auth=self.auth)
        if photo != {} and media_ids:
            photo.id_posted_tweet = created_post["id"]  # TODO TEST IT!!!!
            self.table.post_photo(photo_id=photo.id_flickr, post_id=photo.id_posted_tweet)
        log.info(
            f"Post with text '{status}' and photos '{photo}' uploaded to twitter with id '{created_post['id']}'")
        return str(created_post['id'])

    def get_user_posts(self, amount: int) -> List[int]:
        user_posts = self.requester.request_json(self.twitter_get_users_posts.type,
                                                 self.twitter_get_users_posts.url,
                                                 payload={"count": amount},
                                                 auth=self.auth)
        result = [tweet["id"] for tweet in user_posts]
        log.debug(f"received {len(result)} user messages from twitter")
        return result

    def _delete_tweet_by_id(self, tweet_id: [str, int]):
        self.requester.request_json(self.twitter_delete_tweet_by_id.type,
                                    self.twitter_delete_tweet_by_id.url.format(tweet_id),
                                    auth=self.auth)
        try:
            self.table.delete_photo_from_twitter(post_id=tweet_id)
            log.debug(f"deleted twitter message with id '{tweet_id}', and photos marked as unposted")
        except psycopg2.ProgrammingError:
            log.debug(f"deleted twitter message with id '{tweet_id}', NO photos marked as unposted")

# if __name__ == '__main__':
#     init_logging("log.log")
# with DataBase("twitter") as table:
#     t = Twitter(table=table)
#     t.get_user_posts(1)
