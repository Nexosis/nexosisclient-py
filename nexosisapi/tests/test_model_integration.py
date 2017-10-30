import os
import unittest
import time

import dateutil.parser
import csv

from nexosisapi import Client, ClientError
from nexosisapi.tests import build_test_dataset


class ModelIntegrationTests(unittest.TestCase):
    regression_ds_name = 'model_tests_data'

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/regression-predict.csv')) as f:
            csv_data = csv.DictReader(f)
            cls.predict_data = [dict(d) for d in csv_data]

            cls.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"], uri=os.environ["NEXOSIS_API_TESTURI"])
        models = cls.test_client.models.list()
        if len(models) == 0:
            build_test_dataset(cls.test_client, 'data/regression-data.csv', cls.regression_ds_name)
            model_session = cls.test_client.sessions.train_regression_model(cls.regression_ds_name, 'Profit')
            while True:
                model_session = cls.test_client.sessions.get(model_session.session_id)
                if model_session.status.name == 'completed' or model_session.status.name == 'failed':
                    break
                time.sleep(10)
            models = cls.test_client.models.list()
        # get the most recently created model. might not be from this run.
        cls.test_model = sorted(models, key=lambda model: dateutil.parser.parse(model.created_on))[-1]

    @classmethod
    def tearDownClass(cls):
        try:
            cls.test_client.datasets.remove(cls.regression_ds_name, None, None, ['model'])
        except ClientError:
            return

    def test_list_models(self):
        models = self.test_client.models.list(datasource_name=self.test_model.datasource_name)
        self.assertGreater(len(models), 0)

    def test_list_is_paged(self):
        actual = self.test_client.models.list(page_number=1, page_size=10)
        self.assertEqual(1, actual.page_number)
        self.assertEqual(10, actual.page_size)

    def test_run_predict(self):
        results = self.test_client.models.predict(self.test_model.model_id, self.predict_data)
        self.assertEqual(4, len(results.data))
