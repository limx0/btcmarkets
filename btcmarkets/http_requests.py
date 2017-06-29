
session = None


def urllib_request(method, url, headers, data):
    import json
    from urllib.request import urlopen, Request
    if isinstance(data, str):
        data = data.encode("utf-8")
    resp = urlopen(Request(method=method, url=url, headers=headers, data=data))
    return json.loads(resp.read().decode())


async def async_request(method, url, headers=None, data=None):
    from aiohttp import ClientSession
    global session
    if session is None:
        session = ClientSession()
    resp = await session.request(method, url=url, headers=headers, data=data)
    data = await resp.json()
    return data
