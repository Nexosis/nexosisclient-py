import unittest
import nexosisclient
import os


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.test_client = nexosisclient.NexosisClient(key=os.environ["NEXOSIS_API_TESTKEY"],
                                                       uri=os.environ["NEXOSIS_API_TESTURI"])

    def test_can_create_client_with_env_key(self):
        target = nexosisclient.NexosisClient()
        self.assertIsNotNone(target.key)

    def test_can_override_client_base_uri(self):
        target = nexosisclient.NexosisClient(uri='https://api.uat.nexosisdev.com/v1')
        self.assertEqual(target.uri, "https://api.uat.nexosisdev.com/v1")

    def test_api_returns_current_balance(self):
        actual = self.test_client.get_account_balance()
        self.assertIsNotNone(actual)
        self.assertTrue(actual > 0)


class SessionIntegrationTests(unittest.TestCase):
    def setUp(self):
        pass


class DataSetIntegrationTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
