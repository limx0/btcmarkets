
import os
import time
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
        ("apikey", api_key),
        ("timestamp", timestamp),
        ("signature", bsig),
    ])
