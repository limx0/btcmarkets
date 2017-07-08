
import sys
import json

if sys.version_info > (3, 0):
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError

    def urllib_request(method, url, headers, data):

        if isinstance(data, str):
            data = data.encode("utf-8")
        resp = urlopen(Request(method=method, url=url, headers=headers, data=data))
        return json.loads(resp.read().decode())

else:
    from urllib2 import urlopen, Request, HTTPError

    def urllib_request(method, url, headers, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        resp = urlopen(Request(url=url, headers=headers, data=data))
        return json.loads(resp.read().decode())
