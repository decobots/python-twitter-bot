import logging
from xml.etree import ElementTree

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
    result = requests.request(method=method_type,
                              url=url,
                              params=params,
                              data=data,
                              auth=kwargs.get("auth", None))
    if result.status_code != 200:
        log.exception(f'response status code !=200 (response status code {result.status_code})')
        raise ValueError("response status code !=200 ", result.text)
    # TODO move parsing json and xml to request
    try:  # try pars as xml, in other case consider that it is json or bytes
        response_tag = ElementTree.fromstring(result.text)
        log.debug(f'trying to parse as xml')
        if response_tag.attrib["stat"] == 'fail':
            log.exception(f'server returned fail status in xml')
            raise ValueError(result.text)
        log.debug(f'parsed as xml')
    except ElementTree.ParseError:  # consider that content not xml
        if isinstance(result.content, bytes):
            log.debug("bytes data received")
        else:
            log.debug(f'json data received')
    return result
