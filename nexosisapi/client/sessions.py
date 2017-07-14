class Sessions(object):
    def __init__(self, client):
        self._client = client

    def _create_session(self, dataset_name, action_type, target_column, event_name,
                        start_date, end_date, is_estimate=False, column_metadata=None, callback_url=None):
        resp = self._client.request('POST', 'sessions/%s' % action_type,
                                    params={
                                        'dataSetName': dataset_name,
                                        'targetColumn': target_column,
                                        'eventName': event_name,
                                        'startDate': start_date,
                                        'endDate': end_date,
                                        'isEstimate': is_estimate,
                                        'callbackUrl': callback_url})

        return resp

    def create_forecast(self, dataset_name, target_column, start_date, end_date, callback_url=None):
        """create_forecast"""
        return self._create_session(
            dataset_name, 'forecast', target_column, None, start_date, end_date, callback_url)

    def analyze_impact(self, dataset_name, target_column, event_name, start_date, end_date, callback_url=None):
        """analyze_impact"""
        return self._create_session(
            dataset_name, 'impact', target_column, event_name, start_date, end_date, callback_url)

    def estimate_forecast(self, dataset_name, target_column, start_date, end_date):
        """create_forecast"""
        return self._create_session(
            dataset_name, 'forecast', target_column, None, start_date, end_date, is_estimate=True)

    def estimate_impact(self, dataset_name, target_column, event_name, start_date, end_date):
        """analyze_impact"""
        return self._create_session(
            dataset_name, 'impact', target_column, event_name, start_date, end_date, is_estimate=True)

    def list(self, dataset_name, event_name, requested_after, requested_before, session_type):
        pass

    def remove(self, session_id):
        """Remove a sessions based on the session id

        :param str session_id: the session to remove
        """
        self._client.request('DELETE', 'sessions/%s' % session_id)

    def remove_sessions(self, **kwargs):
        self._client.request('DELETE', 'sessions', params=kwargs)

    def get_results(self):
        pass

    def get(self):
        pass
