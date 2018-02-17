import requests
from xml.etree import ElementTree


def request(method_type, url, **kwargs):
    result = requests.request(method=method_type,
                              url=url,
                              params=kwargs.get("params", None),
                              data=kwargs.get("data", None),
                              auth=kwargs.get("auth", None))
    if result.status_code != 200:
        raise ValueError(result.text)
    try:
        response_tag = ElementTree.fromstring(result.text)
        if response_tag.attrib["stat"] == 'fail':
            raise ValueError(result.text)
    except ElementTree.ParseError:
        pass
    return result
