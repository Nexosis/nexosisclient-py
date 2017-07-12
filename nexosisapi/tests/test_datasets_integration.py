import os
import unittest

import nexosisapi


class DatasetsIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.test_client = nexosisapi.Client(key=os.environ["NEXOSIS_API_TESTKEY"],
                                             uri=os.environ["NEXOSIS_API_TESTURI"])

    def test_something(self):
        self.test_client.datasets.create_json()
