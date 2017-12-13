import pytest

from btcmarkets import BTCMarkets


@pytest.fixture(scope='module')
def api():
    return BTCMarkets()
