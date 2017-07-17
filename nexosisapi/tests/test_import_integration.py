import csv
import time
import os
import dateutil.parser
import unittest

from nexosisapi import Client
from nexosisapi.column_metadata import ColumnMetadata
from nexosisapi.import_response import ImportType
from nexosisapi.status import Status


class ImportIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"], uri=os.environ["NEXOSIS_API_TESTURI"])

        metadata = {'sales': ColumnMetadata({'dataType': 'numeric', 'role': 'target'}),
                    'transactions': ColumnMetadata({'dataType': 'numeric', 'role': 'none'}),
                    'timeStamp': ColumnMetadata({'dataType': 'date', 'role': 'timestamp'})}

        self.import_response = self.test_client.imports.import_from_s3('test-python-import', 'nexosis-sample-data',
                                                                       'LocationA.csv', 'us-east-1', metadata)

    def tearDown(self):
        self.test_client.sessions.remove(self.import_response.import_id)

    def test_import_from_s3(self):
        self.assertIsNotNone(self.import_response)
        self.assertEqual(Status.requested, self.import_response.status)

    def test_get_import(self):
        import_ = self.test_client.imports.get(self.import_response.import_id)

        self.assertEqual(self.import_response.import_id, import_.import_id)

    def test_list_import(self):
        import_list = self.test_client.imports.list()

        self.assertGreater(len(import_list), 0)
