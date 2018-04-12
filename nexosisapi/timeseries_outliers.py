from nexosisapi.session import Session
from nexosisapi.paged_list import PagedList
from nexosisapi.outlier import Outlier

class TimeseriesOutliers(Session):
    def __init__(self, data_dict):
        super(TimeseriesOutliers, self).__init__(data_dict)
        self._data = PagedList.from_response([Outlier(item) for item in data_dict.get('data', [])], data_dict)

    @property
    def data(self):
        return self._data