# Generated by Django 2.0.3 on 2018-03-24 10:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coins_monitor', '0002_auto_20180323_2118'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('user', models.ForeignKey(on_delete='CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
