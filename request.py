import requests
from requests_oauthlib import OAuth1
from environment_variables import get_env
import collections


def myrequest(method_type, url, **kwargs):
    return requests.request(method=method_type,
                            url=url,
                            params=kwargs.get("params", ""),
                            data=kwargs.get("data", ""),
                            auth=kwargs.get("auth", ""))
