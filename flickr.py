import collections
from xml.etree import ElementTree

from environment_variables import get_env
from request import request
from data_base import add_photo

endpoint = collections.namedtuple('endpoint', ["url", "method", "type"])


class Flickr:
    FLICKR_API_KEY = get_env("FLICKR_API_KEY")
    user_id = '76163487@N05'  # TODO get rid of it
    get_pictures = endpoint("https://api.flickr.com/services/rest", "flickr.people.getPublicPhotos", "POST")
    get_picture = endpoint("https://farm{}.staticflickr.com/{}/{}_{}.jpg", "", "GET")

    def __init__(self, requester=request):
        self.request = requester

    def get_photos(self):
        get_photos_response = self.request(method_type=self.get_pictures.type,
                                           url=self.get_pictures.url,
                                           payload={"method": self.get_pictures.method,
                                                    "api_key": self.FLICKR_API_KEY,
                                                    "user_id": self.user_id}
                                           )
        for tag in ElementTree.fromstring(get_photos_response.text)[0]:
            add_photo(attributes=tag.attrib)
        return [tag.attrib for tag in ElementTree.fromstring(get_photos_response.text)[0]]  # TODO remove return

    def get_photo(self, url, name):

        get_photo_response = self.request(method_type=self.get_picture.type,
                                          url=url)
        return get_photo_response.content, name
