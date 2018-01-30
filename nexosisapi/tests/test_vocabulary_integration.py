import os
import sys
import tempfile
import unittest
from datetime import datetime
import csv

from nexosisapi import Client, ClientError
from nexosisapi.vocabulary_summary import VocabularySummary



class VocabularyIntegationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"], uri=os.environ["NEXOSIS_API_TESTURI"])

    def test_list_vocabularies(self):
        vocabularies = self.test_client.vocabularies.list()

        self.assertGreaterEqual(len(vocabularies), 0)


