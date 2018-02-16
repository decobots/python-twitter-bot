import requests


def myrequest(method_type, url, **kwargs):
    return requests.request(method=method_type,
                            url=url,
                            params=kwargs.get("params", ""),
                            data=kwargs.get("data", ""),
                            auth=kwargs.get("auth", ""))
