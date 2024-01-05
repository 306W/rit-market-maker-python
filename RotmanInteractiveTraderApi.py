import json

import requests
from enum import Enum
import logging


class OrderAction(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class OrderType(str, Enum):
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'


class OrderStatus(str, Enum):
    OPEN = 'OPEN'
    TRANSACTED = 'TRANSACTED'
    CANCELLED = 'CANCELLED'


class RotmanInteractiveTraderApi:
    """
    Partial implementation of https://rit.306w.ca/RIT-REST-API-DEV/1.0.3/.
    """

    def __init__(self, api_key: str, api_host='http://localhost:9999'):
        self.api_key = api_key
        self.api_host = api_host
        self.api_version = 'v1'

    def make_request(self, method: str, endpoint: str, params=None):
        req = requests.Request(
            method=method,
            url=f'{self.api_host}/{self.api_version}/{endpoint}',
            headers={
                'X-API-Key': self.api_key,
                'Accept': 'application/json'
            },
            params=params
        )
        p = req.prepare()
        s = requests.Session()
        logging.debug(f'{p.method} {p.url}')
        r = s.send(p).json()
        if not p.method == 'GET':
            logging.debug(f'{p.method} {p.url} {json.dumps(r, indent=2)}')
        return r

    def get_case(self):
        return self.make_request('get', 'case')

    def is_market_open(self):
        return self.get_case()['status'] == 'ACTIVE'

    def get_orders(self, status: OrderStatus = OrderStatus.OPEN):
        return self.make_request('get', 'orders', {
            'status': status.value
        })

    def get_time_and_sales(self, ticker):
        return self.make_request('get', 'securities/tas', {
            'ticker': ticker
        })

    def get_history(self, ticker):
        return self.make_request('get', 'securities/history', {
            'ticker': ticker
        })

    def get_trader(self):
        return self.make_request('get', 'trader')

    def get_limits(self):
        limits = {}
        for item in self.make_request('get', 'limits'):
            limits[item['name']] = item
        return limits

    def get_portfolio(self):
        portfolio = {}
        for item in self.make_request('get', 'securities'):
            portfolio[item['ticker']] = item
        return portfolio

    def get_order_book(self, ticker, limit=20):
        return self.make_request('get', 'securities/book', {
            'ticker': ticker,
            'limit': limit
        })

    def get_order_fills(self):
        partial = list(filter(lambda order: order['quantity_filled'] > 0, self.get_orders(OrderStatus.OPEN)))
        transacted = self.get_orders(OrderStatus.TRANSACTED)
        return partial + transacted

    def cancel_all_orders(self, ticker=None):
        return self.make_request('post', 'commands/cancel', {
            'ticker': ticker,
            'all': 1 if ticker is None else None
        })

    def place_order(self, ticker: str, order_type: OrderType, quantity: int, action: OrderAction, price=None, dry_run=None):
        if not self.is_market_open():
            raise Exception('Market is closed.')
        return self.make_request('post', 'orders', params={
            'ticker': ticker,
            'type': order_type.value,
            'quantity': quantity,
            'action': action.value,
            'price': price,
            'dry_run': 1 if dry_run else None
        })

    def cancel_orders(self, order_ids: list[int]):
        return self.make_request('post', f'commands/cancel', {
            'ids': ','.join(map(str, order_ids))
        })

    def get_assets(self):
        assets = {}
        for item in self.make_request('get', 'assets'):
            assets[item['ticker']] = item
        return assets

    def get_leases(self):
        return self.make_request('get', 'leases')

    def lease_asset(self, ticker: str):
        return self.make_request('post', 'leases', {
            'ticker': ticker
        })

    def unlease_asset(self, lease_id: int):
        return self.make_request('delete', f'leases/{lease_id}')

    def use_lease(self, lease_id: int, convert_from: dict[str, int]):
        params = {}
        i = 1
        for ticker in convert_from:
            params[f'from{i}'] = ticker
            params[f'quantity{i}'] = convert_from[ticker]
            i += 1
        return self.make_request('post', f'leases/{lease_id}', params)
