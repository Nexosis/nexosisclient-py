from nexosisapi.session import Session

class SessionSelectionMetrics(Session):
    def __init__(self, data_dict):
        super(SessionSelectionMetrics, self).__init__(data_dict)
        self._metric_sets = data_dict.get('metricSets', [])

    @property
    def metric_sets(self):
        return self._metric_sets