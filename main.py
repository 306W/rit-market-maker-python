import json
import logging
from RotmanInteractiveTraderApi import RotmanInteractiveTraderApi
from CustomArbitrageBot import CustomArbitrageBot
from Algo1CaseArbitrageBot import Algo1CaseArbitrageBot
from settings import settings

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    client = RotmanInteractiveTraderApi(api_key=settings['api_key'], api_host=settings['api_host'])
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
