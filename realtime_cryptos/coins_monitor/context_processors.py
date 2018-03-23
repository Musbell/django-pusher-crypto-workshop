from django.conf import settings


def pusher_settings(request):
    return {
        'pusher': {
            'API_KEY': settings.PUSHER_API_KEY,
            'CLUSTER': settings.PUSHER_CLUSTER
        }
    }
