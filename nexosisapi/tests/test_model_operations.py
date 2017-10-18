import unittest
from nexosisapi.tests.fake_http_client import FakeHttpClient
from nexosisapi import Client


class ModelOperationTests(unittest.TestCase):
    def setUp(self):
        self.http = FakeHttpClient({})
        self.client = Client(client=self.http)

    def test_remove_models_formats_arguments(self):
        self.client.models.remove_models(datasource_name='a-test-datasource')

        self.assertEqual(self.http.verb, 'DELETE')
        self.assertIsNotNone(self.http.uri, 'models')
        self.assertEqual(self.http.args['params']['dataSourceName'], 'a-test-datasource')

    def test_get_model_given_id(self):
        self.client.models.get_model('some-model-id')

        self.assertEqual(self.http.verb, 'GET')
        self.assertEqual(self.http.uri, 'models/some-model-id')

    def test_remove_model_given_id(self):
        self.client.models.remove('some-model-id')

        self.assertEqual(self.http.verb, 'DELETE')
        self.assertEqual(self.http.uri, 'models/some-model-id')

    def test_list_formats_arguments(self):
        self.client.models.list(page_number=0, page_size=10, datasource_name='some-datasource', created_before='2017-01-01', created_after='2017-10-10')

        self.assertEqual(self.http.verb, 'GET')
        self.assertEqual(self.http.uri, 'models')
        params = self.http.args['params']
        self.assertEqual(params['page'], 0)
        self.assertEqual(params['pageSize'], 10)
        self.assertEqual(params['dataSourceName'], 'some-datasource')
        self.assertEqual(params['createdBefore'], '2017-01-01')
        self.assertEqual(params['createdAfter'], '2017-10-10')
