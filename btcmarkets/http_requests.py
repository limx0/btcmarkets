
import sys
if sys.version_info > (3, 0):
    from urllib.request import urljoin
else:
    from urlparse import urljoin

session = None


def urllib_request(method, url, headers, data):
    import json
    from urllib.request import urlopen, Request
    if isinstance(data, str):
        data = data.encode("utf-8")
    resp = urlopen(Request(method=method, url=url, headers=headers, data=data))
    return json.loads(resp.read().decode())
