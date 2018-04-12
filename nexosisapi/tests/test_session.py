import unittest
import datetime
from nexosisapi.tests.fake_http_client import FakeHttpClient
from nexosisapi import Client
from nexosisapi.class_scores import ClassScores
from nexosisapi.anomaly_scores import AnomalyScores
from nexosisapi.feature_importance import FeatureImportance
from nexosisapi.outlier import Outlier
from nexosisapi.timeseries_outliers import TimeseriesOutliers
from nexosisapi.distance_metric import DistanceMetric
from nexosisapi.anomaly_distances import AnomalyDistances

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

    def test_can_build_importance_scores(self):
        session = self.session_data
        session.update({
             'featureImportance' : {
                "col1": 0.91805331325755257,
                "col2": 1,
                "col3": 0.21478609588442729,
                "col4:0": 0.0526418163207683,
                "col4:1": 0.10938777105141982,
             }
            })
        actual = FeatureImportance(session)
        self.assertEqual(len(actual.scores), 5)
        self.assertEqual(actual.scores['col3'], 0.21478609588442729)

    def test_anomalies_includes_extra_parms(self):
        self.client.sessions.train_anomalies_model('test')
        self.assertEqual(self.http.args['data']['extraParameters']['containsAnomalies'], True)

    def test_class_scores_uses_correct_url(self):
        self.client.sessions.get_class_scores('f8d11e26-79f0-43b4-9545-111b8eaa00a5')
        self.assertEqual(self.http.uri, 'sessions/f8d11e26-79f0-43b4-9545-111b8eaa00a5/results/classScores')

    def test_anomaly_scores_uses_correct_url(self):
        self.client.sessions.get_anomaly_scores('f8d11e26-79f0-43b4-9545-111b8eaa00a5')
        self.assertEqual(self.http.uri, 'sessions/f8d11e26-79f0-43b4-9545-111b8eaa00a5/results/anomalyScores')

    def test_feature_importance_uses_correct_url(self):
        self.client.sessions.get_feature_importance('f8d11e26-79f0-43b4-9545-111b8eaa00a5')
        self.assertEqual(self.http.uri, 'sessions/f8d11e26-79f0-43b4-9545-111b8eaa00a5/results/featureimportance')

    def test_timeseries_outliers_uses_correct_url(self):
        self.client.sessions.get_timeseries_outliers('f8d11e26-79f0-43b4-9545-111b8eaa00a5')
        self.assertEqual(self.http.uri, 'sessions/f8d11e26-79f0-43b4-9545-111b8eaa00a5/results/outliers')

    def test_timeseries_outliers_uses_correct_url(self):
        self.client.sessions.get_distance_metrics('f8d11e26-79f0-43b4-9545-111b8eaa00a5')
        self.assertEqual(self.http.uri, 'sessions/f8d11e26-79f0-43b4-9545-111b8eaa00a5/results/mahalanobisdistances')

    def test_outlier_parses_keys(self):
        target = Outlier({'timeStamp': datetime.datetime.now, 'sales:actual': 25.65, 'sales:smooth': 300.00})
        self.assertEqual(target.smooth, 300.00)

    def test_outlier_parses_string_values(self):
        target = Outlier({'timeStamp': datetime.datetime.now, 'sales:actual': '25.65', 'sales:smooth': '300.00'})
        self.assertEqual(target.actual, 25.65)

    def test_outlier_safe_if_missing_value(self):
        target = Outlier({'timeStamp': datetime.datetime.now})
        self.assertIsNone(target.actual)

    def test_outliers_from_data(self):
        session = self.session_data
        session.update({
            'data': [
            {
                'timeStamp': '1/5/2014 12:00:00 AM',
                'sales:actual': 229.09,
                'sales:smooth': 1743.42167102697
            },
            {
                'timeStamp': '1/6/2014 12:00:00 AM',
                'sales:actual': 0,
                'sales:smooth': 1920.29538270229
            }
        ]})
        target = TimeseriesOutliers(session)
        self.assertEqual(len(target.data), 2)
        self.assertEqual(target.data[0].actual, 229.09)

    def test_distance_from_data(self):
        data = {'anomaly': 0.0487072268545709, 'col1': 85.7984, 'col2': 0.93, 'mahalanobis_distance': 143.312589889491}
        actual = DistanceMetric(data)
        self.assertEqual(actual.anomaly_score, 0.0487072268545709)
        self.assertTrue('col1' in actual.data.keys())
        self.assertFalse('anomaly' in actual.data.keys())

    def test_anomaly_distances_adds_all_data(self):
        session = self.session_data
        session.update({
            'data': [
                {
                    'anomaly': '0.0487072268545709',
                    'Ash': '2',
                    'Hue': '0.93',
                    'Alcohol': '12',
                    'ODRatio': '3.05',
                    'mahalanobis_distance': '143.312589889491'
                },
                {
                    'anomaly': '0.000317797613019206',
                    'Ash': '2.28',
                    'Hue': '1.25',
                    'Alcohol': '12.33',
                    'ODRatio': '1.67',
                    'mahalanobis_distance': '156.112291933161'
                }
            ],
            'pageNumber': 0,
            'totalPages': 4,
            'pageSize': 50,
            'totalCount': 178,
        })
        actual = AnomalyDistances(session)
        self.assertEqual(len(actual.data), 2)
        self.assertEqual(actual.data.page_number, 0)
        self.assertEqual(actual.data.page_size, 50)

    @classmethod
    def setUpClass(cls):
        cls.session_data = {
            'sessionId': 'f8d11e26-79f0-43b4-9545-111b8eaa00a5',
            'type': 'forecast',
            'status': 'completed',
            'predictionDomain': 'forecast',
            'supportsFeatureImportance': True,
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