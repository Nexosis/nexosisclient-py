import unittest
from nexosisapi.tests.fake_http_client import FakeHttpClient
from nexosisapi import Client
from nexosisapi.class_scores import ClassScores
from nexosisapi.anomaly_scores import AnomalyScores


class TestSession(unittest.TestCase):

    def test_can_build_class_scores(self):
        session = self.session_data
        session.update({
            'data': [{
                'x1': 'class1',
                'x1:class1': 3.2,
                'x1:class2': 2.1,
                'x2': 0.4829,
                'x3': 0.2343,
                'x1:actual': 'class1'
            }],
            'classes': ['class1', 'class2'],
            'metrics': {
                "macroAverageF1Score": 0.76363636363636367,
                "accuracy": 0.77777777777777779,
                "macroAveragePrecision": 0.81060606060606066,
                "macroAverageRecall": 0.77272727272727271,
                "matthewsCorrelationCoefficient": 0.75548589341692785
            }
        })
        actual = ClassScores(session)
        self.assertEqual(len(actual.data), 1)
        self.assertEqual(len(actual.metrics), 5)
        self.assertEqual(len(actual.classes), 2)
        self.assertEqual(actual.data[0]['x1:class1'], 3.2)
        self.assertEqual(actual.metrics['accuracy'], 0.77777777777777779)

    def test_can_build_anom_scores(self):
        session = self.session_data
        session.update({
            'data': [{
                'anomaly': -0.245645,
                'x1': 0.8348,
                'x2': .03422
            }],
            'metrics': {
                "percentAnomalies": 0.10119047619047619
            }
        })
        actual = AnomalyScores(session)
        self.assertEqual(len(actual.data), 1)
        self.assertEqual(len(actual.metrics), 1)
        self.assertEqual(actual.data[0]['anomaly'], -0.245645)
        self.assertEqual(actual.metrics['percentAnomalies'], 0.10119047619047619)

    def test_anomalies_includes_extra_parms(self):
        self.client.sessions.train_anomalies_model('test')
        self.assertEqual(self.http.args['data']['extraParameters']['containsAnomalies'], True)

    def test_class_scores_uses_correct_url(self):
        self.client.sessions.get_class_scores('f8d11e26-79f0-43b4-9545-111b8eaa00a5')
        self.assertEqual(self.http.uri, 'sessions/f8d11e26-79f0-43b4-9545-111b8eaa00a5/results/classScores')

    def test_anomaly_scores_uses_correct_url(self):
        self.client.sessions.get_anomaly_scores('f8d11e26-79f0-43b4-9545-111b8eaa00a5')
        self.assertEqual(self.http.uri, 'sessions/f8d11e26-79f0-43b4-9545-111b8eaa00a5/results/anomalyScores')

    @classmethod
    def setUpClass(cls):
        cls.session_data = {
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
        cls.http = FakeHttpClient(cls.session_data)
        cls.client = Client(client=cls.http)