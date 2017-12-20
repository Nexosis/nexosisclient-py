import unittest
from nexosisapi.tests.fake_http_client import FakeHttpClient
from nexosisapi import Client


class ViewsIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.http = FakeHttpClient({
            'importId': '714753d3-d0fb-49f7-9746-436672828c47',
            'type': 's3',
            'status': 'requested',
            'dataSetName': 'test_ds',
            'requestedDate': '7/1/2012 12:00:00 AM +00:00',
            'statusHistory': {
                                "requested": "7/1/2012 12:00:00 AM +00:00"
                             },
            'links': {},
            'parameters': {},
            'messages': {}
        })
        self.client = Client(client=self.http)

    def test_secures3_adds_creds(self):
        self.client.imports.import_from_s3('test_ds',
                                                    'my_bucket',
                                                    'somefile.csv',
                                                    'us-east-1',
                                                    {"accesKeyId": "testid", "secretAccessKey": "testsecret"})
        self.assertEqual(self.http.args['data']['accesKeyId'], 'testid')
        self.assertEqual(self.http.args['data']['secretAccessKey'], 'testsecret')
        self.assertEqual(self.http.uri, '/imports/s3')

    def test_azure_adds_connection_info(self):
        self.client.imports.import_from_azure('test_ds', 'connstring', 'container', 'blob')
        self.assertEqual(self.http.uri, '/imports/azure')
        self.assertEqual(self.http.args['data']['connectionString'],'connstring')
        self.assertEqual(self.http.args['data']['container'], 'container')
        self.assertEqual(self.http.args['data']['blob'], 'blob')

    def test_azure_raises_error_if_params_missing(self):
        self.assertRaises(ValueError, self.client.imports.import_from_azure, 'ds-name', '', '', '')
        self.assertRaises(ValueError, self.client.imports.import_from_azure, 'ds-name', 'foo', None, 'bar')
        self.assertRaises(ValueError, self.client.imports.import_from_azure, '', 'foo', 'bar', 'fun')

    def test_url_raises_if_params_missing(self):
        self.assertRaises(ValueError, self.client.imports.import_from_url, 'ds-name', '')
        self.assertRaises(ValueError, self.client.imports.import_from_url, '', 'http://example.com')

    def test_url_passes_url(self):
        self.client.imports.import_from_url('test-ds','http://example.com/somefile.csv')
        self.assertEqual(self.http.uri,'/imports/url')
        self.assertEqual(self.http.args['data']['url'], 'http://example.com/somefile.csv')


    def test_url_includes_content_type(self):
        self.client.imports.import_from_url('test-ds','http://example.com/somefile.csv',content_type='json')
        self.assertEqual(self.http.args['data']['contentType'], 'json')

    def test_url_ignore_wrong_content_type(self):
        self.client.imports.import_from_url('test-ds', 'http://example.com/somefile.csv', content_type='foo')
        self.assertTrue('contentType' not in self.http.args['data'].keys())