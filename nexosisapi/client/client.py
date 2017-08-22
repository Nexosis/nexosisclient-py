import json
import os

import requests

from .sessions import Sessions
from .imports import Imports
from .datasets import Datasets
from .views import Views
from .http_client import HttpClient

from nexosisapi import NEXOSIS_API_KEY


class Client(object):
    def __init__(self, key=None, uri='https://ml.nexosis.com/v1', client=None):
        self._key = key or os.environ[NEXOSIS_API_KEY]
        if uri.endswith('/'):
            uri = uri[:-1]
        self._uri = uri

        if client is None:
            client = HttpClient(key, uri)
        self._client = client
        self._datasets = Datasets(self._client)
        self._imports = Imports(self._client)
        self._sessions = Sessions(self._client)
        self._views = Views(self._client)

    @property
    def datasets(self):
        return self._datasets

    @property
    def imports(self):
        return self._imports

    @property
    def sessions(self):
        return self._sessions

    @property
    def views(self):
        return self._views

    def get_account_balance(self):
        """get_account_balance"""
        response, status, headers = self._client.request_with_headers('GET', 'data')
        if status == 200:
            header = headers['nexosis-account-balance']
            if header is not None:
                value = header.split(' ')[0]
                return float(value)

        response.raise_for_status()
