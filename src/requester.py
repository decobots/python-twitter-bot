import logging
from typing import Dict
from xml.etree import ElementTree

import requests

from src.logger import init_logging

log = logging.getLogger()


class Requester:
    @staticmethod
    def _request_basic(method_type: str, url: str, **kwargs) -> requests.Response:
        log.debug(f"started request to url '{url}'")
        params = kwargs.get("payload", None)
        data = kwargs.get("data", None)
        response = requests.request(method=method_type,
                                    url=url,
                                    params=params,
                                    data=data,
                                    auth=kwargs.get("auth", None))
        if response.status_code != 200:
            log.exception(f'response status code !=200 (response status code {response.status_code})')
            raise ValueError("response status code !=200 ", response.text)
        return response

    def request_json(self, method_type: str, url: str, **kwargs) -> Dict:
        response = self._request_basic(method_type, url, **kwargs)
        try:
            result = response.json()
            log.debug(f'server returned json')
        except:
            log.debug("server returned not json")
            raise ValueError("server returned not json")
        return result

    def request_xml(self, method_type: str, url: str, **kwargs) -> ElementTree:
        response = self._request_basic(method_type, url, **kwargs)
        try:
            result = ElementTree.fromstring(response.text)
        except:
            log.debug("server returned not xml")
            raise ValueError("server returned not xml")
        if result.attrib["stat"] == 'fail':
            log.exception(f'server returned fail status in xml')
            raise ValueError(f'server returned fail status in xml {response.text}')
        log.debug(f'server returned xml')
        return result

    def request_binary(self, method_type: str, url: str, **kwargs) -> bytes:
        response = self._request_basic(method_type, url, **kwargs)
        log.debug("server returned bytes data")
        return response.content

# if __name__ == '__main__':
# init_logging("test_log.log")
# r = Requester()
# r.request_xml(method_type="GET", url="https://farm4.staticflickr.com/3856/14848963128_9e4e83e446.jpg")
