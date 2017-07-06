
import vcr
from btcmarkets.api import BTCMarkets

api = BTCMarkets()


def test_get_accounts():
    with vcr.use_cassette('resources/vcr_cassettes/get_accounts.yaml'):
        response = api.get_accounts()
        assert response