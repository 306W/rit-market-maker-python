from RotmanInteractiveTraderApi import RotmanInteractiveTraderApi
import logging
import json
from time import sleep
from settings import settings


class BaseArbitrageBot:
    def __init__(self, exchange: RotmanInteractiveTraderApi):
        self.exchange = exchange
        self.is_market_open = False

    def round_to_quoted_decimals(self, price, quoted_decimals):
        """Round price to the appropriate number of decimals."""
        return round(price, quoted_decimals)

    def print_status(self):
        """Helper function to print out current status."""
        trader = self.exchange.get_trader()
        portfolio = self.exchange.get_portfolio()
        fills = self.exchange.get_order_fills()
        limits = self.exchange.get_limits()
        case = self.exchange.get_case()
        assets = self.exchange.get_assets()
        leases = self.exchange.get_leases()

        # print case info
        print(f"Case: {json.dumps(case, indent=2)}")
        # print trader info
        print(f"Trader: {json.dumps(trader, indent=2)}")
        # print portfolio info
        for ticker in portfolio:
            item = portfolio[ticker]
            quantity_traded = sum(map(lambda fill: fill['quantity_filled'], filter(lambda fill: fill['ticker'] == ticker, fills)))
            item['quantity_traded'] = quantity_traded
            print(f'Security [{ticker}]: {json.dumps(item, indent=2)}')
        # print limit info
        for name in limits:
            item = limits[name]
            print(f'Margin [{name}]: {json.dumps(item, indent=2)}')
        # print asset info
        for ticker in assets:
            item = assets[ticker]
            print(f'Asset [{ticker}]: {json.dumps(item, indent=2)}')
        # print lease info
        for lease in leases:
            print(f'Lease [{lease["id"]}]: {json.dumps(lease, indent=2)}')

    def on_status(self, is_market_open):
        """(Optional) To be implemented. Should contain any status / monitoring display that will run every loop."""
        pass

    def on_case_start(self):
        """(Optional) To be implemented. Runs once every time the case starts (and if the loop was started with the case already active)."""
        pass

    def on_loop(self):
        """To be implemented. Should contain the primary logic that will run every loop."""
        pass

    def run_loop(self):
        logging.info('Starting arbitrage loop')
        while True:
            sleep(settings['loop_interval'])
            is_market_open_now = self.exchange.is_market_open()
            self.on_status(is_market_open_now)
            if self.is_market_open != is_market_open_now:
                if is_market_open_now:
                    logging.info('Running case start events')
                    self.on_case_start()
                self.is_market_open = is_market_open_now
            if is_market_open_now:
                self.on_loop()
            else:
                logging.info('Exchange is closed')