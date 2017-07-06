
import pytest
from btcmarkets.api import BTCMarkets

api = BTCMarkets()


def test_pair_specific():
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


def test_order_book():
    result = api.get_order_book('BTC', 'AUD')
    assert all(x in result for x in ('bids', 'asks',))


def test_get_accounts():
    accounts = api.get_accounts()
    assert isinstance(accounts, list)


def test_process_exception():
    from urllib.error import HTTPError
    with pytest.raises(HTTPError):
        api.delete_order('a')
