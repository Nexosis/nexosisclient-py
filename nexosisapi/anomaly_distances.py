from nexosisapi.session import Session
from nexosisapi.paged_list import PagedList
from nexosisapi.distance_metric import DistanceMetric

class AnomalyDistances(Session):
    def __init__(self, anomaly_dict):
        super(AnomalyDistances, self).__init__(anomaly_dict)
        self._data = PagedList.from_response([DistanceMetric(item) for item in anomaly_dict.get('data', [])], anomaly_dict)

    @property
    def data(self):
        return self._data