from django.conf import settings


def pusher_settings(request):
    return {
        'pusher': {
            'APP_KEY': settings.PUSHER_APP_KEY,
            'CLUSTER': settings.PUSHER_CLUSTER
        }
    }
