class Outlier(object):
    def __init__(self, outlier_data):
        self._timestamp = outlier_data.get('timeStamp')
        try:
            self._actual = float(next((value for key, value in outlier_data.items() if 'actual' in key.lower()), ''))
            self._smooth = float(next((value for key, value in outlier_data.items() if 'smooth' in key.lower()), ''))
        except ValueError:
            self._actual = None
            self._smooth = None


    @property
    def timestamp(self):
        return self._timestamp

    @property
    def actual(self):
        return self._actual

    @property
    def smooth(self):
        return self._smooth

