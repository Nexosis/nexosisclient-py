from enum import Enum
import dateutil.parser

from nexosisapi.column_metadata import ColumnMetadata
from nexosisapi.time_interval import TimeInterval


class Status(Enum):
    requested = 0,
    started = 1,
    completed = 2,
    cancelled = 3,
    failed = 4,
    estimated = 5


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
        self._links = data_dict['links']
        self._is_estimate = bool(data_dict['isEstimate'])
        self._extra_parameters = data_dict['extraParameters']
        self._result_interval = TimeInterval[data_dict['resultInterval']] if 'resultInterval' in data_dict.keys() and \
                                                                             data_dict[
                                                                                 'resultInterval'] else TimeInterval.day
        self._column_metadata = {key: ColumnMetadata(value) for (key, value) in data_dict.get('metadata', {}).items()}

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


class SessionResponse(Session):
    def __init__(self, data_dict):
        super(SessionResponse, self).__init__(data_dict)
        self._cost = 0
        self._balance = 0

    @property
    def cost(self):
        return self._cost

    @property
    def balance(self):
        return self._balance


class SessionResult(Session):
    def __init__(self, data_dict):
        super(SessionResult, self).__init__(data_dict)

        self._metrics = None
        self._data = None

    @property
    def metrics(self):
        return self._metrics

    @property
    def data(self):
        return self._data
