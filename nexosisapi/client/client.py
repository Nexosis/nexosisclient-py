import os


from .datasets import Datasets
from .imports import Imports
from .models import Models
from .sessions import Sessions
from .views import Views
from .vocabularies import Vocabularies
from .http_client import HttpClient

from nexosisapi import NEXOSIS_API_KEY


class Client(object):
    """The main interface into the Nexosis API.
    """
    def __init__(self, key=None, uri='https://ml.nexosis.com/v1', client=None):
        self._key = key or os.environ.get(NEXOSIS_API_KEY)
        if uri.endswith('/'):
            uri = uri[:-1]
        self._uri = uri

        if client is None:
            client = HttpClient(self._key, uri)
        self._client = client
        self._models = Models(self._client)
        self._datasets = Datasets(self._client)
        self._imports = Imports(self._client)
        self._sessions = Sessions(self._client)
        self._views = Views(self._client)
        self._vocabularies = Vocabularies(self._client)

    @property
    def datasets(self):
        """Dataset based API operations"""
        return self._datasets

    @property
    def imports(self):
        """Import based API operations"""
        return self._imports

    @property
    def models(self):
        """Model based API operations"""
        return self._models

    @property
    def sessions(self):
        """Session based API operations"""
        return self._sessions

    @property
    def views(self):
        """View based API operations"""
        return self._views

    @property
    def vocabularies(self):
        """Vocabulary based API operations"""
        return self._vocabularies

    def get_account_balance(self):
        """Gets the current account balance"""
        response, status, headers = self._client.request_with_headers('GET', 'data')
        if status == 200:
            header = headers['nexosis-account-balance']
            if header is not None:
                value = header.split(' ')[0]
                return float(value)

        response.raise_for_status()
