from enum import Enum


class Status(Enum):
    Requested = 0,
    Started = 1,
    Completed = 2,
    Cancelled = 3,
    Failed = 4,
    Estimated = 5


class SessionType(Enum):
    Import = 0,
    Forecast = 1,
    Impact = 2


class Session(object):
    def __init__(self):
        self._session_id = None
        self._type = None
        self._status = None
        self._status_history = None
        self._dataset_name = None
        self._target_column = None
        self._start_date = None
        self._end_date = None
        self._links = None
        self._is_estimate = None
        self._extra_parameters = None
        self._result_interval = None
        self._column_metadata = None

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


class SessionResult(Session):
    def __init__(self):
        super(SessionResult, self).__init__()

    @property
    def metrics(self):
        return self._metrics

    @property
    def data(self):
        return self._data
