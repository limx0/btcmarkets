import time

import pytest

from btcmarkets.api import BTCMarkets
from btcmarkets.compat import HTTPError
from btcmarkets.enums import OrderSide, OrderType
from btcmarkets.util import BTCMException


def test_pair_specific_funcs(api):
    instrument, currency = 'BTC', 'AUD'
    pair_funcs = [
        api.get_open_orders,
        api.get_order_history,
        api.get_trade_history,
        api.get_market_trades,
    ]

    for func in pair_funcs:
        result = func(instrument=instrument, currency=currency)
        assert isinstance(result, list)


def test_order_book(api):
    result = api.get_order_book('BTC', 'AUD')
    assert all(x in result for x in ('bids', 'asks',))


def test_get_accounts(api):
    accounts = api.get_accounts()
    assert isinstance(accounts, list)
    print(accounts)


def test_order_insert_delete(api):
    instrument, currency = 'BTC', 'AUD'
    price = 1
    volume = 0.001

    # Insert a super low bid
    resp_insert = api.insert_order(
        instrument=instrument, currency=currency, order_side=OrderSide.Buy, price=price,
        volume=volume, order_type=OrderType.LIMIT
    )
    assert (resp_insert['id'])

    # Check order exists and is correct
    time.sleep(0.5)
    resp_info = api.get_order_detail(order_ids=[resp_insert['id']])
    assert resp_info[0]['status'] in ('New', 'Placed')
    assert resp_info[0]['volume'] == volume
    assert resp_info[0]['price'] == price

    # Check delete
    resp_delete = api.delete_order(order_ids=[resp_insert['id']])
    assert resp_delete['responses'][0]['id']
    assert resp_delete['responses'][0]['success']
    time.sleep(0.5)
    assert not api.get_open_orders(instrument, currency)


def test_return_kwargs():
    api = BTCMarkets(return_kwargs=True)
    kwargs = api.get_accounts()
    assert kwargs['url'] == 'https://api.btcmarkets.net//account/balance'
    assert kwargs['method'] == 'GET'
    assert kwargs['headers']


def test_process_exception(api):
    with pytest.raises(HTTPError):
        api.delete_order('a')


def test_btcmarkets_exception(api):
    with pytest.raises(BTCMException):
        api.get_trade_history('BTC', 'AUD', limit=99999)


def test_order_insert_currency_precision(api):
    success_orders = [
        {"instrument": "BTC", "currency": "AUD", "price": 0.1, "volume": 1,
         "order_side": "Bid", "order_type": "Limit"},
        {"instrument": "ETH", "currency": "BTC", "price": 0.00000001, "volume": 1,
         "order_side": "Bid", "order_type": "Limit"},
        {"instrument": "BTC", "currency": "AUD", "price": 0.011, "volume": 1,
         "order_side": "Bid", "order_type": "Limit"},

    ]
    for order in success_orders:
        resp = api.insert_order(**order)
        assert resp['success']
        api.delete_order([resp['id']])
