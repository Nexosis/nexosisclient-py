import unittest
from nexosisapi.algorithm import Algorithm
from nexosisapi.session_contest import SessionContest
from nexosisapi.algorithm_contestant import AlgorithmContestant


class TestContest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session_data = {
            'championMetric': 'meanAbsoluteError',
            'champion': cls.algorithm_contestant(),
            'contestants': [
                cls.algorithm_contestant(),
                cls.algorithm_contestant()
            ],
            'sessionId': 'f8d11e26-79f0-43b4-9545-111b8eaa00a5',
            'type': 'forecast',
            'status': 'completed',
            'predictionDomain': 'forecast',
            'availablePredictionIntervals': ['0.5'],
            'startDate': '2017-09-01T00:00:00+00:00',
            'endDate': '2017-09-30T00:00:00+00:00',
            'requestedDate': '2017-12-19T04:30:16.070806+00:00',
            'statusHistory': [],
            'extraParameters': {},
            'messages': [],
            'dataSourceName': '',
            'targetColumn': '',
            'links': []
        }

    def test_can_build_contest_from_dict(self):
        actual = SessionContest(self.session_data)
        self.assertEqual(actual.session_id, 'f8d11e26-79f0-43b4-9545-111b8eaa00a5')
        self.assertEqual(actual.champion_metric, 'meanAbsoluteError')
        self.assertEqual(len(actual.contestants), 2)

    def test_algorithm_built_from_dict(self):
        actual = Algorithm(self.algorithm())
        self.assertEqual(actual.name, 'Bayesian Structural Time Series, Weekly')

    def test_algorithm_contestant_includes_metrics(self):
        actual = AlgorithmContestant(self.algorithm_contestant())
        self.assertEqual(actual.metrics['meanAbsoluteError'], 693.40022421791662)

    def test_algorithm_contestant_holds_data(self):
        data = self.algorithm_contestant()
        data['data'] = [
            {
                "foo": "bar"
            },
            {
                "bar": "fun"
            }
        ]
        actual = AlgorithmContestant(data)
        self.assertEqual(len(actual.data), 2)

    @classmethod
    def algorithm(cls):
        return {
            'name': 'Bayesian Structural Time Series, Weekly',
            'description': 'Time series regression using dynamic linear models fit using MCMC, with weekly seasonality',
            'key': ''
        }

    @classmethod
    def algorithm_contestant(cls):
        return {
            'id': 'e7a683d6-b7cd-473e-a0e7-af8c1f369f0f',
            'algorithm': cls.algorithm(),
            'dataSourceProperties': [
                'Aggregated',
                'Imputed',
                'Smoothed'
            ],
            'metrics': {
                'meanAbsoluteError': 693.40022421791662,
                'meanAbsolutePercentError': 0.1215356667023087,
                'meanAbsoluteScaledError': 0.47103415512843011,
                'rootMeanSquareError': 832.50318786515641,
                'rSquared': 0.75624852461790371
            },
            'links': []
        }
