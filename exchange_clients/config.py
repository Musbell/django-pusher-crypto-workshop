LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

PUSHER_APP_ID = '496809'
PUSHER_API_KEY = '6f4dce495b70f4f53d86'
PUSHER_SECRET_KEY = '8af64dd8915fda14b02d'
PUSHER_CLUSTER = 'mt1'
PUSHER_SSL = True

PUSHER_APP_KEY = 'de504dc5763aeef9ff52'
