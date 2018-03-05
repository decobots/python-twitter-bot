import collections
import logging
import random
from typing import Dict
from xml.etree import ElementTree

from src.data_base import DataBase
from src.environment_variables import get_env
from src.photo import Photo
from src.request import request

endpoint = collections.namedtuple('endpoint', ["url", "method", "type"])

log = logging.getLogger()


class Flickr:
    FLICKR_API_KEY = get_env("FLICKR_API_KEY")
    user_id = '76163487@N05'  # TODO get rid of it
    get_pictures = endpoint("https://api.flickr.com/services/rest", "flickr.people.getPublicPhotos", "POST")
    get_picture = endpoint("https://farm{}.staticflickr.com/{}/{}_{}.jpg", "", "GET")

    def __init__(self, database: DataBase, requester=request):
        self.request = requester
        self.db = database
        logging.info(self.__class__)
        log.debug(
            f"class Flickr initialized with requester={requester.__name__} and table={database.photos_table_name}")

    def get_photos(self) -> Dict[str, Photo]:
        response = self.request(method_type=self.get_pictures.type,
                                url=self.get_pictures.url,
                                payload={"method": self.get_pictures.method,
                                         "api_key": self.FLICKR_API_KEY,
                                         "user_id": self.user_id}
                                )
        result_photos = {}
        photos = ElementTree.fromstring(response.text)
        for tag in photos.iter('photo'):
            self.db.add_photo(id_photo=tag.attrib["id"])
            photo = Photo(id_flickr=tag.attrib["id"],
                          farm=tag.attrib["farm"],
                          server=tag.attrib["server"],
                          secret=tag.attrib["secret"],
                          title=tag.attrib["title"])
            result_photos[photo.id_flickr] = photo
        log.info(f"received {len(result_photos)} from flickr")
        return result_photos

    def get_photo(self, photo: Photo) -> Photo:
        response = self.request(method_type=self.get_picture.type,
                                url=self.get_picture.url.format(photo.farm,
                                                                photo.server,
                                                                photo.id_flickr,
                                                                photo.secret))
        photo.data = response.content
        log.info(f"received data for photo with flickr id = {photo.id_flickr}")
        return photo

    def random_photo(self, pictures: Dict) -> Photo:
        result = pictures[random.choice(self.db.unposted_photos())]
        log.info(f"selected random photo {result.id_flickr}")
        return result
