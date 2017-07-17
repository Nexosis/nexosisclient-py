import csv
import time
import os
from datetime import datetime
import unittest

from nexosisapi import Client, ClientError
from nexosisapi.session import Status, SessionType


class SessionIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"], uri=os.environ["NEXOSIS_API_TESTURI"])
        self.ds_name = "data-sessions-integration"
        with open('data/data.csv') as f:
            csv_data = csv.DictReader(f)
            self.data = [dict(d) for d in csv_data]

        try:
            self.test_client.datasets.get(self.ds_name)
        except ClientError as e:
            if e.status == 404:
                self.test_client.datasets.create(self.ds_name, self.data)
            else:
                raise

        self._setup_sessions()

    def tearDown(self):
        try:
            self.test_client.datasets.remove(self.ds_name)
        except ClientError:
            pass

    def test_list_sessions(self):
        results = self.test_client.sessions.list(self.ds_name)

        name = set([s.dataset_name for s in results])

        self.assertEqual(1, len(name))

    def test_create_forecast(self):
        pass

    def test_estimate_forecast(self):
        pass

    def test_create_impact(self):
        pass

    def test_estimate_impact(self):
        pass

    def test_get_results(self):
        pass

    def test_remove_session(self):
        pass

    def test_remove_sessions(self):
        pass

    def test_create_session_no_data_error(self):
        pass

    def test_create_session_bad_dates(self):
        pass





    def _setup_sessions(self):
        # check if we have a session data for forecast and impact, and if not, kick them off
        current_sessions = self.test_client.sessions.list(self.ds_name)
        for s in current_sessions:
            if s.type == SessionType.forecast:
                self.forecast = s
            if s.type == SessionType.impact:
                self.impact = s

        if self.forecast is None:
            self.forecast = self.test_client.sessions.create_forecast(self.ds_name, 'observed',
                                                                      datetime.strptime('2008-09-01', '%Y-%m-%d'),
                                                                      datetime.strptime('2008-09-30', '%Y-%m-%d'))
        if self.impact is None:
            self.impact = self.test_client.sessions.analyze_impact(self.ds_name, 'observed',
                                                                   'integration-test-analysis',
                                                                   datetime.strptime('2008-08-01', '%Y-%m-%d'),
                                                                   datetime.strptime('2008-08-31', '%Y-%m-%d'))

        counter = 0
        while self.impact.status != Status.completed and self.forecast.status != Status.completed:
            self.impact = self.test_client.sessions.get(self.impact.session_id)
            self.forecast = self.test_client.sessions.get(self.forecast.session_id)

            if counter > 120:
                raise TimeoutError('Running the sessions took longer than 10 minutes of setup time...')

            counter = counter + 1
            time.sleep(5)
