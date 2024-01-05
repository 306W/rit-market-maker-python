from BaseArbitrageBot import BaseArbitrageBot
import logging


class CustomArbitrageBot(BaseArbitrageBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_loop(self):
        pass

    def on_case_start(self):
        # print out a bunch of information
        self.print_status()
        # lease the converter assets so we have access to them
        logging.info('Running case start events')
        self.exchange.lease_asset('ETF-CREATE')
        self.exchange.lease_asset('ETF-REDEEM')

    def get_etf_create_lease(self):
        leases = [lease for lease in self.exchange.get_leases() if lease['ticker'] == 'ETF-CREATE']
        return leases[0] if leases else None

    def get_etf_redeem_lease(self):
        leases = [lease for lease in self.exchange.get_leases() if lease['ticker'] == 'ETF-REDEEM']
        return leases[0] if leases else None

    def use_etf_create(self, quantity):
        lease = self.get_etf_create_lease()
        if lease:
            if lease['convert_finish_tick']:
                logging.error("Currently converting, can't start another conversion")
                return
            convert_from = {
                'ETFTOKEN': 1
            }
            for ticker in self.etf_parts:
                convert_from[ticker] = quantity
            logging.info(f'Using ETF-CREATE for {quantity}')
            self.exchange.use_lease(lease['id'], convert_from)

    def use_etf_redeem(self, quantity):
        lease = self.get_etf_redeem_lease()
        if lease:
            if lease['convert_finish_tick']:
                logging.error("Currently converting, can't start another conversion")
                return
            convert_from = {
                'ETFTOKEN': 1,
                'ETF': quantity
            }
            logging.info(f'Using ETF-REDEEM for {quantity}')
            self.exchange.use_lease(lease['id'], convert_from)
