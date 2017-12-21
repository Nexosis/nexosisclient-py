import unittest
import os

import sys

from nexosisapi import Client, ClientError
from nexosisapi.status import Status


class ContestIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.can_test = True
        cls.test_client = Client(key=os.environ['NEXOSIS_PAID_API_TESTKEY'],
                                 uri=os.environ['NEXOSIS_API_TESTURI'])
        try:
            current_sessions = cls.test_client.sessions.list('', page_size=100)
            cls.completed_session = next((s for s in current_sessions if s.status == Status.completed), None)
        except(ClientError):
            # HACK: having issues with different key
            print('Could not execute listing for sessions. Aborting this test suite')
            cls.can_test = False

    def test_can_get_contest(self):
        if not self.can_test:
            return
        actual = self.test_client.sessions.get_contest(self.completed_session.session_id)
        self.assertEqual(actual.session_id, self.completed_session.session_id)
        self.assertGreater(len(actual.contestants), 0)

    def test_can_get_champion_data(self):
        if not self.can_test:
            return
        actual = self.test_client.sessions.get_champion(self.completed_session.session_id)
        self.assertGreater(len(actual.data), 0)
        self.assertIsNotNone(actual.algorithm.name)
        self.assertGreater(len(actual.metrics),0)

    def test_can_get_contestant_data(self):
        if not self.can_test:
            return
        contestants = self.test_client.sessions.get_contest(self.completed_session.session_id).contestants
        contestant = next(iter(contestants), None)
        actual = self.test_client.sessions.get_contestant(self.completed_session.session_id, contestant.id)
        self.assertGreater(len(actual.data), 0)
        self.assertIsNotNone(actual.algorithm.name)
        self.assertGreater(len(actual.metrics),0)

    def test_can_get_metrics(self):
        if not self.can_test:
            return
        actual = self.test_client.sessions.get_contest_selection_criteria(self.completed_session.session_id)
        self.assertIsNotNone(actual)
        self.assertGreater(len(actual.metric_sets), 0)