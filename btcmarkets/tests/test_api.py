
import pytest
from btcmarkets.api import BTCMarkets
from btcmarkets.enums import OrderSide, OrderType

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
    print(accounts)


def test_order_insert_delete():
    instrument, currency = 'BTC', 'AUD'
    resp = api.insert_order(
        instrument=instrument, currency=currency, order_side=OrderSide.Buy, price=1,
        volume=0.001, order_type=OrderType.LIMIT
    )
    x=1


def test_process_exception():
    from urllib.error import HTTPError
    with pytest.raises(HTTPError):
        api.delete_order('a')
