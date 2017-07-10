from Lib.test.test_importlib import import_

import os
import requests
import json
from datetime import datetime, date

class NexosisClient:
    NEXOSIS_API_KEY = 'NEXOSIS_API_KEY'
    SESSION_STATUS_HEADER = 'Nexosis-Session-Status'

    def __init__(self, key = os.environ[NEXOSIS_API_KEY], uri='https://ml.nexosis.com/v1'):
        self.key = key
        if uri.endswith('/'):
            uri = uri[:-1]
        self.uri = uri

    @staticmethod
    def __json_serial(obj):
        """JSON serializer for datetime since it is not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type %s not serializable" % type(obj))

    def __generate_headers(self):
        return {
            'api-key': self.key,
            'User-Agent': 'Nexosis-Python-API-Client/1.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def __create_session(self, data, action_type, dataset_name, target_column, event_name,
                         start_date, end_date, column_metadata = {}, callback_url = None):
        resp = requests.post('%s/sessions/%s' % (self.uri, action_type),
                             params={
                                 'dataSetName': dataset_name,
                                 'targetColumn': target_column,
                                 'eventName': event_name,
                                 'startDate': start_date,
                                 'endDate': end_date,
                                 'callbackUrl': callback_url},
                             data=json.dumps(data, default = NexosisClient.__json_serial),
                             headers=self.__generate_headers())

        return resp.json(), resp.status_code, resp.headers

    def get_account_balance(self):
        balance_url = self.uri + "/data"
        response = requests.get(balance_url, headers=self.__generate_headers())
        if response.status_code == 200:
            return response.headers['nexosis-account-balance']
        else:
            response.raise_for_status()

    def create_forecast(self,dataset_name,start_date,end_date,column_metadata):
        return None

    def create_forecast(self, data, start_date, end_date, callback_url=None):
        """create_forecast"""
        return self.__create_session(
            data, 'forecast', None, target_column, None, start_date, end_date, callback_url)

    def analyze_impact(self, data, target_column, event_name, start_date, end_date, callback_url=None):
        """analyze_impact"""
        return self.__create_session(
            data, 'impact', None, target_column, event_name, start_date, end_date, callback_url)

    def get_status(self, session_id):
        """get_status"""
        resp = requests.head('%s/sessions/%s' % (self.uri, session_id), headers=self.__generate_headers())
        return None, resp.status_code, resp.headers

    def get_results(self, session_id):
        """get_results"""
        resp = requests.get('%s/sessions/%s/results' % (self.uri, session_id), headers=self.__generate_headers())
        return resp.json(), resp.status_code, resp.headers