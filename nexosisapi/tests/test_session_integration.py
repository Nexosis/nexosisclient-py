import time
import os

import dateutil.parser
import unittest

from nexosisapi.column_metadata import ColumnMetadata

from nexosisapi import Client, ClientError
from nexosisapi.confusion_matrix import ConfusionMatrix
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
        cls.classification_ds_name = 'data-classification-integration'

        cls.data = build_test_dataset(cls.test_client, 'data/data.csv', cls.ds_name)
        cls.regression_data = build_test_dataset(cls.test_client, 'data/regression-data.csv', cls.regression_ds_name)
        cls.classification_data = build_test_dataset(cls.test_client, 'data/iris_data.csv', cls.classification_ds_name)
        cls._setup_sessions()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.test_client.datasets.remove(cls.ds_name, cascade="session")
            cls.test_client.datasets.remove(cls.regression_ds_name, cascade="session")
            cls.test_client.datasets.remove(cls.classification_ds_name, cascade="session")
            dataset_list = cls.test_client.datasets.list('test-session-integration')

            for dataset in dataset_list:
                cls.test_client.datasets.remove(dataset.name, cascade="session")

        except ClientError:
            pass

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


    def test_create_impact(self):
        self.test_client.datasets.create('test-session-integration-impact', self.data)
        impact = self.test_client.sessions.analyze_impact('test-session-integration-impact', 'observed',
                                                          'create-impact-test',
                                                          dateutil.parser.parse('2008-08-01'),
                                                          dateutil.parser.parse('2008-08-31'))

        self.assertIsNotNone(impact)

        self.assertEqual(SessionType.impact, impact.type)


    def test_get_results(self):
        results = self.test_client.sessions.get_results(self.forecast.session_id)
        self.assertGreater(len(results.data), 0)

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
        results = self.test_client.sessions.train_model(self.regression_ds_name, 'profit', columns)

    def test_create_classification_model(self):
        result = self.test_client.sessions.train_model(self.classification_ds_name,'iris',prediction_domain='classification')
        self.assertEqual(result.prediction_domain.lower(),'classification')

    def test_get_confusion_matrix(self):
        actual = self.test_client.sessions.get_confusion_matrix(self.classification.session_id)
        self.assertIsNotNone(actual)
        self.assertIsInstance(actual, ConfusionMatrix)
        self.assertGreater(len(actual.values), 0)

    @classmethod
    def _setup_sessions(cls):
        # check if we have a session data for forecast and impact, and if not, kick them off
        current_sessions = cls.test_client.sessions.list('', page_size=100)

        cls.forecast = next((s for s in current_sessions if s.type == SessionType.forecast and s.status == Status.completed), None)
        cls.impact = next((s for s in current_sessions if s.type == SessionType.impact and s.status == Status.completed), None)
        cls.classification = next((s for s in current_sessions if s.type == SessionType.model and s.prediction_domain.lower() == 'classification' and s.status == Status.completed), None)

        if cls.forecast is None:
            cls.forecast = cls.test_client.sessions.create_forecast(cls.ds_name, 'observed',
                                                                      dateutil.parser.parse('2008-09-01'),
                                                                      dateutil.parser.parse('2008-09-30'))
        if cls.impact is None:
            cls.impact = cls.test_client.sessions.analyze_impact(cls.ds_name, 'observed',
                                                                   'integration-test-analysis',
                                                                   dateutil.parser.parse('2008-08-01'),
                                                                   dateutil.parser.parse('2008-08-31'))

        if cls.classification is None:
            cls.classification = cls.test_client.sessions.train_model(cls.classification_ds_name, 'iris', prediction_domain='classification')

        counter = 0
        while cls.impact.status != Status.completed or cls.forecast.status != Status.completed or cls.classification.status != Status.completed:
            cls.impact = cls.test_client.sessions.get(cls.impact.session_id)
            cls.forecast = cls.test_client.sessions.get(cls.forecast.session_id)
            cls.classification = cls.test_client.sessions.get(cls.classification.session_id)

            if counter > 120:
                raise TimeoutError('Running the sessions took longer than 10 minutes of setup time...')

            counter = counter + 1
            time.sleep(5)
