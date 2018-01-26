from nexosisapi.paged_list import PagedList
from nexosisapi.vocabulary_summary import VocabularySummary
from nexosisapi.vocabulary import Vocabulary
from nexosisapi.word import Word


class Vocabularies(object):
    """Exposes API Operations on vocabularies"""

    def __init__(self, client):
        self._client = client


    def list(self, data_source=None, created_from_session=None, page_number=0, page_size=50):
        """Get the list of vocabularies built from sessions, optionally filtering by data set name or the session from which
        the vocabularies were built

        :param str data_source: optional name to filter vocabularies on
        :param str created_from_session: optional filter to limit vocabularies to those built from a particular session
        :param int page_number: optional zero-based page number of results to retrieve
        :param int page_size: optional count of results to retrieve in each page (default 50, max 1000).
        :return: a `list` of VocabularySummary objects representing the vocabularies built
        :rtype: list
        """

        params = {'page': page_number, 'pageSize': page_size}
        if data_source:
            params['dataSource'] = data_source

        if created_from_session:
            params['createdFromSession'] = created_from_session

        listing = self._client.request('GET', '/vocabulary',
                                       params=params)

        return PagedList.from_response(
            [VocabularySummary(item) for item in listing.get('items', [])],
            listing)


    def get(self, vocabulary_id, type=None, page_number=0, page_size=50):
        """Get the list of vocabulary words in a vocabulary

        :param str vocabulary_id: the vocabulary id whose words should be retrieved
        :param str type: optional filter to limit words to only Words or StopWords
        :param int page_number: optional zero-based page number of results to retrieve
        :param int page_size: optional count of results to retrieve in each page (default 50, max 1000).
        :return: a `list` of Word objects representing the words on the vocabulary
        :rtype: list
        """

        params = {'page': page_number, 'pageSize': page_size}
        if type:
            params['type'] = type


        listing = self._client.request('GET', '/vocabulary/%s' % vocabulary_id,
                                       params=params)

        return Vocabulary.from_response(
            [Word(item) for item in listing.get('items', [])],
            listing)
