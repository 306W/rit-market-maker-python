import json
import logging
from RotmanInteractiveTraderApi import RotmanInteractiveTraderApi
from RotmanInteractiveTraderDma import RotmanInteractiveTraderDma
from Algo1CaseArbitrageBot import Algo1CaseArbitrageBot
from settings import settings

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    client = RotmanInteractiveTraderDma(api_trader_id=settings['dma_trader_id'], api_password=settings['dma_password'], api_host=settings['dma_host'])
    # verify connection
    trader = client.get_trader()
    logging.info(f'Connected as trader {json.dumps(trader, indent=2)}')
    # start event loop
    try:
        mm = Algo1CaseArbitrageBot(client)
        mm.run_loop()
    finally:
        logging.info('Cancelling open orders')
        client.cancel_all_orders()