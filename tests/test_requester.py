import json
from unittest import mock

import pytest
import requests

from src.requester import Requester


def test_request_basic_incorrect():
    r = Requester()
    requests.request = mock.MagicMock()
    requests.request.return_value.status_code = "x"
    with pytest.raises(ValueError):
        r._request_basic("GET", "URL")


def test_request_json_correct():
    r = Requester()
    r._request_basic = mock.MagicMock()
    r._request_basic.return_value.content = json.dumps({"id": 243145735212777472})
    r.request_json("GET", "URL")


def test_request_json_incorrect():
    r = Requester()
    r._request_basic = mock.MagicMock()
    r._request_basic.return_value.json = TypeError()
    with pytest.raises(ValueError):
        r.request_json("GET", "URL")


def test_request_xml_correct():
    r = Requester()
    r._request_basic = mock.MagicMock()
    r._request_basic.return_value.text = """<rsp stat="ok"><photos>
                                    <photo id="2636" secret="a123456" server="2" title="test_04" farm="5"/>
                                    </photos></rsp>"""
    r.request_xml("GET", "URL")


def test_request_xml_incorrect():
    r = Requester()
    r._request_basic = mock.MagicMock()
    r._request_basic.return_value.content = "incorrect input"
    with pytest.raises(ValueError):
        r.request_xml("GET", "URL")