import base64


class Photo:
    def __init__(self, id_flickr: str, farm: str, server: str, secret: str, title: str):
        self.id_flickr = id_flickr
        self.farm = farm
        self.server = server
        self.secret = secret
        self.title = title
        self.data = None
        self.id_twitter = None

    @property
    def data(self):
        return base64.b64encode(self.__data)

    @data.setter
    def data(self, data):
        self.__data = data
