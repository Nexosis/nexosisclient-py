import csv
import time
import os

import dateutil.parser
import unittest

from nexosisapi import Client, ClientError
from nexosisapi.session import SessionType
from nexosisapi.status import Status


class SessionIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.forecast = None
        self.impact = None
        self.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"], uri=os.environ["NEXOSIS_API_TESTURI"])
        self.ds_name = "data-sessions-integration"
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/data.csv')) as f:
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
            session_list = self.test_client.sessions.list()

            for session in session_list:
                if session.dataset_name != self.ds_name:
                    self.test_client.sessions.remove(session.session_id)

            dataset_list = self.test_client.datasets.list('test-session-integration')

            for dataset in dataset_list:
                self.test_client.datasets.remove(dataset.name)

        except ClientError:
            pass

    def test_list_sessions(self):
        results = self.test_client.sessions.list(self.ds_name)

        name = set([s.dataset_name for s in results])

        self.assertEqual(1, len(name))

    def test_create_forecast(self):
        self.test_client.datasets.create('test-session-integration-forecast', self.data)
        forecast = self.test_client.sessions.create_forecast('test-session-integration-forecast', 'observed',
                                                             dateutil.parser.parse('2008-09-01'),
                                                             dateutil.parser.parse('2008-09-30'))

        self.assertIsNotNone(forecast)
        self.assertEqual(SessionType.forecast, forecast.type)

    def test_estimate_forecast(self):
        self.test_client.datasets.create('test-session-integration-forecast', self.data)
        forecast = self.test_client.sessions.estimate_forecast('test-session-integration-forecast', 'observed',
                                                               dateutil.parser.parse('2008-07-01'),
                                                               dateutil.parser.parse('2008-07-31'))

        self.assertIsNotNone(forecast)
        self.assertTrue(forecast.is_estimate)
        self.assertEqual('0.01 USD', forecast.cost)

    def test_create_impact(self):
        self.test_client.datasets.create('test-session-integration-impact', self.data)
        impact = self.test_client.sessions.analyze_impact('test-session-integration-impact', 'observed',
                                                          'create-impact-test',
                                                          dateutil.parser.parse('2008-08-01'),
                                                          dateutil.parser.parse('2008-08-31'))

        self.assertIsNotNone(impact)

        self.assertEqual(SessionType.impact, impact.type)

    def test_estimate_impact(self):
        self.test_client.datasets.create('test-session-integration-impact', self.data)
        impact = self.test_client.sessions.estimate_impact('test-session-integration-impact', 'observed',
                                                           'create-impact-test',
                                                           dateutil.parser.parse('2008-06-01'),
                                                           dateutil.parser.parse('2008-06-30'))

        self.assertIsNotNone(impact)

        self.assertTrue(impact.is_estimate)
        self.assertEqual('0.01 USD', impact.cost)

    def test_get_results(self):
        results = self.test_client.sessions.get_results(self.forecast.session_id)

        self.assertEqual(len(results.data), 29)

    def test_remove_session(self):
        session = self.test_client.sessions.estimate_forecast(self.ds_name, 'observed',
                                                              dateutil.parser.parse('2008-10-01'),
                                                              dateutil.parser.parse('2008-10-31'))

        self.test_client.sessions.remove(session.session_id)

        try:
            self.test_client.sessions.get(session.session_id)
        except ClientError as e:
            self.assertEqual(404, e.status)
        else:
            self.assertFalse(True, 'Should have thrown a 404 error.')

    def test_create_session_no_data_error(self):
        try:
            self.test_client.sessions.create_forecast('does-not-exist', 'something',
                                                      dateutil.parser.parse('2008-11-01'),
                                                      dateutil.parser.parse('2008-11-30'))
        except ClientError as e:
            if e.status != 404:
                self.assertFalse(True, 'Should have thrown 404 error.')

    def test_create_session_bad_dates(self):
        try:
            self.test_client.sessions.create_forecast(self.ds_name, 'observed',
                                                      dateutil.parser.parse('2017-09-01'),
                                                      dateutil.parser.parse('2008-09-30'))
        except ClientError as e:
            if e.status != 400:
                self.assertFalse(True, 'Should have thrown 400 error.')

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
                                                                      dateutil.parser.parse('2008-09-01'),
                                                                      dateutil.parser.parse('2008-09-30'))
        if self.impact is None:
            self.impact = self.test_client.sessions.analyze_impact(self.ds_name, 'observed',
                                                                   'integration-test-analysis',
                                                                   dateutil.parser.parse('2008-08-01'),
                                                                   dateutil.parser.parse('2008-08-31'))

        counter = 0
        while self.impact.status != Status.completed and self.forecast.status != Status.completed:
            self.impact = self.test_client.sessions.get(self.impact.session_id)
            self.forecast = self.test_client.sessions.get(self.forecast.session_id)

            if counter > 120:
                raise TimeoutError('Running the sessions took longer than 10 minutes of setup time...')

            counter = counter + 1
            time.sleep(5)
