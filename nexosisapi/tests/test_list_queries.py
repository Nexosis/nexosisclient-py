import unittest
from datetime import datetime, timedelta
from nexosisapi.list_queries import *
from dateutil import parser

class TestListQueries(unittest.TestCase):
    def test_dataset_query_uses_name(self):
        target = DatasetListQuery(partial_name='foo')
        actual = target.query_parameters()
        self.assertTrue('partialName' in actual.keys())
        self.assertEqual(actual['pageSize'], 50)

    def test_session_query_uses_dates(self):
        target = SessionListQuery(options={'requested_after_date': datetime.datetime.now() - timedelta(days=2)})
        actual = target.query_parameters()['requestedAfterDate']
        self.assertTrue(type(actual) is str)

    def test_session_query_formats_with_tz(self):
        target = SessionListQuery(options={'requested_after_date': parse('2018-04-11T20:18:05+0300')})
        actual = target.query_parameters()['requestedAfterDate']
        self.assertEqual(actual,'2018-04-11T20:18:05+0300')

    def test_session_query_handles_string(self):
        target = SessionListQuery(options={
            'requested_before_date': '2018-04-11T20:18:05+0300'})
        actual = target.query_parameters()['requestedBeforeDate']
        self.assertEqual(actual, '2018-04-11T20:18:05+0300')

    def test_session_query_handles_empty_options(self):
        target = SessionListQuery()
        actual = target.query_parameters()
        self.assertEqual(actual['pageSize'], 50)