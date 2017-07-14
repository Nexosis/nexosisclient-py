from enum import Enum


class ColumnType(Enum):
    string = 0,
    numeric = 1,
    logical = 2,
    date = 3


class Role(Enum):
    none = 0,
    timestamp = 1,
    target = 2,
    feature = 3


class ColumnMetadata(object):
    """The data describing a column in a dataset."""

    def __init__(self, data_dict={}):
        """Create an instance with the data or defaults

        Defaults to data_type = ColumnType.string and role = ColumnRole.none

        :arg dict data_dict: the dictionary containing the data for this object
        """

        self._data_type = ColumnType[data_dict.get('dataType', 'string')]
        self._role = Role[data_dict.get('role', 'none')]

    @property
    def data_type(self):
        """Gets the data_type of the column.

        :return: The data_type of the column.
        :rtype: ColumnType
        """
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        """Sets the data_type of the metadata.

        :param ColumnType data_type: the specified data type of the metadata
        """
        self._data_type = data_type

    @property
    def role(self):
        """Gets the role of the column.

        :return: The role of this column.
        :rtype: ColumnRole
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this column.

        :param ColumnRole role: The role of this column.
        """
        self._role = role

