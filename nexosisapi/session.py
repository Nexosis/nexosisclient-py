from enum import Enum

import dateutil.parser

from nexosisapi.column_metadata import ColumnMetadata
from nexosisapi.status import Status
from nexosisapi.time_interval import TimeInterval


class SessionType(Enum):
    import_ = 0,
    forecast = 1,
    impact = 2


class Session(object):
    def __init__(self, data_dict=None):
        if data_dict is None:
            data_dict = {}

        self._session_id = data_dict['sessionId']
        self._type = SessionType[data_dict['type']]
        self._status = Status[data_dict['status']]
        self._status_history = data_dict['statusHistory']
        self._dataset_name = data_dict['dataSetName']
        self._target_column = data_dict['targetColumn']
        self._start_date = dateutil.parser.parse(data_dict['startDate'])
        self._end_date = dateutil.parser.parse(data_dict['endDate'])
        self._requested_date = dateutil.parser.parse(data_dict['requestedDate'])
        self._links = data_dict['links']
        self._is_estimate = bool(data_dict['isEstimate'])
        self._extra_parameters = data_dict['extraParameters']
        self._result_interval = TimeInterval[data_dict['resultInterval']] \
            if 'resultInterval' in data_dict.keys() and data_dict['resultInterval'] \
            else TimeInterval.day
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
    def dataset_name(self):
        return self._dataset_name

    @property
    def target_column(self):
        return self._target_column

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
    def is_estimate(self):
        return self._is_estimate

    @property
    def result_interval(self):
        return self._result_interval

    @property
    def column_metadata(self):
        return self._column_metadata

    @property
    def extra_parameters(self):
        return self._extra_parameters

    def __repr__(self):
        return """Session({
    'sessionId': '%s',
    'type': '%s',
    'status': '%s',
    'statusHistory': %s,
    'dataSetName': '%s',
    'targetColumn': '%s',
    'startDate': '%s',
    'endDate': '%s',
    'resultInterval': '%s',
    'metadata': %s
    'requestedDate': '%s',
    'isEstimate': %s,
    'extraParameters': %s,
    'links': %s
})""" % (self._session_id, self._type.name, self._status.name, self._status_history, self._dataset_name,
            self._target_column, self._start_date, self._end_date, self._result_interval.name,
            self._column_metadata, self._requested_date, self._is_estimate,
            self._extra_parameters, self._links)


class SessionResponse(Session):
    def __init__(self, data_dict, headers):
        super(SessionResponse, self).__init__(data_dict)
        self._cost = headers.get('nexosis-request-cost')
        self._balance = headers.get('nexosis-account-balance')

    @property
    def cost(self):
        return self._cost

    @property
    def balance(self):
        return self._balance


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
    'dataSetName': '%s',
    'targetColumn': '%s',
    'startDate': '%s',
    'endDate': '%s',
    'resultInterval': '%s',
    'metadata': %s
    'requestedDate': '%s',
    'isEstimate': %s,
    'extraParameters': %s,
    'links': %s,
    'metrics': %s,
    'data': %s
})""" % (self._session_id, self._type.name, self._status.name, self._status_history, self._dataset_name,
            self._target_column, self._start_date, self._end_date, self._result_interval.name,
            self._column_metadata, self._requested_date, self._is_estimate,
            self._extra_parameters, self._links, self._metrics, self._data)

