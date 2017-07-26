import requests  # pip install requests
import json
import base64
import hashlib
import hmac
import os
import time  # for nonce


class Trading_v2():
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



class Trading_v1:


    def __init__(self, key, secret):
        self.base_url = "https://api.bitfinex.com"
        self.key = key
        self.secret = secret.encode()

    def _nonce(self):
        """
        Returns a nonce
        Used in authentication
        """
        return str(int(round(time.time() * 1e9)))

    def sign_payload(self, payload):
        payload_json = json.dumps(payload).encode()
        payload_base = base64.b64encode(payload_json)

        h = hmac.new(self.secret, payload_base, hashlib.sha384)
        signature = h.hexdigest()

        return {
            "X-BFX-APIKEY": self.key,
            "X-BFX-SIGNATURE": signature,
            "X-BFX-PAYLOAD": payload_base
        }

    def _post(self, path, params):
        body = params
        rawBody = json.dumps(body)
        headers = self.sign_payload(body)
        url = self.base_url + path
        resp = requests.post(url, headers=headers, data=rawBody, verify=True)

        if resp.status_code == 200:
            return resp.json()

        else:
            print('Status code: ', resp.status_code)
            print('Text: ', resp.text)
            print(resp.url)

    def account_info(self):
        payload = {
            'request': '/v1/account_infos',
            'nonce': self._nonce()
        }
        return self._post('/v1/account_infos', payload)

    def account_fees(self):
        payload = {
            'request': '/v1/account_fees',
            'nonce': self._nonce()
        }
        return self._post('/v1/account_fees', payload)

    def balances(self):
        payload = {
            'request': '/v1/balances',
            'nonce': self._nonce()
        }
        return self._post('/v1/balances', payload)

    def cancel_order(self, order_id):
        """
        Cancel an order

        Parameters
        ----------
        order_id: int
                Order number to be canceled.

        Returns
        -------
        response: response result of post request

        """

        payload = {
            'request': '/v1/order/cancel',
            'nonce': self._nonce(),
            'order_id': order_id
        }
        return self._post('/v1/order/cancel', payload)

    def deposit(self, method, wallet_name, renew=0):
        payload = {
            'request': '/v1/deposit/new',
            'nonce': self._nonce(),
            'method': method,
            'wallet_name': wallet_name,
            'renew': renew
        }
        return self._post('/v1/deposit/new', payload)

    def key_permissions(self):
        payload = {
            'request': '/v1/key_info',
            'nonce': self._nonce()
        }
        return self._post('/v1/key_info', payload)

    def new_order(self, symbol, amount, price, side, type_, exchange='bitfinex', use_all_available=False):
        """
        Sets up new order.

        Parameters
        ----------
        symbol: str
                Valid trading pair symbol
        amount: float
                Amount of currency to be traded
        price: float
                Price to trade currency at.
        side: str:
                Valid values: 'buy' or 'sell'
        type_: str
                Transaction type. Either “market” / “limit” / “stop” / “trailing-stop” / “fill-or-kill” /
                “exchange market” / “exchange limit” / “exchange stop” / “exchange trailing-stop” /
                “exchange fill-or-kill”. (
                type starting by “exchange ” are exchange orders, others are margin trading orders)

        exchange: str, default is 'bitfinex'
                    Exchange to trade one. Typically 'bitfinex'
        use_all_available: bool, default is False.
                            True will post an order using all the available balance.

        Returns
        -------
        response: response object

        """
        payload = {
            'request': '/v1/order/new',
            'nonce': self._nonce(),
            'symbol': symbol,
            'amount': str(amount),
            'price': str(price),
            'side': side,
            'type': type_,
            'exchange': exchange,
            'use_all_available': int(use_all_available),
            'ocoorder': False,
            'buy_price_oco': 0,
            'sell_price_oco': 0
        }
        return self._post('/v1/order/new', payload)

    def summary(self):
        payload = {
            'request': '/v1/summary',
            'nonce': self._nonce()
        }
        return self._post('/v1/summary', payload)
    

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


