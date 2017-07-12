import json
import os

import requests

from .sessions import Sessions
from .imports import Imports
from .datasets import Datasets
from .http_client import HttpClient

from nexosisapi import NEXOSIS_API_KEY


class Client(object):

    def __init__(self, key=os.environ[NEXOSIS_API_KEY], uri='https://ml.nexosis.com/v1'):
        self._key = key
        if uri.endswith('/'):
            uri = uri[:-1]
        self._uri = uri

        self._client = HttpClient()
        self._datasets = Datasets(self._client)
        self._imports = Imports(self._client)
        self._sessions = Sessions(self._client)

    @property
    def datasets(self):
        return self._datasets

    @property
    def imports(self):
        return self._imports

    @property
    def sessions(self):
        return self._sessions

    def get_account_balance(self):
        """get_account_balance"""
        balance_url = self._uri + "/data"
        response = self._client.get(balance_url)
        if response.status_code == 200:
            header = response.headers['nexosis-account-balance']
            if header is not None:
                value = header.split(' ')[0]
                return float(value)

        response.raise_for_status()

    def get_status(self, session_id):
        """get_status"""
        resp = self._client.head('%s/sessions/%s' % (self._uri, session_id), headers=self._generate_headers())
        return None, resp.status_code, resp.headers

    def get_results(self, session_id):
        """get_results"""
        resp = requests.get('%s/sessions/%s/results' % (self._uri, session_id), headers=self._generate_headers())
        return resp.json(), resp.status_code, resp.headers
