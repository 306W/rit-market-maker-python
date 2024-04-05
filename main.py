import json
import logging
from RotmanInteractiveTraderApi import RotmanInteractiveTraderApi
from settings import settings

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    client = RotmanInteractiveTraderApi(api_key=settings['api_key'], api_host=settings['api_host'])
    # verify connection
    trader = client.get_trader()
    logging.info(f'Connected as trader {json.dumps(trader, indent=2)}')
