from enum import Enum

import dateutil.parser

from nexosisapi.column_metadata import ColumnMetadata
from nexosisapi.status import Status
from nexosisapi.time_interval import TimeInterval


class SessionType(Enum):
    import_ = 0,
    forecast = 1,
    impact = 2,
    model = 3


class Session(object):
    def __init__(self, data_dict=None):
        if data_dict is None:
            data_dict = {}

        self._session_id = data_dict['sessionId']
        self._type = SessionType[data_dict['type']]
        self._status = Status[data_dict['status']]
        self._status_history = data_dict['statusHistory']
        self._datasource_name = data_dict['dataSourceName']
        self._target_column = data_dict['targetColumn']
        if 'modelId' in data_dict:
            self._model_id = data_dict['modelId']
        else:
            self._model_id = None
        if 'startDate' in data_dict:
            self._start_date = dateutil.parser.parse(data_dict['startDate'])
        else:
            self._start_date = None
        if 'endDate' in data_dict:
            self._end_date = dateutil.parser.parse(data_dict['endDate'])
        else:
            self._end_date = None
        self._requested_date = dateutil.parser.parse(data_dict['requestedDate'])
        self._links = data_dict['links']
        self._extra_parameters = data_dict['extraParameters']
        self._result_interval = TimeInterval[data_dict['resultInterval']] \
            if 'resultInterval' in data_dict and data_dict['resultInterval'] \
            else TimeInterval.day
        self._available_prediction_intervals = data_dict.get('availablePredictionIntervals')
        self._prediction_domain = data_dict.get('predictionDomain', 'none')
        md = data_dict.get('metadata') or {}
        self._column_metadata = {key: ColumnMetadata(value) for (key, value) in md.items()}

    @property
    def session_id(self):
        return self._session_id

    @property
    def type(self):
        return self._type

    @property
    def status(self):
        return self._status

    @property
    def status_history(self):
        return self._status_history

    @property
    def datasource_name(self):
        return self._datasource_name

    @property
    def target_column(self):
        return self._target_column

    @property
    def model_id(self):
        return self._model_id

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def requested_date(self):
        return self._requested_date

    @property
    def links(self):
        return self._links

    @property
    def result_interval(self):
        return self._result_interval

    @property
    def column_metadata(self):
        return self._column_metadata

    @property
    def available_prediction_intervals(self):
        return self._available_prediction_intervals

    @property
    def prediction_domain(self):
        return self._prediction_domain

    @property
    def extra_parameters(self):
        return self._extra_parameters

    def __repr__(self):
        return """Session({
    'sessionId': '%s',
    'type': '%s',
    'status': '%s',
    'statusHistory': %s,
    'dataSourceName': '%s',
    'targetColumn': '%s',
    'modelId': '%s',
    'startDate': '%s',
    'endDate': '%s',
    'resultInterval': '%s',
    'metadata': %s
    'requestedDate': '%s',
    'availablePredictionIntervals': '%s',
    'extraParameters': %s,
    'links': %s
})""" % (self._session_id, self._type.name, self._status.name, self._status_history, self._datasource_name,
            self._target_column, self._model_id, self._start_date, self._end_date, self._result_interval.name,
            self._column_metadata, self._requested_date, self._available_prediction_intervals,
            self._extra_parameters, self._links)


class SessionResponse(Session):
    def __init__(self, data_dict, headers):
        super(SessionResponse, self).__init__(data_dict)
        self._dataset_count = headers.get('nexosis-account-datasetcount-current')
        self._datasets_allowed = headers.get('nexosis-account-datasetcount-allotted')
        self._session_count = headers.get('nexosis-account-sessioncount-current')
        self._sessions_allowed = headers.get('nexosis-account-sessioncount-allotted')
        self._prediction_count = headers.get('nexosis-account-predictioncount-current')
        self._predictions_allowed = headers.get('nexosis-account-predictioncount-allotted')

    @property
    def dataset_count(self):
        return self._dataset_count

    @property
    def datasets_allowed(self):
        return self._datasets_allowed

    @property
    def session_count(self):
        return self._session_count

    @property
    def sessions_allowed(self):
        return self._sessions_allowed

    @property
    def prediction_count(self):
        return self._prediction_count

    @property
    def predictions_allowed(self):
        return self._predictions_allowed


class SessionResult(Session):
    def __init__(self, data_dict):
        super(SessionResult, self).__init__(data_dict)

        self._metrics = data_dict['metrics']
        self._data = data_dict['data']

    @property
    def metrics(self):
        return self._metrics

    @property
    def data(self):
        return self._data

    def __repr__(self):
        return """SessionResult({
    'sessionId': '%s',
    'type': '%s',
    'status': '%s',
    'statusHistory': %s,
    'dataSourceName': '%s',
    'targetColumn': '%s',
    'modelId': '%s',
    'startDate': '%s',
    'endDate': '%s',
    'resultInterval': '%s',
    'metadata': %s
    'requestedDate': '%s',
    'extraParameters': %s,
    'availablePredictionIntervals': '%s',
    'links': %s,
    'metrics': %s,
    'data': %s
})""" % (self._session_id, self._type.name, self._status.name, self._status_history, self._datasource_name,
            self._target_column, self._model_id, self._start_date, self._end_date, self._result_interval.name,
            self._column_metadata, self._requested_date, self._available_prediction_intervals,
            self._extra_parameters, self._links, self._metrics, self._data)

