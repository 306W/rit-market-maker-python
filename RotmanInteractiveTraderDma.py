import json

import requests
from requests.auth import HTTPBasicAuth
from enum import Enum
import logging
import time


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


class RotmanInteractiveTraderDma:
    """
    Partial implementation of https://rit.306w.ca/RIT-REST-API-DEV/1.0.4/.
    """

    def __init__(self, api_trader_id: str, api_password: str, api_host='http://localhost:9999'):
        self.api_trader_id = api_trader_id
        self.api_password = api_password
        self.api_host = api_host
        self.api_version = 'v1'

    def make_request(self, method: str, endpoint: str, params=None, max_retries=99):
        for attempt in range(max_retries):
            req = requests.Request(
                method=method,
                url=f'{self.api_host}/{self.api_version}/{endpoint}',
                auth=HTTPBasicAuth(self.api_trader_id, self.api_password),
                headers={
                    'Accept': 'application/json'
                },
                params=params
            )
            p = req.prepare()
            s = requests.Session()
            logging.debug(f'{p.method} {p.url}')

            response = s.send(p)

            if response.status_code == 200:
                r = response.json()
                if not p.method == 'GET':
                    logging.debug(f'{p.method} {p.url} {json.dumps(r, indent=2)}')
                return r
            elif response.status_code == 429:
                retry_after = float(response.headers.get('Retry-After', 1))
                logging.warning(f"Rate limit exceeded. Retrying in {retry_after} seconds.")
                time.sleep(retry_after)
            else:
                response.raise_for_status()  # This will raise an HTTPError for non-200 status codes

        raise Exception(f"Max retries ({max_retries}) exceeded for {method} {endpoint}")

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
