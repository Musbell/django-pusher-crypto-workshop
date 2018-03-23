# http://aws.mannem.me/?p=1462
# https://www.okex.com/ws_api.html#spapi
import zlib
import json
import websocket
import threading
import time
from datetime import datetime


WSS_URL = 'wss://ws.pusherapp.com:443/app/de504dc5763aeef9ff52'


report = {
    'last': datetime.utcnow(),
    'total_secs': 0,
    'total_records': 0,
    'first_passed': False
}


def on_message(self, msg):
    print(msg)
    return
    data = json.loads(msg)
    if type(data) == list:
        record = data[0]
        if record.get('channel') == 'ok_sub_futureusd_btc_ticker_quarter':
            now = datetime.utcnow()
            diff = (now - report['last']).seconds
            avg = 'nan'
            if report['first_passed']:
                report['total_secs'] += diff
                report['total_records'] += 1
                avg = report['total_secs'] / report['total_records']
            else:
                report['first_passed'] = True
            report['last'] = now
            print("{:>3}s. - Avg: {:3}s. - {}".format(diff, avg, record['data']))
            return

    print("\t%s" % data)


def on_error(ws, error):
    print("ERROR %s" % error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send(json.dumps({
        'event': 'pusher:subscribe',
        'data': {
            'channel': 'live_tickers'
        }
    }))
    print("opened!!!")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        WSS_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
