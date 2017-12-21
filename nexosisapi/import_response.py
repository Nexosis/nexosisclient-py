from enum import Enum
import dateutil.parser

from nexosisapi.column_metadata import ColumnMetadata
from nexosisapi.status import Status


class ImportType(Enum):
    s3 = 0,
    url = 1,
    azure = 2


class ImportResponse(object):
    def __init__(self, data_dict=None):
        if data_dict is None:
            data_dict = {}

        self._import_id = data_dict['importId']
        self._type = ImportType[data_dict['type']]
        self._status = Status[data_dict['status']]
        self._dataset_name = data_dict['dataSetName']
        self._requested_date = dateutil.parser.parse(data_dict['requestedDate'])
        self._status_history = data_dict['statusHistory']
        self._links = data_dict['links']
        self._parameters = data_dict['parameters']
        self._messages = data_dict['messages']
        md =  data_dict.get('metadata') or {}
        self._column_metadata = {key: ColumnMetadata(value) for (key, value) in md.items()}

    @property
    def import_id(self):
        return self._import_id

    @property
    def type(self):
        return self._type

    @property
    def status(self):
        return self._status

    @property
    def dataset_name(self):
        return self._dataset_name

    @property
    def status_history(self):
        return self._status_history

    @property
    def links(self):
        return self._links

    @property
    def parameters(self):
        return self._parameters

    @property
    def messages(self):
        return self._messages

    @property
    def column_metadata(self):
        return self._column_metadata

    @property
    def requested_date(self):
        return self._requested_date
