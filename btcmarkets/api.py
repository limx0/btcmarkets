
import json
from collections import OrderedDict
from btcmarkets.enums import Multipliers
from btcmarkets.compat import urllib_request
from btcmarkets.util import build_headers, BTCMException, maybe_list


class BTCMarkets:

    base_url = 'https://api.btcmarkets.net'

    def __init__(self, request_func=urllib_request, return_kwargs=False):
        self.request = request_func
        self.return_kwargs = return_kwargs

    def get_accounts(self):
        return self.process(method='GET', end_point='/account/balance', parse_output=True)

    def get_order_book(self, instrument, currency):
        return self.process(method='GET', end_point='/market/%s/%s/orderbook' % (instrument, currency))

    def get_market_trades(self, instrument, currency, since=0):
        return self.process(method='GET', end_point='/market/%s/%s/trades?since=%s' % (instrument, currency, since))

    def get_open_orders(self, instrument, currency, limit=100, since=0):
        data = OrderedDict([
            ('currency', currency), ('instrument', instrument), ('limit', limit), ('since', since),
        ])
        return self.process(method='POST', end_point='/order/open', data=data, result_key='orders', parse_output=True)

    def get_order_history(self, instrument, currency, limit=100, since=0):
        data = OrderedDict([
            ('currency', currency), ('instrument', instrument), ('limit', limit), ('since', since)
        ])
        return self.process(method='POST', end_point='/order/history', data=data, result_key='orders', parse_output=True)

    def get_trade_history(self, instrument, currency, limit=100, since=0):
        data = OrderedDict([
            ('currency', currency), ('instrument', instrument), ('limit', limit), ('since', since)
        ])
        end_point = '/order/trade/history'
        return self.process(method='POST', end_point=end_point, data=data, result_key='trades', parse_output=True)

    def get_order_detail(self, order_ids):
        data = OrderedDict([('orderIds', maybe_list(order_ids))])
        return self.process(method='POST', end_point='/order/detail', data=data, result_key='orders', parse_output=True)

    def insert_order(self, instrument, currency, order_side, price, volume, order_type):
        """
        :param instrument: {'BTC', 'ETH', 'LTC'}
        :param currency: {'BTC', 'AUD'}
        :param order_side: ('Bid', 'Ask')
        :param price: price for order.
        :param volume: volume for order.
        :param order_type: {'Limit', 'Market')
        :return:
        """
        price_precision = {'AUD': 2, 'BTC': 8}[currency]
        data = OrderedDict([
            ('currency', currency),
            ('instrument', instrument),
            ('price', round(price, price_precision)),
            ('volume', volume),
            ('orderSide', order_side),
            ('ordertype', order_type),
            ('clientRequestId', '1'),
        ])
        return self.process(method='POST', end_point='/order/create', data=data, parse_output=True)

    def delete_order(self, order_ids):
        """
        :param order_ids: list of order_ids
        :return:
        """
        data = OrderedDict([('orderIds', maybe_list(order_ids))])
        return self.process(method='POST', end_point='/order/cancel', data=data, parse_output=True)

    def parse_input_data(self, data):
        for upper in ('currency', 'instrument'):
            if upper in data:
                    data[upper] = data[upper].upper()
        if 'price' in data:
            data['price'] = int(data['price'] * Multipliers.PRICE)
        if 'volume' in data:
            data['volume'] = int(data['volume'] * Multipliers.VOLUME)
        return data

    @staticmethod
    def parse_output_data(data):
        for x in maybe_list(data):
            if isinstance(x, dict):
                if 'price' in x:
                    x['price'] = x['price'] / Multipliers.PRICE
                if 'volume' in x:
                    x['volume'] = x['volume'] / Multipliers.VOLUME
                if 'balance' in x:
                    x['balance'] = x['balance'] / Multipliers.VOLUME
        return data

    def build_request(self, method, end_point, data=None):
        url = '%s/%s' % (self.base_url, end_point)
        if data is not None:
            data = self.parse_input_data(data)
            data = json.dumps(data, separators=(',', ':'))
        headers = build_headers(end_point, data)
        return dict(method=method, url=url, headers=headers, data=data)

    def process(self, method, end_point, data=None, result_key=None, parse_output=True):
        kwargs = self.build_request(method, end_point, data)
        if self.return_kwargs:
            return kwargs
        resp = self.request(**kwargs)
        if isinstance(resp, dict) and resp.get('errorMessage') is not None:
            raise BTCMException('[%s] %s' % (resp['errorCode'], resp['errorMessage']))
        if result_key:
            resp = resp[result_key]
        if parse_output:
            resp = self.parse_output_data(resp)
        return resp
