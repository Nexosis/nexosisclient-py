import time
import os

import dateutil.parser
import unittest

from nexosisapi.column_metadata import ColumnMetadata

from nexosisapi import Client, ClientError
from nexosisapi.session import SessionType
from nexosisapi.status import Status
from nexosisapi.tests import build_test_dataset


class SessionIntegrationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.forecast = None
        cls.impact = None
        cls.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"], uri=os.environ["NEXOSIS_API_TESTURI"])
        cls.ds_name = 'data-sessions-integration'
        cls.regression_ds_name = 'data-regression-integration'

        cls.data = build_test_dataset(cls.test_client, 'data/data.csv', cls.ds_name)
        cls.regression_data = build_test_dataset(cls.test_client, 'data/regression-data.csv', cls.regression_ds_name)

        cls._setup_sessions()

    @classmethod
    def tearDownClass(cls):
        try:
            session_list = cls.test_client.sessions.list()

            for session in session_list:
                if session.dataset_name != cls.ds_name:
                    cls.test_client.sessions.remove(session.session_id)

            dataset_list = cls.test_client.datasets.list('test-session-integration')

            for dataset in dataset_list:
                cls.test_client.datasets.remove(dataset.name)

        except ClientError:
            pass

    def test_list_sessions(self):
        results = self.test_client.sessions.list(self.ds_name)

        name = set([s.dataset_name for s in results])

        self.assertEqual(1, len(name))

    def test_list_is_paged(self):
        actual = self.test_client.sessions.list(page_number=1,page_size=10)
        self.assertEqual(1, actual.page_number)
        self.assertEqual(10, actual.page_size)

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

        self.assertEqual(len(results.data), 30)

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

    def test_create_regression_model(self):
        columns = {
            'R.D.Spend': ColumnMetadata({'dataType': 'numeric', 'role': 'feature', 'imputation': 'mode', 'aggregation': 'median'}),
            'Administration': ColumnMetadata({'dataType': 'numeric', 'role': 'feature', 'imputation': 'mode', 'aggregation': 'median'}),
            'Marketing.Spend': ColumnMetadata({'dataType': 'numeric', 'role': 'feature', 'imputation': 'mode', 'aggregation': 'median'}),
            'Profit': ColumnMetadata({'dataType': 'numeric', 'role': 'target'}),
            'ny': ColumnMetadata({'dataType': 'logical', 'role': 'feature'}),
            'florida': ColumnMetadata({'dataType': 'logical', 'role': 'feature'}),
            'cali': ColumnMetadata({'dataType': 'logical', 'role': 'feature'}),
        }
        results = self.test_client.sessions.train_regression_model(self.regression_ds_name, 'profit', columns)

    @classmethod
    def _setup_sessions(cls):
        # check if we have a session data for forecast and impact, and if not, kick them off
        current_sessions = cls.test_client.sessions.list(cls.ds_name)
        for s in current_sessions:
            if s.type == SessionType.forecast:
                cls.forecast = s
            if s.type == SessionType.impact:
                cls.impact = s

        if cls.forecast is None:
            cls.forecast = cls.test_client.sessions.create_forecast(cls.ds_name, 'observed',
                                                                      dateutil.parser.parse('2008-09-01'),
                                                                      dateutil.parser.parse('2008-09-30'))
        if cls.impact is None:
            cls.impact = cls.test_client.sessions.analyze_impact(cls.ds_name, 'observed',
                                                                   'integration-test-analysis',
                                                                   dateutil.parser.parse('2008-08-01'),
                                                                   dateutil.parser.parse('2008-08-31'))

        counter = 0
        while cls.impact.status != Status.completed and cls.forecast.status != Status.completed:
            cls.impact = cls.test_client.sessions.get(cls.impact.session_id)
            cls.forecast = cls.test_client.sessions.get(cls.forecast.session_id)

            if counter > 120:
                raise TimeoutError('Running the sessions took longer than 10 minutes of setup time...')

            counter = counter + 1
            time.sleep(5)
