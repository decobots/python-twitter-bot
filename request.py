from xml.etree import ElementTree

import requests


def request(method_type: str, url: str, **kwargs):
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
        raise ValueError("oops ", result.text)
    try:
        response_tag = ElementTree.fromstring(result.text)
        if response_tag.attrib["stat"] == 'fail':
            raise ValueError(result.text)
    except ElementTree.ParseError:
        pass
    return result
