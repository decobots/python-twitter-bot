import json
from unittest import mock

import pytest

from src.requester import Requester


def test_request_basic_incorrect():
    r = Requester()
    with mock.patch(target="requests.request"):
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


def test_request_xml_returned_fail():
    r = Requester()
    r._request_basic = mock.MagicMock()
    r._request_basic.return_value.text = \
        '''<?xml version="1.0" encoding="utf-8" ?>
            <rsp stat="fail">
            <err code="98" msg="Invalid auth token" />
            </rsp>'''
    with pytest.raises(ValueError, match="server returned fail status in xml"):
        r.request_xml("GET", "URL")
