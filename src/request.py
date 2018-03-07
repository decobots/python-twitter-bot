import json
import logging
from xml.etree import ElementTree
from src.logger import init_logging

import requests

log = logging.getLogger()


def request(method_type: str, url: str, **kwargs):
    log.debug(f"started request to url '{url}'")
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
    try:  # try if response xml, in other case consider that it is json or bytes
        result = ElementTree.fromstring(response.text)
        if result.attrib["stat"] == 'fail':
            log.exception(f'server returned fail status in xml')
            raise ValueError(response.text)
        log.debug(f'server returned xml')
    except ElementTree.ParseError:  # consider that content not xml
        try:  # try if response json, in other case consider that it is bytes
            response.json()
            log.debug(f'server returned json')
        except ValueError:  # consider that content not json
            response.content
            log.debug("server returned bytes data")

    return response


if __name__ == '__main__':
    init_logging("test_log.log")
    request(method_type="GET", url="https://farm4.staticflickr.com/3856/14848963128_9e4e83e446.jpg")
