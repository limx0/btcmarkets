
session = None


def urllib_request(method, url, headers, data):
    import json
    from urllib.request import urlopen, Request
    resp = urlopen(Request(method=method, url=url, headers=headers, data=data))
    return json.loads(resp.read().decode())


def requests_request(method, url, headers, data):
    from requests import Session
    global session
    if session is None:
        session = Session()
    resp = session.request(method, url=url, headers=headers, data=data)
    resp_json = resp.json()
    if 'success' in resp_json and not resp_json['success']:
        raise Exception('ErrorCode: %s Message: %s' % (resp_json['errorCode'], resp_json['errorMessage']))
    return resp_json


async def async_request(method, url, headers=None, data=None):
    from aiohttp import ClientSession
    global session
    if session is None:
        session = ClientSession()
    resp = await session.request(method, url=url, headers=headers, data=data)
    data = await resp.json()
    return data
