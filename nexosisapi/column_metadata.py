from enum import Enum


class ColumnType(Enum):
    string = 0
    numeric = 1
    logical = 2
    date = 3


class Role(Enum):
    none = 0
    timestamp = 1
    target = 2
    feature = 3


class ColumnMetadata(object):
    """The data describing a column in a dataset."""

    def __init__(self, data_dict={}):
        """Create an instance with the data or defaults

        Defaults to data_type = ColumnType.string and role = ColumnRole.none

        :arg dict data_dict: the dictionary containing the data for this object
        """

        self._data_type = ColumnType[data_dict.get('dataType') or 'string']
        self._role = Role[data_dict.get('role') or 'none']

    @property
    def data_type(self):
        """Gets the data_type of the column.

        :return: The data_type of the column.
        :rtype: ColumnType
        """
        return self._data_type

    @property
    def role(self):
        """Gets the role of the column.

        :return: The role of this column.
        :rtype: ColumnRole
        """
        return self._role

