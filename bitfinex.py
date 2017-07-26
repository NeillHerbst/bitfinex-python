import requests  # pip install requests
import json
import base64
import hashlib
import hmac
import os
import time  # for nonce


class Trading():
    def __init__(self, key, secret):
        self.base_url = "https://api.bitfinex.com/"
        self.key = key
        self.secret = secret.encode()

    def _nonce(self):
        """
        Returns a nonce
        Used in authentication
        """
        return str(int(round(time.time() * 10000)))

    def _headers(self, path, nonce, body):
        signature = "/api/" + path + nonce + body
        h = hmac.new(self.secret, signature.encode(), hashlib.sha384)
        signature = h.hexdigest()
        return {
            "bfx-nonce": nonce,
            "bfx-apikey": self.key,
            "bfx-signature": signature,
            "content-type": "application/json"
        }

    def req(self, path, params={}):
        nonce = self._nonce()
        body = params
        rawBody = json.dumps(body)
        headers = self._headers(path, nonce, rawBody)
        url = self.base_url + path
        resp = requests.post(url, headers=headers, data=rawBody, verify=True)
        return resp

    def active_orders(self):
        """
        Fetch active orders
        """
        response = self.req("v2/auth/r/orders")
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            print(response)
            return ''


class Public:
    base_url = "https://api.bitfinex.com/"

    def _get(self, path, *args, **kwargs):
        return requests.get(self.base_url + path, kwargs)

    def ticker(self, symbol='tBTCUSD'):
        res = self._get('v2/ticker/{}'.format(symbol))
        return res.json()

    def trades(self, symbol='tBTCUSD'):
        res = self._get('v2/trades/{}/hist'.format(symbol))
        return res.json()

    def books(self, symbol, precision):
        res = self._get('v2/book/{0}/{1}'.format(symbol, precision))
        return res.json()

    def stats(self, key, size, symbol, side, section):
        res = self._get('v2/stats1/{0}:{1}:{2}:{3}/{4}'.format(key, size, symbol, side, section))
        return res.json()

    def candles(self, timeframe, symbol, section):
        res = self._get('v2/candles/trade:{0}:{1}/{2}'.format(timeframe, symbol, section))
        return res.json()


