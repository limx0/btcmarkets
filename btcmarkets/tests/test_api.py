
import pytest
import vcr
from btcmarkets.api import BTCMarkets

my_vcr = vcr.VCR(
    cassette_library_dir='resources/vcr_cassettes',
    record_mode='once',
    match_on=['uri', 'method', ],
    filter_headers=['Apikey', 'Signature'],
)


api = BTCMarkets()


@my_vcr.use_cassette
def test_get_accounts():
    accounts = api.get_accounts()
    assert isinstance(accounts, list)


@my_vcr.use_cassette
def test_get_open_orders():
    open_orders = api.get_open_orders('BTC', 'AUD')
    assert 'orders' in open_orders
    assert isinstance(open_orders['orders'], list)


@my_vcr.use_cassette
def test_process_exception():
    from urllib.error import HTTPError
    with pytest.raises(HTTPError):
        api.delete_order('a')
