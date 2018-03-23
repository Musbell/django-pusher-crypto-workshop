import json
import websocket
import logging.config

from base_client import BaseClient


class BitfinexClient(BaseClient):
    EXCHANGE_NAME = 'Bitfinex'

    DEFAULT_SYMBOLS = {
        'tBTCUSD': 'BTC',
        'tETHUSD': 'ETH',
        'tLTCUSD': 'LTC'
    }

    BASE_WS_URL = 'wss://api.bitfinex.com/ws/2'

    MESSAGE_HANDLERS = {
        dict: '_handle_dict_message',
        list: '_handle_list_message'
    }
    EVENT_HANDLERS = {
        'subscribed': '_handle_subscribed'
    }
    DEFAULT_MESSAGE_HANDLER = '_handle_other_message'

    def __init__(self, url=None, symbols=None):
        super().__init__()
        self.url = url or self.BASE_WS_URL
        self.symbols = symbols or self.DEFAULT_SYMBOLS
        self.channels = {}

    def _handle_subscribed(self, data):
        self.logger.debug('Subscribed %s', data)
        self.channels[data['chanId']] = data['symbol']

    def _handle_dict_message(self, data):
        if 'event' not in data:
            self.logger.error(
                "Unable to handle dict message without event: %s", data)
            return

        event = data['event']
        if event not in self.EVENT_HANDLERS:
            self.logger.warning(
                "No handler registered for event: %s", data)
            return

        event_handler = getattr(self, self.EVENT_HANDLERS[event])
        event_handler(data)

    def _handle_list_message(self, data):
        channel_id, values = data
        if type(values) != list:
            return
        last_price = values[-4]
        symbol = self.channels[channel_id]
        currency = self.symbols[symbol]

        # Pusher trigger
        self.notify(currency, last_price)

        # For debugging purposes
        self.logger.info("{}: ${}".format(currency, last_price))

    def _handle_other_message(self, data):
        self.logger.warning("Unhandled message type: {}".format(data))

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
            message_handler_name = self.MESSAGE_HANDLERS.get(
                type(data), self.DEFAULT_MESSAGE_HANDLER)
            message_handler = getattr(self, message_handler_name)
            message_handler(data)
        except json.JSONDecodeError:
            self.logger.warning("Couldn't parse message: {}".format(message))

    def _on_error(self, ws, error):
        self.logger.error("An error in WS Client: %s", error)

    def _on_close(self, ws):
        self.logger.info("## Connection Closed ##")

    def _subscribe(self, ws, symbol):
        data = {
          'event': "subscribe",
          'channel': "ticker",
          'symbol': symbol
        }
        ws.send(json.dumps(data))

    def _on_open(self, ws):
        for symbol in self.symbols:
            self._subscribe(ws, symbol)

    def run(self):
        ws = websocket.WebSocketApp(
            self.BASE_WS_URL,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close)
        ws.on_open = self._on_open
        ws.run_forever()


if __name__ == "__main__":
    import config as localconfig
    logging.config.dictConfig(localconfig.LOGGING)
    client = BitfinexClient()
    client.run()
