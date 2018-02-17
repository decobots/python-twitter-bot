import collections
from xml.etree import ElementTree

from environment_variables import get_env
from request import request

endpoint = collections.namedtuple('flickr_method', ["url", "method", "type"])


class Flickr:
    FLICKR_API_KEY = get_env("FLICKR_API_KEY")
    user_id = '76163487@N05'  # TODO get rid of it
    get_pictures = endpoint("https://api.flickr.com/services/rest", "flickr.people.getPublicPhotos", "POST")
    get_picture = endpoint("https://farm{}.staticflickr.com/{}/{}_{}.jpg", "", "GET")

    def get_photos(self):
        params = {"method": self.get_pictures.method, "api_key": self.FLICKR_API_KEY, "user_id": self.user_id}
        get_photos_response = request(method_type=self.get_pictures.type,
                                      url=self.get_pictures.url,
                                      params=params
                                      )
        return [tag.attrib for tag in ElementTree.fromstring(get_photos_response.text)[0]]

    def get_photo(self, photo_attributes):
        get_photo_response = request(method_type=self.get_picture.type,
                                     url=self.get_picture.url.format(photo_attributes["farm"],
                                                                     photo_attributes["server"],
                                                                     photo_attributes['id'],
                                                                     photo_attributes["secret"]))

        return get_photo_response.content, photo_attributes["title"]
