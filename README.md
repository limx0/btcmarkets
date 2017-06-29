# btcmarkets
Python wrapper for the BTCMarkets API

### Quick start:

##### Install
```bash
$ pip install btcmarkets
```

#### Account / Trading endpoints
In order to be able to access POST endpoints (trading and accounts), the following environment variables need to be set
- `BTCMARKETS_API_KEY`
- `BTCMARKETS_SECRET`

API keys can be generated from https://btcmarkets.net/account/apikey

##### Examples
`btcmarkets.BTCMarkets` class contains the definitions and parameters for each of the API endpoints. Pass the output of any of the functions to a http_request to retreive results.
```pydocstring
>>> from btcmarkets import BTCMarkets, request
>>> api = BTCMarkets()
>>> api.get_accounts()
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

>>> request(**api.get_accounts())
[{'currency': 'AUD', 'balance': 100, 'pendingFunds': 0}, ...]

>>> request(**api.get_trade_history(instrument='BTC', currency='AUD'))
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

Further documentation and examples can be found on the BTCMarkets API page - https://github.com/BTCMarkets/API

##### Using a different http library
. By default `btcmarkets.request` will use python3s `urllib.request`, to use another library:

```pydocstring
>>> from btcmarkets import BTCMarkets, request
>>> api = BTCMarkets()

# Use requests
>>> from requests import request
>>> request(**api.get_accounts())
<Response [200]>

# Use aiohttp
>>> from aiohttp import ClientSession
>>> session = ClientSession()
>>> resp = await session.request(**api.get_accounts())
>>> data = await resp.json()
>>> data
[{'currency': 'AUD', 'balance': 100, 'pendingFunds': 0}, ...]
```