from django.db import models
from django.conf import settings
from django.utils import timezone


class CoinMonitor(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=10)
    currency_name = models.CharField(max_length=255)
    icon_html = models.TextField(blank=True, default='')

    monitors = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class BuyOperation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete='CASCADE')
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return '{} ({}): ${}@${}'.format(
            self.user, self.symbol, self.amount, self.price)
