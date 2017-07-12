class Sessions(object):
    def __init__(self, client):
        self._client = client

    def _create_session(self, data, action_type, dataset_name, target_column, event_name,
                        start_date, end_date, column_metadata={}, callback_url=None):
        resp = self._client.request('POST', '%s/sessions/%s' % (self._uri, action_type),
                                    params={
                                        'dataSetName': dataset_name,
                                        'targetColumn': target_column,
                                        'eventName': event_name,
                                        'startDate': start_date,
                                        'endDate': end_date,
                                        'callbackUrl': callback_url},
                                    data=data)

        return resp.json(), resp.status_code, resp.headers

    def create_forecast(self, data, target_column, start_date, end_date, callback_url=None):
        """create_forecast"""
        return self._create_session(
            data, 'forecast', None, target_column, None, start_date, end_date, callback_url)

    def analyze_impact(self, data, target_column, event_name, start_date, end_date, callback_url=None):
        """analyze_impact"""
        return self._create_session(
            data, 'impact', None, target_column, event_name, start_date, end_date, callback_url)
