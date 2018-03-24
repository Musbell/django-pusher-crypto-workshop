from django.db import models
from django.conf import settings


class CoinMonitor(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=10)
    currency_name = models.CharField(max_length=255)
    icon_html = models.TextField(blank=True, default='')

    monitors = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name
