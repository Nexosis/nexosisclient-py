from nexosisapi.vocabulary_summary import VocabularySummary
from nexosisapi.vocabulary import Vocabulary
from nexosisapi.data_source_type import DataSourceType
from nexosisapi.word import Word, WordType
import unittest
import dateutil.parser

class VocabularySummaryUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.summary = VocabularySummary({'id': '123', 'dataSourceName': 'my-data-source', 'columnName': 'my-column', 'dataSourceType': "view", 'createdOnDate': '2000-01-01', 'createdBySessionId': '5678'})


    def test_parses_id(self):
        self.assertEqual('123', self.summary.id)

    def test_parses_data_source_name(self):
        self.assertEqual('my-data-source', self.summary.data_source_name)

    def test_parses_column_name(self):
        self.assertEqual('my-column', self.summary.column_name)

    def test_parses_data_source_type(self):
        self.assertEqual(DataSourceType.view, self.summary.data_source_type)

    def test_parses_created_on_date(self):
        self.assertEqual(dateutil.parser.parse("2000-01-01"), self.summary.created_on_date)

    def test_parses_session_id(self):
        self.assertEqual('5678', self.summary.created_by_session_id)


class VocabularyWordUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.word = Word({'text': 'all work and no play make jack a dull boy', 'type': 1, 'rank': 1})


    def test_parses_text(self):
        self.assertEqual('all work and no play make jack a dull boy', self.word.text)

    def test_parses_type(self):
        self.assertEqual(WordType.stop_word, self.word.type)

    def test_parses_rank(self):
        self.assertEqual(1, self.word.rank)

class VocabularyUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        message = {'id': '12345', 'items': [{'text': 'all work and no play make jack a dull boy', 'type': 0, 'rank': 1}, {'text': 'all work and no play make jack a dull boy', 'type': 0, 'rank': 1}], 'pageNumber': 1, 'totalPages': 2, 'pageSize': 3, 'totalCount': 10}
        cls.vocab = Vocabulary.from_response([Word(w) for w in message.get('items')], message)

    def test_parses_id(self):
        self.assertEqual('12345', self.vocab.vocabulary_id)

    def test_parses_items(self):
        self.assertEqual(2, len(self.vocab))

    def test_parses_paging_stuff(self):
        self.assertEqual(1, self.vocab.page_number)
        self.assertEqual(2, self.vocab.total_pages)
        self.assertEqual(3, self.vocab.page_size)
        self.assertEqual(10, self.vocab.item_total)



