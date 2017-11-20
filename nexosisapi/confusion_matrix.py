from nexosisapi.session import Session


class ConfusionMatrix(Session):
    def __init__(self, data_dict=None):
        super(ConfusionMatrix, self).__init__(data_dict)
        self._classes = data_dict.get('classes', [])
        self._values = data_dict.get('confusionMatrix', [[]])

    @property
    def classes(self):
        return self._classes

    @property
    def values(self):
        return self._values