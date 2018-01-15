from nexosisapi.session import Session
from nexosisapi.paged_list import PagedList


class AnomalyScores(Session):
    def __init__(self, data_dict=None):
        super(AnomalyScores, self).__init__(data_dict)
        self._metrics = data_dict.get('metrics', {})
        self._data = PagedList.from_response(data_dict.get('data', []), data_dict)

    @property
    def metrics(self):
        return self._metrics

    @property
    def data(self):
        return self._data