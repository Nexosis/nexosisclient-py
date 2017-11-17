import os
import unittest

import nexosisapi


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.test_client = nexosisapi.Client(key=os.environ["NEXOSIS_API_TESTKEY"], uri=os.environ["NEXOSIS_API_TESTURI"])

    def test_can_create_client_with_env_key(self):
        target = nexosisapi.Client()
        self.assertIsNotNone(target._key)

    def test_can_override_client_base_uri(self):
        target = nexosisapi.Client(uri='https://something.example.com/v1')
        self.assertEqual(target._uri, 'https://something.example.com/v1', 'uri not set by constructor')
