from nexosisapi.confusion_matrix import ConfusionMatrix
from nexosisapi.paged_list import PagedList
from nexosisapi.session import SessionResult, SessionResponse
from nexosisapi.time_interval import TimeInterval
from nexosisapi.session_contest import SessionContest
from nexosisapi.algorithm_contestant import AlgorithmContestant
from nexosisapi.session_selection_metrics import SessionSelectionMetrics
from nexosisapi.class_scores import ClassScores
from nexosisapi.anomaly_scores import AnomalyScores


class Sessions(object):
    """Session based API operations"""

    def __init__(self, client):
        self._client = client

    def _create_session(self, datasource_name, action_type, start_date, end_date, target_column=None, event_name=None,
                        result_interval=TimeInterval.day, column_metadata=None, callback_url=None):
        if datasource_name is None:
            raise ValueError('datasource_name is required and was not provided')
        if start_date is None:
            raise ValueError('start_date is required and was not provided')
        if end_date is None:
            raise ValueError('end_date is required and was not provided')

        return self._client.request_with_headers('POST', 'sessions/%s' % action_type,
                                                 data={
                                                     'dataSourceName': datasource_name,
                                                     'columns': column_metadata,
                                                     'targetColumn': target_column,
                                                     'eventName': event_name,
                                                     'startDate': start_date,
                                                     'endDate': end_date,
                                                     'resultInterval': result_interval.name,
                                                     'callbackUrl': callback_url
                                                 })

    def create_forecast(self, datasource_name, target_column, start_date, end_date, result_interval=TimeInterval.day,
                        callback_url=None):
        """Create a new forecast for a datasource

        :param str datasource_name: the name of the data source to forecast on
        :param str target_column: the column from the data source to forecast over
        :param datetime start_date: the first datetime of the forecast
        :param datetime end_date: the last datetime of the forecast
        :param TimeInterval result_interval: the interval between predictions in the results
        :param str callback_url: the url to callback to on session status change events

        :return the session description
        :rtype: SessionResponse
        """
        response, _, headers = self._create_session(datasource_name, 'forecast', start_date, end_date, target_column,
                                                    result_interval=result_interval, callback_url=callback_url)
        return SessionResponse(response, headers)

    def create_forecast_with_metadata(self, datasource_name, column_metadata, start_date, end_date,
                                      result_interval=TimeInterval.day, callback_url=None):
        """Create a new forecast for a datasource

        :param str datasource_name: the name of the data source to forecast on
        :param dict column_metadata: the metadata describing the columns to include in the session
        :param datetime start_date: the first datetime of the forecast
        :param datetime end_date: the last datetime of the forecast
        :param TimeInterval result_interval: the interval between predictions in the results
        :param str callback_url: the url to callback to on session status change events

        :return the session description
        :rtype: SessionResponse
        """
        response, _, headers = self._create_session(datasource_name, 'forecast', start_date, end_date,
                                                    result_interval=result_interval, column_metadata=column_metadata,
                                                    callback_url=callback_url)

        return SessionResponse(response, headers)

    def analyze_impact(self, datasource_name, target_column, event_name, start_date, end_date,
                       result_interval=TimeInterval.day, callback_url=None):
        """Create a new impact analysis on a datasource

        :param str datasource_name: the name of the data source to forecast on
        :param str target_column: the column from the data source to forecast over
        :param str event_name: the name of this analysis
        :param datetime start_date: the first datetime of the forecast
        :param datetime end_date: the last datetime of the forecast
        :param TimeInterval result_interval: the interval between predictions in the results
        :param str callback_url: the url to callback to on session status change events

        :return the session description
        :rtype: SessionResponse
        """
        response, _, headers = self._create_session(datasource_name, 'impact', start_date, end_date, target_column,
                                                    event_name, result_interval, callback_url=callback_url)
        return SessionResponse(response, headers)

    def estimate_forecast(self, datasource_name, target_column, start_date, end_date, result_interval=TimeInterval.day):
        """Estimate a new forecast for a datasource

        :param str datasource_name: the name of the data source to forecast on
        :param str target_column: the column from the data source to forecast over
        :param datetime start_date: the first datetime of the forecast
        :param datetime end_date: the last datetime of the forecast
        :param TimeInterval result_interval: the interval between predictions in the results

        :return the session description
        :rtype: SessionResponse
        """
        response, _, headers = self._create_session(datasource_name, 'forecast', start_date, end_date, target_column,
                                                    result_interval=result_interval)
        return SessionResponse(response, headers)

    def estimate_impact(self, datasource_name, target_column, event_name, start_date, end_date,
                        result_interval=TimeInterval.day):
        """Estimate an impact analysis on a dataset

        :param str datasource_name: the name of the data source to forecast on
        :param str target_column: the column from the data source to forecast over
        :param str event_name: the name of this analysis
        :param datetime start_date: the first datetime of the forecast
        :param datetime end_date: the last datetime of the forecast
        :param TimeInterval result_interval: the interval between predictions in the results

        :return the session description
        :rtype: SessionResponse
        """
        response, _, headers = self._create_session(datasource_name, 'impact', start_date, end_date, target_column,
                                                    event_name, result_interval)
        return SessionResponse(response, headers)

    def train_model(self, datasource_name, target_column=None, column_metadata=None, prediction_domain='regression',
                    callback_url=None, extra_parameters=None):
        """Train a model for later predictions

        :param str datasource_name: the name of the data source for which to create the model
        :param str target_column: the column from the data source that will be requested in predictions
        :param object column_metadata: a dict of column name mapped to ColumnMetadata objects describing the columns used in the modeling process
        :param string prediction_domain: a string indicating the desired model type: either 'regression', 'classification', or 'anomalies'
        :param str callback_url: the url to callback to on session status change events
        :param extra_parameters: additional indicators to modify this model building session

        :return the session description
        :rtype: SessionResponse
        """
        response, _, headers = self._client.request_with_headers('POST', 'sessions/model',
                                                                 data={
                                                                     'predictionDomain': prediction_domain,
                                                                     'dataSourceName': datasource_name,
                                                                     'targetColumn': target_column,
                                                                     'columns': column_metadata,
                                                                     'callbackUrl': callback_url,
                                                                     'extraParameters': extra_parameters
                                                                 })

        return SessionResponse(response, headers)

    def train_anomalies_model(self, datasource_name, contains_anomalies=True, column_metadata=None):
        """

        :param datasource_name: str datasource_name: the name of the data source on which to train the anomaly model
        :param contains_anomalies: does this data source contain the anomalies? Defaults to True.
        :param column_metadata: modify column types and/or roles for this session
        :return: the session description
        """
        return self.train_model(datasource_name=datasource_name, column_metadata=column_metadata,
                                extra_parameters={'containsAnomalies': contains_anomalies})

    def list(self, datasource_name=None, event_name=None, requested_after=None, requested_before=None,
             session_type=None, page_number=0, page_size=50):
        """Get a list of all sessions, optionally filtering on session parameters

        :param str datasource_name: the name of the data source the session is related to
        :param str event_name: filter on the event name given when running an impact analysis
        :param datetime requested_before: only include sessions requested before this date
        :param datetime requested_after: only include sessions requested after this date
        :param SessionType session_type: filter on the type of session
        :param int page_number: zero-based page number of results to retrieve
        :param int page_size: count of results to retrieve in each page (default 50, max 1000).

        :returns a list of `SessionResponse`
        :rtype list
        """
        query = {
            'page': page_number,
            'pageSize': page_size,
            'dataSourceName': datasource_name,
            'eventName': event_name,
            'requestedBefore': requested_before,
            'requestedAfter': requested_after,
            'sessionType': session_type
        }
        response, _, headers = self._client.request_with_headers('GET', 'sessions', params=query)
        return PagedList.from_response(
            [SessionResponse(item, headers) for item in response.get('items', [])],
            response)

    def remove(self, session_id):
        """Remove a session based on the session id

        :param str session_id: the session to remove
        """
        if session_id is None:
            raise ValueError('session_id is required and was not provided')

        self._client.request('DELETE', 'sessions/%s' % session_id)

    def remove_sessions(self, **kwargs):
        self._client.request('DELETE', 'sessions', params=kwargs)

    def get_results(self, session_id):
        """Get the results of a session based on the session id

        :param str session_id: the session to get results for

        :returns the results of computation run by the session
        :rtype SessionResult
        """
        if session_id is None:
            raise ValueError('session_id is required and was not provided')

        response = self._client.request('GET', 'sessions/%s/results' % session_id)
        return SessionResult(response)

    def get(self, session_id):
        """Get a session based on the session id

        :param str session_id: the session to get

        :returns the information about the session
        :rtype SessionResponse
        """
        if session_id is None:
            raise ValueError('session_id is required and was not provided')

        response, _, headers = self._client.request_with_headers('GET', 'sessions/%s' % session_id)
        return SessionResponse(response, headers)

    def get_confusion_matrix(self, session_id):
        """Get the confusion matrix results for a completed classification model.
        Note - will return 404 if not a completed classification model session

        :param session_id: the completed classification model building session
        :returns: a session result that includes matrix and labels
        :rtype: ConfusionMatrix
        """
        if session_id is None:
            raise ValueError('session_id is required and was not provided')

        response = self._client.request('GET', 'sessions/%s/results/confusionmatrix' % session_id)
        return ConfusionMatrix(response)

    def get_class_scores(self, session_id, page=0, pageSize=50):
        """
        Gets the class scores for each result of a particular completed classification model session
        Note - will return 404 if not a completed classification model session
        :param session_id: the completed classification model building session
        :param page: page number, defaults to 0
        :param pageSize: number of items per page, defaults to 50; 1000 max.
        :return: ClassScores
        """
        if session_id is None:
            raise ValueError('session_id is required and was not provided')

        response = self._client.request('GET', 'sessions/%s/results/classScores' % session_id)
        return ClassScores(response)

    def get_anomaly_scores(self, session_id, page=0, pageSize=50):
        """
        Gets the scores of the entire dataset generated by a particular completed anomalies session
        Note - will return 404 if not a completed anomalies model session
        :param session_id: the completed anomalies model building session
        :param page: page number, defaults to 0
        :param pageSize: number of items per page, defaults to 50; 1000 max.
        :return: AnomalyScores
        """
        if session_id is None:
            raise ValueError('session_id is required and was not provided')

        response = self._client.request('GET', 'sessions/%s/results/anomalyScores' % session_id)
        return AnomalyScores(response)

    def get_contest(self, session_id):
        """
        get information about the algorithm contestants used to determine session results
        :param session_id: the unique id of a completed session
        :returns: a collection of algorithms
        :rtype: SessionContest
        """
        if session_id is None or not session_id:
            raise ValueError('session_id is required and was not provided')
        response = self._client.request('GET', 'sessions/%s/contest' % session_id)
        return SessionContest(response)

    def get_champion(self, session_id):
        """
        Information about the winning algorithm for the given session
        :param session_id: the unique id of a completed session
        :returns: name, metrics and test data for champion of this session
        :rtype: AlgorithmContestant
        """
        if session_id is None or not session_id:
            raise ValueError('session_id is required and was not provided')
        response = self._client.request('GET', 'sessions/%s/contest/champion' % session_id)
        return AlgorithmContestant(response)

    def get_contestant(self, session_id, contestant_id):
        """
        Information about a contestant for this session
        :param session_id: the unique id of a completed session
        :param contestant_id: the unique id of the contestant from the session contest
        :returns: name, metrics, and test data for the given contestant
        :rtype: AlgorithmContestant
        """
        if session_id is None or not session_id:
            raise ValueError('session_id is required and was not provided')
        if contestant_id is None or not contestant_id:
            raise ValueError('contestant_id is required and was not provided')
        response = self._client.request('GET',
                                        'sessions/{0}/contest/contestants/{1}'.format(session_id, contestant_id))
        return AlgorithmContestant(response)

    def get_contest_selection_criteria(self, session_id):
        """
        Information about the dataset on which the session was based
        :param session_id: the unique id of a completed session
        :returns: dataset metrics used in algorithm selection
        :rtype: SessionSelectionMetrics
        """
        if session_id is None or not session_id:
            raise ValueError('session_id is required and was not provided')
        response = self._client.request('GET',
                                        'sessions/{0}/contest/selection'.format(session_id))
        return SessionSelectionMetrics(response)
