
import os
import sys
import time
import json
import hmac
import base64
import hashlib
import collections


def build_headers(end_point, post_data=None):

    api_key = os.environ['BTCMARKETS_API_KEY'].encode("utf-8")
    secret = os.environ['BTCMARKETS_SECRET'].encode("utf-8")

    timestamp = str(int(time.time() * 1000))
    string_body = end_point + "\n" + timestamp + "\n"
    if post_data is not None:
        string_body += post_data
    rsig = hmac.new(base64.standard_b64decode(secret), string_body.encode("utf-8"), hashlib.sha512)
    bsig = base64.standard_b64encode(rsig.digest()).decode("utf-8")

    return collections.OrderedDict([
        ("Accept", "application/json"),
        ("Accept-Charset", "UTF-8"),
        ("Content-Type", "application/json"),
        ("apikey", api_key.decode("utf-8")),
        ("timestamp", timestamp),
        ("signature", bsig),
    ])


def urllib_request(method, url, headers, data):
    from urllib.request import urlopen, Request
    if isinstance(data, str):
        data = data.encode("utf-8")
    resp = urlopen(Request(method=method, url=url, headers=headers, data=data))
    return json.loads(resp.read().decode())


def urllib2_request(url, headers, data):
    from urllib2 import urlopen, Request
    if isinstance(data, str):
        data = data.encode("utf-8")
    resp = urlopen(Request(url=url, headers=headers, data=data))
    return json.loads(resp.read().decode())


if sys.version_info > (3, 0):
    DEFAULT_REQUESTER = urllib_request
else:
    DEFAULT_REQUESTER = urllib2_request
