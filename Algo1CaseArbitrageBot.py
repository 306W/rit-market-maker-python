from RotmanInteractiveTraderApi import OrderAction, OrderType
from BaseArbitrageBot import BaseArbitrageBot
import logging


class Algo1CaseArbitrageBot(BaseArbitrageBot):
    def on_loop(self):
        case = self.exchange.get_case()
        portfolio = self.exchange.get_portfolio()
        limits = self.exchange.get_limits()

        quantity = 1000
        if portfolio['CRZY_M']['bid'] > portfolio['CRZY_A']['ask']:
            logging.info(f"BUY CRZY_A / SELL CRZY_M, {quantity} @ {portfolio['CRZY_M']['bid'] - portfolio['CRZY_A']['ask']:.2f}")
            self.exchange.place_order('CRZY_A', OrderType.MARKET, quantity, OrderAction.BUY)
            self.exchange.place_order('CRZY_M', OrderType.MARKET, quantity, OrderAction.SELL)
        elif portfolio['CRZY_M']['ask'] < portfolio['CRZY_A']['bid']:
            logging.info(f"SELL CRZY_A / BUY CRZY_M, {quantity} @ {portfolio['CRZY_A']['bid'] - portfolio['CRZY_M']['ask']:.2f}")
            self.exchange.place_order('CRZY_A', OrderType.MARKET, quantity, OrderAction.SELL)
            self.exchange.place_order('CRZY_M', OrderType.MARKET, quantity, OrderAction.BUY)

    def on_case_start(self):
        # print out a bunch of information
        self.print_status()