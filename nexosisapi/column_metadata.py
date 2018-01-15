import io
from enum import Enum


class ColumnType(Enum):
    string = 0
    numeric = 1
    logical = 2
    date = 3
    text = 4
    numericMeasure = -1


class Role(Enum):
    none = 0
    timestamp = 1
    target = 2
    feature = 3
    key = 4


class Imputation(Enum):
    zeroes = 0
    mean = 1
    median = 2
    mode = 3
    min = 4
    max = 5


class Aggregation(Enum):
    sum = 0
    mean = 1
    median = 2
    mode = 3
    min = 4
    max = 5


class ColumnMetadata(object):
    """The data describing a column in a dataset."""

    def __init__(self, data_dict=None):
        """Create an instance with the data or defaults

        Defaults to data_type = ColumnType.string and role = ColumnRole.none

        :arg dict data_dict: the dictionary containing the data for this object
        """
        if data_dict is None:
            data_dict = {}

        impute = data_dict.get('imputation')
        aggregate = data_dict.get('aggregation')

        self._data_type = ColumnType[data_dict.get('dataType') or 'string']
        self._role = Role[data_dict.get('role') or 'none']
        self._imputation = Imputation[impute] if impute is not None else None
        self._aggregation = Aggregation[aggregate] if aggregate is not None else None

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

    @property
    def imputation(self):
        """Gets the imputation strategy of the column.

        :return: The imputation strategy of the column.
        :rtype: Imputation
        """
        return self._imputation

    @property
    def aggregation(self):
        """Gets the aggregation strategy of the column.

        :return: The aggregation strategy of the column.
        :rtype: Aggregation
        """
        return self._aggregation

    def __repr__(self):
        value = io.StringIO()

        value.write("ColumnMetadata({")
        value.write("'dataType': '%s'" % self._data_type.name)
        value.write(", 'role': '%s'" % self._role.name)
        if self._aggregation is not None:
            value.write(", 'aggregation': '%s'" % self._aggregation.name)
        if self._imputation is not None:
            value.write(", 'imputation': '%s'" % self._imputation.name)
        value.write("})")
        return value.getvalue()
