# btcmarkets
Python wrapper for the BTCMarkets API

#### Quick start:
```pydocstring
>>> from btcmarkets import BTCMarkets
>>> api = BTCMarkets()
 
>>> api.get_accounts()
[{'currency': 'AUD', 'balance': 100, 'pendingFunds': 0}, ...]
```

Further documentation and examples can be found on the BTCMarkets API page - https://github.com/BTCMarkets/API