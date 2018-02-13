import unittest
from environment_variables import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_KEY, \
    TWITTER_ACCESS_SECRET, FLICKR_API_KEY
from main import flickr_get_photos_list, flickr_get_photo


class TestEnvironmentVariables(unittest.TestCase):
    def test_environment_variables_TWITTER_CONSUMER_KEY(self):
        self.assertIsInstance(TWITTER_CONSUMER_KEY, str)
        self.assertFalse(TWITTER_CONSUMER_KEY == '')

    def test_environment_variables_TWITTER_CONSUMER_SECRET(self):
        self.assertIsInstance(TWITTER_CONSUMER_SECRET, str)
        self.assertFalse(TWITTER_CONSUMER_SECRET == '')

    def test_environment_variables_TWITTER_ACCESS_KEY(self):
        self.assertIsInstance(TWITTER_ACCESS_KEY, str)
        self.assertFalse(TWITTER_ACCESS_KEY == '')

    def test_environment_variables_TTWITTER_ACCESS_SECRET(self):
        self.assertIsInstance(TWITTER_ACCESS_SECRET, str)
        self.assertFalse(TWITTER_ACCESS_SECRET == '')

    def test_environment_variables_FLICKR_API_KEY(self):
        self.assertIsInstance(FLICKR_API_KEY, str)
        self.assertFalse(FLICKR_API_KEY == '')


class TestFlickr(unittest.TestCase):
    def test_flickr_get_photos_list_correct(self):
        """
        check that returned value is list and attribute farm, server, id, secret exists for each list item
        """
        flickr_get_photos_list_result = flickr_get_photos_list()
        self.assertIsInstance(flickr_get_photos_list_result, list)
        for photo in flickr_get_photos_list_result:
            self.assertIsInstance(photo, dict)
            self.assertIsNotNone(photo["farm"])
            self.assertIsNotNone(photo["server"])
            self.assertIsNotNone(photo["id"])
            self.assertIsNotNone(photo["secret"])

    def test_flickr_get_photo_correct(self):
        """
        check that returned value are exist and have types bytes and string
        """
        test_flickr_get_photo_result_binary, test_flickr_get_photo_result_name = flickr_get_photo(
            {"farm": "5", "server": "4368", "id": "372637598620", "secret": "5bc41f375d", "title": "test"})
        self.assertIsNotNone(test_flickr_get_photo_result_binary)
        self.assertIsNotNone(test_flickr_get_photo_result_name)
        self.assertIsInstance(test_flickr_get_photo_result_binary, bytes)
        self.assertIsInstance(test_flickr_get_photo_result_name, str)

    def _test_flickr_get_photo_empty_input(self):
        self.assertRaises(flickr_get_photo())

    def _test_flickr_get_photo_with_incorrect_input_type(self):
        self.assertRaises(flickr_get_photo([]), ValueError)

    def _test_flickr_get_photo_incorrect_input(self):
        test_flickr_get_photo_result_binary2, test_flickr_get_photo_result_name2 = flickr_get_photo(
            {"farm": "7", "server": "7", "id": "7", "secret": "7", "title": "7"})
        self.assertIsNone(test_flickr_get_photo_result_binary2)
        self.assertIsNone(test_flickr_get_photo_result_name2)

