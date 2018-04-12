from nexosisapi.session import Session
from nexosisapi.paged_list import PagedList


class FeatureImportance(Session):
    def __init__(self, scores_dict=None):
        super(FeatureImportance, self).__init__(scores_dict)
        self._scores = scores_dict.get('featureImportance', {})

    @property
    def scores(self):
        return self._scores