import csv
import os
from datetime import datetime
import unittest

from nexosisapi import Client, ClientError


class SessionIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"], uri=os.environ["NEXOSIS_API_TESTURI"])
        self.ds_name = "data-%s" % datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        with open('data/data.csv') as f:
            csv_data = csv.DictReader(f)
            self.data = [dict(d) for d in csv_data]

    def tearDown(self):
        try:
            self.test_client.datasets.remove(self.ds_name)
        except ClientError:
            pass

    def test_list_sessions(self):
        pass

    def _setup_sessions(self):
        self.forecast = self.test_client.sessions.create_forecast(self.ds_name, 'observed',
                                                                  datetime.strptime('2008-09-01', '%Y-%m-%d'),
                                                                  datetime.strptime('2008-09-30', '%Y-%m-%d'))
        self.impact = self.test_client.sessions.analyze_impact(self.ds_name, 'observed', 'integration-test-analysis',
                                                               datetime.strptime('2008-08-01', '%Y-%m-%d'),
                                                               datetime.strptime('2008-08-31', '%Y-%m-%d'))
