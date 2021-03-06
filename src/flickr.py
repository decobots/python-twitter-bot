import collections
import logging
import random
from typing import Dict

from src.data_base import PhotoTable
from src.environment_variables import get_env
from src.photo import Photo
from src.requester import Requester

endpoint = collections.namedtuple('endpoint', ["url", "method", "type"])

log = logging.getLogger()


class Flickr:
    FLICKR_API_KEY = get_env("FLICKR_API_KEY")
    user_id = '76163487@N05'  # TODO get rid of it
    get_pictures = endpoint("https://api.flickr.com/services/rest", "flickr.people.getPublicPhotos", "POST")
    get_picture = endpoint("https://farm{}.staticflickr.com/{}/{}_{}.jpg", "", "GET")

    def __init__(self, table: PhotoTable, requester: Requester = Requester()):
        self.requester = requester
        self.table = table
        log.debug(
            f"class Flickr initialized with requester={requester.__class__} and table={table.table_name}")

    def get_photos(self) -> Dict[str, Photo]:
        log.info("stared function Flickr get_photos")
        photos = self.requester.request_xml(method_type=self.get_pictures.type,
                                            url=self.get_pictures.url,
                                            payload={"method": self.get_pictures.method,
                                                     "api_key": self.FLICKR_API_KEY,
                                                     "user_id": self.user_id}
                                            )
        result_photos = {}
        for tag in photos.iter('photo'):
            photo = Photo(id_flickr=tag.attrib["id"],
                          farm=tag.attrib["farm"],
                          server=tag.attrib["server"],
                          secret=tag.attrib["secret"],
                          title=tag.attrib["title"])
            result_photos[photo.id_flickr] = photo
        log.info(f"{len(result_photos)} photos received from flickr")
        self.table.add_photos(result_photos)
        return result_photos

    def get_photo(self, photo: Photo) -> Photo:
        log.info("started function Flickr get_photo")
        photo.data = self.requester.request_binary(method_type=self.get_picture.type,
                                                   url=self.get_picture.url.format(photo.farm,
                                                                                   photo.server,
                                                                                   photo.id_flickr,
                                                                                   photo.secret))

        log.info(f"received data for photo with flickr id = {photo.id_flickr}")
        return photo

    def random_photo(self, pictures: Dict) -> Photo:
        log.info("started function Flickr random_photo")
        result = pictures[random.choice(self.table.unposted_photos())]
        log.info(f"selected random photo {result.id_flickr}")
        return result
