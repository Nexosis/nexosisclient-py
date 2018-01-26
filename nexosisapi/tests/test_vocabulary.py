from nexosisapi.vocabulary_summary import VocabularySummary
import unittest
import dateutil.parser

class VocabularySummaryUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.summary = VocabularySummary({'id': '123', 'dataSourceName': 'my-data-source', 'columnName': 'my-column', 'dataSourceType': 1, 'createdOnDate': '2000-01-01', 'createdBySessionId': '5678'})


    def test_parses_id(self):
        self.assertEqual('123', self.summary.id)

    def test_parses_data_source_name(self):
        self.assertEqual('my-data-source', self.summary.data_source_name)

    def test_parses_column_name(self):
        self.assertEqual('my-column', self.summary.column_name)

    def test_parses_created_on_date(self):
        self.assertEqual(dateutil.parser.parse("2000-01-01"), self.summary.created_on_date)

    def test_parses_session_id(self):
        self.assertEqual('5678', self.summary.created_by_session_id)