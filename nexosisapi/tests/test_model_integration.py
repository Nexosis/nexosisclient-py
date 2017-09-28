import os
import unittest

from nexosisapi import Client

class ImportIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"], uri=os.environ["NEXOSIS_API_TESTURI"])

    def tearDown(self):
        pass

    def test_list_models(self):
        pass
