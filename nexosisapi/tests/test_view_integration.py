import os
import tempfile
import unittest
from datetime import datetime
import csv

from nexosisapi import Client, ClientError

class DatasetsIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"],
                                  uri=os.environ["NEXOSIS_API_TESTURI"])
        self.ds_name = "data-%s" % datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/data.csv')) as f:
            csv_data = csv.DictReader(f)
            self.data = [dict(d) for d in csv_data]

    def tearDown(self):
        try:
            self.test_client.datasets.remove(self.ds_name)
        except ClientError:
            pass

    def test_create_view(self):
        self.test_client.views.create('mike', self.ds_name, self.ds_name)
