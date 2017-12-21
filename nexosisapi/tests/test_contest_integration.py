import unittest
import os
from nexosisapi import Client
from nexosisapi.status import Status


class ContestIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_client = Client(key=os.environ['NEXOSIS_PAID_API_TESTKEY'],
                                 uri=os.environ['NEXOSIS_API_TESTURI'])
        if not os.environ['NEXOSIS_PAID_API_TESTKEY']:
            print('Paid API key was not found')
        current_sessions = cls.test_client.sessions.list('', page_size=100)
        cls.completed_session = next((s for s in current_sessions if s.status == Status.completed), None)


    def test_can_get_contest(self):
        actual = self.test_client.sessions.get_contest(self.completed_session.session_id)
        self.assertEqual(actual.session_id, self.completed_session.session_id)
        self.assertGreater(len(actual.contestants), 0)

    def test_can_get_champion_data(self):
        actual = self.test_client.sessions.get_champion(self.completed_session.session_id)
        self.assertGreater(len(actual.data), 0)
        self.assertIsNotNone(actual.algorithm.name)
        self.assertGreater(len(actual.metrics),0)

    def test_can_get_contestant_data(self):
        contestants = self.test_client.sessions.get_contest(self.completed_session.session_id).contestants
        contestant = next(iter(contestants), None)
        actual = self.test_client.sessions.get_contestant(self.completed_session.session_id, contestant.id)
        self.assertGreater(len(actual.data), 0)
        self.assertIsNotNone(actual.algorithm.name)
        self.assertGreater(len(actual.metrics),0)

    def test_can_get_metrics(self):
        actual = self.test_client.sessions.get_contest_selection_criteria(self.completed_session.session_id)
        self.assertIsNotNone(actual)
        self.assertGreater(len(actual.metric_sets), 0)