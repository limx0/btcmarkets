# btcmarkets
![build_status]

`btcmarkets` is a python wrapper for the BTCMarkets API. It has no dependencies and works with Python 2/3.

### Quick start:

#### Install
```bash
$ pip install btcmarkets
```

#### Examples
`btcmarkets.BTCMarkets` class contains the definitions and parameters for each of the API endpoints
```pydocstring
>>> from btcmarkets import BTCMarkets
>>> btcm_api = BTCMarkets()
>>> btcm_api.get_accounts()
[{'currency': 'AUD', 'balance': 100, 'pendingFunds': 0}, ...]

>>> btcm_api.get_trade_history(instrument='BTC', currency='AUD')
{'errorCode': None,
 'errorMessage': None,
 'success': True,
 'trades': [{'creationTime': 1498623229184,
   'description': None,
   'fee': 69963502,
   'id': 123456789,
   'orderId': 123456789,
   'price': 350000000000,
   'side': 'Bid',
   'volume': 1000000},
   ...
   ]
 }
```

Further documentation and examples can (somewhat) be found on the BTCMarkets API page - https://github.com/BTCMarkets/API


#### Auth endpoints (Accounts & Trading)
In order to be able to access POST endpoints (trading and accounts), the following environment variables need to be set
- `BTCMARKETS_API_KEY`
- `BTCMARKETS_SECRET`

API keys can be generated from https://btcmarkets.net/account/apikey


#### Advanced Usage

##### Using a different HTTP request library

By default `BTCMarkets` has no dependencies and will use python3s `urllib.request`.
You can replace this with any http library by passing the request function to the constructor eg.

```pydocstring
>>> import requests
>>> btcm_api = BTCMarkets(request_func=requests.request)
```

##### Even more control
Each of the `BTCMarkets` methods simply generate a dict to pass to a http request library.
For even finer grain control over your execution, setting `return_kwargs=True` will return the underlying request dict.

```pydocstring
>>> from btcmarkets import BTCMarkets
>>> btcm_api = BTCMarkets(return_kwargs=True)
>>> btcm_api.get_accounts()
{'method': 'GET',
 'url': 'https://api.btcmarkets.net/account/balance',
 'headers': OrderedDict([
              ('Accept', 'application/json'),
              ('Accept-Charset', 'UTF-8'),
              ('Content-Type', 'application/json'),
              ('apikey', 'MY_API_KEY'),
              ('timestamp', '1498699921678'),
              ('signature', '123456789123456789')
            ]),
 }
```

This could be handy if you want to use the new `async/await` features of Python with a library like `aiohttp`

```
>>> from aiohttp import ClientSession
>>> session = ClientSession()
>>> resp = await session.request(**api.get_accounts())
>>> data = await resp.json()
>>> data
[{'currency': 'AUD', 'balance': 100, 'pendingFunds': 0}, ...]
```

[build_status]: https://travis-ci.org/limx0/btcmarkets.svg?branch=master