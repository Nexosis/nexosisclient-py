import unittest

import nexosisapi

from nexosisapi.tests.fake_http_client import FakeHttpClient


class DatasetMethodTests(unittest.TestCase):
    def test_list_all(self):
        fake_client = FakeHttpClient(None)
        client = nexosisapi.Client(client=fake_client)
        client.datasets.list()
        self.assertEqual(fake_client.verb, 'GET', 'Did not use GET verb.')
        self.assertEqual(fake_client.uri, '/data', 'Did not request right url.')
        self.assertEqual(fake_client.args['params'], {'partialName': ''})

    def test_list_with_query(self):
        fake_client = FakeHttpClient(None)
        client = nexosisapi.Client(client=fake_client)
        client.datasets.list('ds-partial-name')
        self.assertEqual(fake_client.verb, 'GET', 'Did not use GET verb.')
        self.assertEqual(fake_client.uri, '/data', 'Did not request right url')
        self.assertEqual(fake_client.args['params'], {'partialName': 'ds-partial-name'})
