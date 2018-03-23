import json
import pysher
import functools

import config
from base_client import BaseClient


class BitstampClient(BaseClient):
    EXCHANGE_NAME = 'Bitstamp'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pusher = pysher.Pusher(config.PUSHER_APP_KEY)

    def on_trade(self, currency, message):
        data = json.loads(message)
        self.notify(currency, data['price'])

    on_btc = functools.partialmethod(on_trade, 'BTC')
    on_ltc = functools.partialmethod(on_trade, 'LTC')
    on_eth = functools.partialmethod(on_trade, 'ETH')

    def connect_handler(self, data):
        btc_channel = self.pusher.subscribe('live_trades')
        btc_channel.bind('trade', self.on_btc)

        ltc_channel = self.pusher.subscribe('live_trades_ltcusd')
        ltc_channel.bind('trade', self.on_ltc)

        eth_channel = self.pusher.subscribe('live_trades_ethusd')
        eth_channel.bind('trade', self.on_eth)

    def run(self):
        self.pusher.connection.bind(
            'pusher:connection_established', self.connect_handler)
        self.pusher.connect()
        self.pusher.connection.join()


if __name__ == '__main__':
    import config as localconfig
    import logging.config
    logging.config.dictConfig(localconfig.LOGGING)
    b = BitstampClient()

    b.run()
