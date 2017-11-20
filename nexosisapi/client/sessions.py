from nexosisapi.paged_list import PagedList
from nexosisapi.session import SessionResult, SessionResponse
from nexosisapi.time_interval import TimeInterval


class Sessions(object):
    """Session based API operations"""

    def __init__(self, client):
        self._client = client

    def _create_session(self, datasource_name, action_type, start_date, end_date, target_column=None, event_name=None,
                        result_interval=TimeInterval.day, is_estimate=False, column_metadata=None, callback_url=None):
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
                                                     'isEstimate': is_estimate,
                                                     'resultInterval': result_interval.name,
                                                     'callbackUrl': callback_url
                                                 })

    def create_forecast(self, datasource_name, target_column, start_date, end_date, result_interval=TimeInterval.day, callback_url=None):
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

    def create_forecast_with_metadata(self, datasource_name, column_metadata, start_date, end_date, result_interval=TimeInterval.day, callback_url=None):
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
        response, _, headers = self._create_session(datasource_name, 'forecast', start_date, end_date, result_interval=result_interval,
                                                    is_estimate=False, column_metadata=column_metadata, callback_url=callback_url)

        return SessionResponse(response, headers)

    def analyze_impact(self, datasource_name, target_column, event_name, start_date, end_date, result_interval=TimeInterval.day, callback_url=None):
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
                                                    result_interval=result_interval, is_estimate=True)
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
                                                    event_name, result_interval, is_estimate=True)
        return SessionResponse(response, headers)

    def train_model(self, datasource_name, target_column=None, column_metadata=None, prediction_domain='regression',callback_url=None):
        """Train a model for later predictions

        :param str datasource_name: the name of the data source to forecast on
        :param str target_column: the column from the data source that will be requested in predictions
        :param object column_metadata: a dict of column name mapped to ColumnMetadata objects describing the columns used in the modeling process
        :param string prediction_domain:
        :param str callback_url: the url to callback to on session status change events

        :return the session description
        :rtype: SessionResponse
        """
        response, _, headers = self._client.request_with_headers('POST', 'sessions/model',
                                                 data={
                                                     'predictionDomain': 'regression',
                                                     'dataSourceName': datasource_name,
                                                     'targetColumn': target_column,
                                                     'columns': column_metadata,
                                                     'callbackUrl': callback_url
                                                 })

        return SessionResponse(response, headers)

    def list(self, datasource_name=None, event_name=None, requested_after=None, requested_before=None, session_type=None, page_number=0, page_size=50):
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
