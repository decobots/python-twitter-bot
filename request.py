import requests
from xml.etree import ElementTree


def request(method_type, url, **kwargs):
    result = requests.request(method=method_type,
                              url=url,
                              params=kwargs.get("params", None),
                              data=kwargs.get("data", None),
                              auth=kwargs.get("auth", None))
    try:
        response_tag = ElementTree.fromstring(result.content)
        if response_tag.attrib["stat"] == 'fail':
            raise ValueError(result.text)
    finally:
        if result.status_code != "200" and result.status_code != 200:
            raise ValueError(result.text)
    return result

