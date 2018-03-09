import logging
from typing import Dict, List
from xml.etree import ElementTree

import requests

from src.logger import init_logging

log = logging.getLogger()


class Request:
    @staticmethod
    def _request_basic(method_type: str, url: str, **kwargs) -> requests.Response:
        log.debug(f"started requester to url '{url}'")
        params = None
        data = None
        if method_type == "GET":
            params = kwargs.get("payload", None)
        else:
            data = kwargs.get("payload", None)
        response = requests.request(method=method_type,
                                    url=url,
                                    params=params,
                                    data=data,
                                    auth=kwargs.get("auth", None))
        if response.status_code != 200:
            log.exception(f'response status code !=200 (response status code {response.status_code})')
            raise ValueError("response status code !=200 ", response.text)
        return response

    def request_json(self, method_type: str, url: str, **kwargs) ->Dict:
        response = self._request_basic(method_type, url, **kwargs)
        result = response.json()
        log.debug(f'server returned json')
        return result

    def request_xml(self, method_type: str, url: str, **kwargs) -> ElementTree:
        response = self._request_basic(method_type, url, **kwargs)
        result = ElementTree.fromstring(response.text)
        if result.attrib["stat"] == 'fail':
            log.exception(f'server returned fail status in xml')
            raise ValueError(response.text)
        log.debug(f'server returned xml')
        return result

    def request_binary(self, method_type: str, url: str, **kwargs) -> bytes:
        response = self._request_basic(method_type, url, **kwargs)
        log.debug("server returned bytes data")
        return response.content


if __name__ == '__main__':
    init_logging("test_log.log")
    r=Request()
    r.request_xml(method_type="GET", url="https://farm4.staticflickr.com/3856/14848963128_9e4e83e446.jpg")
