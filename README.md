# Real Time Crypto Dashboard
_(Django [Pusher](https://pusher.com) workshop by [RMOTR](https://rmotr.com))_

A simple real time app to showcase Pusher + Django integration with some Crypto exchanges.

### Install

_(This app has been developed with Python 3)_

```bash
$ mkvirtualenv -p $(which python3)
$ pip install -r requirements.txt
$ export DJANGO_SETTINGS_MODULE=realtime_cryptos.settings.dev
$ export PYTHONPATH=$(realpath realtime_cryptos)
$ django-admin migrate
```


### Usage

Basic usage for the Django app:
```bash
$ django-admin createsuperuser  # Enter your info
$ django-admin runserver  # App running in localhost:8000
```

You need to create at least 1 _"Coin Monitor group"_. Go to `http://localhost:8000/admin/coins_monitor/coinmonitor/`:

![image](https://user-images.githubusercontent.com/872296/37864792-10644080-2f52-11e8-876e-08ac5bcb4e2b.png)

### Exchange Clients

Once your app is working, you can start pulling data from exchanges. The two available clients are:

```bash
$ python exchange_clients/bitfinex_client.py
$ python exchange_clients/bitstamp_client.py
```
