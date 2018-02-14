import os
import unittest

import environment_variables
from main import flickr_get_photos_list, flickr_get_photo


class TestEnvironmentVariables(unittest.TestCase):
    def test_environment_variables_correct(self):
        key = "TEST_VARIABLE"
        value = "TEST_VALUE"
        os.environ[key] = value
        self.assertEqual(environment_variables.get_env(key), value)
        os.environ.pop(key)

    def test_environment_variables_not_defined(self):
        self.assertRaises(OSError, environment_variables.get_env, "undefined_variable_name")


class TestFlickr(unittest.TestCase):
    def test_flickr_get_photos_list_correct(self):
        """
        check that returned value is list and attributes farm, server, id, secret exist for each list item
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
        check that returned value exist and have types bytes and string
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
