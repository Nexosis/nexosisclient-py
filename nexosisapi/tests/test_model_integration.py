import os
import unittest
import dateutil.parser
import csv

from nexosisapi import Client


class ModelIntegrationTests(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/regression-predict.csv')) as f:
            csv_data = csv.DictReader(f)
            self.predict_data = [dict(d) for d in csv_data]

        self.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"], uri=os.environ["NEXOSIS_API_TESTURI"])
        models = self.test_client.models.list(datasource_name='data-regression-integration')

        # get the most recently created model. might not be from this run.
        self.test_model = sorted(models, key=lambda model: dateutil.parser.parse(model.created_on))[-1]

    def test_list_models(self):
        models = self.test_client.models.list(datasource_name='data-regression-integration')
        self.assertGreater(len(models), 0)

    def test_run_predict(self):
        results = self.test_client.models.predict(self.test_model.model_id, self.predict_data)
        print(results)
        self.assertEqual(4, len(results.data))
