class DistanceMetric(object):
    def __init__(self, metric_dict):
        keys = ['anomaly','mahalanobis_distance']
        try:
            self._anomaly_score = float(metric_dict.get(keys[0], ''))
            self._distance = float(metric_dict.get(keys[1], ''))
        except ValueError:
            self._anomaly_score = None
            self._distance = None

        self._data = {k: v for (k, v) in metric_dict.items() if k not in keys}

    @property
    def anomaly_score(self):
        return self._anomaly_score

    @property
    def distance(self):
        return self._distance

    @property
    def data(self):
        return self._data