
import json
import requests
from urllib.request import urljoin
from collections import OrderedDict

from btcmarkets.auth import build_headers


class BTCMarkets:

    base_url = 'https://api.btcmarkets.net'
    PRICE_MULTI = 100000000
    VOLUME_MULTI = 100000000

    def __init__(self):
        self.session = requests.Session()

    def get_accounts(self):
        return self.request('GET', end_point='/account/balance')

    def get_order_book(self, instrument, currency):
        return self.request('GET', end_point='/market/%s/%s/orderbook' % (instrument, currency))

    def get_trades(self, instrument, currency, since=0):
        return self.request('GET', end_point='/market/%s/%s/trades?since=%s' % (instrument, currency, since))

    def get_open_orders(self, instrument, currency, limit=100, since=0):
        data = OrderedDict([
            ('currency', currency), ('instrument', instrument), ('limit', limit), ('since', since),
        ])
        return self.request('POST', '/order/open', data=data)

    def get_order_history(self, instrument, currency, limit=100, since=0):
        data = OrderedDict([
            ('currency', currency), ('instrument', instrument), ('limit', limit), ('since', since)
        ])
        return self.request('POST', '/order/history', data=data)

    def get_trade_history(self, instrument, currency, limit=100, since=0):
        data = OrderedDict([
            ('currency', currency), ('instrument', instrument), ('limit', limit), ('since', since)
        ])
        return self.request('POST', '/order/trade/history', data=data)

    def get_order_detail(self, order_ids):
        data = OrderedDict([('orderIds', order_ids)])
        return self.request('POST', end_point='/order/detail', data=data)

    def insert_order(self, instrument, currency, order_side, price, volume, order_type):
        data = OrderedDict([
            ('currency', currency),
            ('instrument', instrument),
            ('price', int(price * self.PRICE_MULTI)),
            ('volume', int(volume * self.VOLUME_MULTI)),
            ('orderSide', order_side),
            ('ordertype', order_type),
            ('clientRequestId', '1')
        ])
        return self.request('POST', end_point='/order/create', data=data)

    def delete_order(self, order_ids: list):
        data = OrderedDict([('orderIds', order_ids)])
        return self.request('POST', end_point='/order/cancel', data=data)

    def request(self, method, end_point, data=None):
        url = urljoin(self.base_url, end_point)
        if data is not None:
            data = json.dumps(data, separators=(',', ':'))
        headers = build_headers(end_point, data)
        resp = self.session.request(method, url=url, headers=headers, data=data)
        resp_json = resp.json()
        if 'success' in resp_json and not resp_json['success']:
            raise Exception('ErrorCode: %s Message: %s' % (resp_json['errorCode'], resp_json['errorMessage']))
        return resp_json
