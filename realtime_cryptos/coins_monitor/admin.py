from django.contrib import admin

from .models import CoinMonitor, BuyOperation

admin.site.register(CoinMonitor)
admin.site.register(BuyOperation)
