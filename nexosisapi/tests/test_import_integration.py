import os
import unittest
import time

from nexosisapi import Client, ClientError
from nexosisapi.column_metadata import ColumnMetadata
from nexosisapi.status import Status


class ImportIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"], uri=os.environ["NEXOSIS_API_TESTURI"])

        metadata = {'sales': ColumnMetadata({'dataType': 'numeric', 'role': 'target'}),
                    'transactions': ColumnMetadata({'dataType': 'numeric', 'role': 'none'}),
                    'timeStamp': ColumnMetadata({'dataType': 'date', 'role': 'timestamp'})}

        cls.import_response = cls.test_client.imports.import_from_s3('test-python-import', 'nexosis-sample-data',
                                                                       'LocationA.csv', 'us-east-1', metadata)
        #give import time to run
        time.sleep(10)


    @classmethod
    def tearDownClass(cls):
        try:
            cls.test_client.datasets.remove('test-python-import', cascade="session")
        except(ClientError):
            print('test-python-import was already deleted.')

    def test_import_from_s3(self):
        self.assertIsNotNone(self.import_response)
        self.assertEqual(Status.requested, self.import_response.status)

    def test_get_import(self):
        import_ = self.test_client.imports.get(self.import_response.import_id)

        self.assertEqual(self.import_response.import_id, import_.import_id)

    def test_list_import(self):
        import_list = self.test_client.imports.list()

        self.assertGreater(len(import_list), 0)

    def test_list_is_paged(self):
        actual = self.test_client.imports.list(page_number=1, page_size=10)
        self.assertEqual(1, actual.page_number)
        self.assertEqual(10, actual.page_size)
