from nexosisapi.word import Word
from nexosisapi.paged_list import PagedList

class Vocabulary(PagedList):
    """A vocabulary"""

    def __init__(self, vocabulary_id, *args, **kwargs):
        super(Vocabulary, self).__init__(*args, **kwargs)
        self._id = vocabulary_id

    @property
    def vocabulary_id(self):
        return self._id

    @staticmethod
    def from_response(items, response_dict):
        return Vocabulary(response_dict.get('id', None), items,
                         page_number=response_dict.get('pageNumber', 0),
                         page_size=response_dict.get('pageSize', 50),
                         item_total=response_dict.get('totalCount', 50),
                         total_pages=response_dict.get('totalPages', 1),
                         links=[Link(item['rel'], item['href']) for item in response_dict.get('links', [])])
