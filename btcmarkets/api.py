
import json
from collections import OrderedDict
from btcmarkets.util import build_headers, DEFAULT_REQUESTER


class BTCMarkets:

    base_url = 'https://api.btcmarkets.net'

    def __init__(self, request_func=DEFAULT_REQUESTER, return_kwargs=False):
        self.request = request_func
        self.return_kwargs = return_kwargs

    def get_accounts(self):
        return self.build_request(method='GET', end_point='/account/balance')

    def get_order_book(self, instrument, currency):
        return self.build_request(method='GET', end_point='/market/%s/%s/orderbook' % (instrument, currency))

    def get_trades(self, instrument, currency, since=0):
        return self.build_request(method='GET', end_point='/market/%s/%s/trades?since=%s' % (instrument, currency, since))

    def get_open_orders(self, instrument, currency, limit=100, since=0):
        data = OrderedDict([
            ('currency', currency), ('instrument', instrument), ('limit', limit), ('since', since),
        ])
        return self.build_request(method='POST', end_point='/order/open', data=data)

    def get_order_history(self, instrument, currency, limit=100, since=0):
        data = OrderedDict([
            ('currency', currency), ('instrument', instrument), ('limit', limit), ('since', since)
        ])
        return self.build_request(method='POST', end_point='/order/history', data=data)

    def get_trade_history(self, instrument, currency, limit=100, since=0):
        data = OrderedDict([
            ('currency', currency), ('instrument', instrument), ('limit', limit), ('since', since)
        ])
        return self.build_request(method='POST', end_point='/order/trade/history', data=data)

    def get_order_detail(self, order_ids):
        data = OrderedDict([('orderIds', order_ids)])
        return self.build_request(method='POST', end_point='/order/detail', data=data)

    def insert_order(self, instrument, currency, order_side, price, volume, order_type):
        """
        :param instrument: {'BTC', 'ETH', 'LTC'}
        :param currency: {'BTC', 'AUD'}
        :param order_side: ('Bid', 'Ask')
        :param price: price for order. Must be * 100,000,000 as per https://github.com/BTCMarkets/API/wiki/Trading-API
        :param volume: volume for order. Must be * 100,000,000 as per https://github.com/BTCMarkets/API/wiki/Trading-API
        :param order_type: {'Limit', 'Market')
        :return:
        """
        assert len(str(int(price))) > 5
        data = OrderedDict([
            ('currency', currency),
            ('instrument', instrument),
            ('price', price),
            ('volume', volume),
            ('orderSide', order_side),
            ('ordertype', order_type),
            ('clientRequestId', '1'),
        ])
        return self.build_request(method='POST', end_point='/order/create', data=data)

    def delete_order(self, order_ids):
        """
        :param order_ids: list of order_ids
        :return:
        """
        data = OrderedDict([('orderIds', order_ids)])
        return self.build_request(method='POST', end_point='/order/cancel', data=data)
    
    def build_request(self, method, end_point, data=None):
        url = '%s/%s' % (self.base_url, end_point)
        if data is not None:
            data = json.dumps(data, separators=(',', ':'))
        headers = build_headers(end_point, data)
        return dict(method=method, url=url, headers=headers, data=data)

    def process(self, method, end_point, data=None):
        kwargs = self.build_request(method, end_point, data)
        if self.return_kwargs:
            return kwargs
        response = self.request(**kwargs)
        if response['error']:
            print(kwargs)
            raise Exception(response['error'][0])
        return response['result']
