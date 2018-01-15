from nexosisapi.session import Session
from nexosisapi.paged_list import PagedList


class ClassScores(Session):
    def __init__(self, data_dict=None):
        super(ClassScores, self).__init__(data_dict)
        self._classes = data_dict.get('classes', [])
        self._metrics = data_dict.get('metrics', {})
        self._data = PagedList.from_response(data_dict.get('data', []),data_dict)

    @property
    def classes(self):
        return self._classes

    @property
    def metrics(self):
        return self._metrics

    @property
    def data(self):
        return self._data
