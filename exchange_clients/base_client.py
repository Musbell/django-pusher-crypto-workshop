import pusher
import logging
from datetime import datetime

import config


def pusher_connect():
    return pusher.Pusher(
        app_id=config.PUSHER_APP_ID,
        key=config.PUSHER_API_KEY,
        secret=config.PUSHER_SECRET_KEY,
        cluster=config.PUSHER_CLUSTER,
        ssl=config.PUSHER_SSL
    )


class BaseClient(object):
    EXCHANGE_NAME = None

    def __init__(self, name=None):
        self.logger_name = name or '{}.{}'.format(
            self.__class__.__module__, self.__class__.__name__)
        self.logger = logging.getLogger(self.logger_name)

    def notify(self, currency, price):
        timestamp = datetime.utcnow()
        push = pusher_connect()
        channel = 'prices__{}'.format(currency.lower())
        push.trigger(channel, 'price', {
            'exchange': self.EXCHANGE_NAME,
            'price': price,
            'timestamp': timestamp.isoformat()
        })
