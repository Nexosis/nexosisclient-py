from nexosisapi.session import Session
from nexosisapi.algorithm_contestant import AlgorithmContestant

class SessionContest(Session):
    def __init__(self, data_dict=None):
        super(SessionContest, self).__init__(data_dict)
        self._champion = data_dict.get('champion')
        self._contestants = []
        for contestant in data_dict.get('contestants'):
            self._contestants.append(AlgorithmContestant(contestant))
        self._champion_metric = data_dict.get('championMetric')

    @property
    def champion(self):
        return self._champion

    @property
    def contestants(self):
        return self._contestants

    @property
    def champion_metric(self):
        return self._champion_metric