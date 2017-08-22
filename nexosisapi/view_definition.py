from nexosisapi.time_interval import TimeInterval
from nexosisapi.column_metadata import ColumnMetadata


class ColumnOptions(object):
    """The options defined on a specific column within a join"""

    def __init__(self, data_dict):
        if data_dict is None:
            data_dict = {}

        self._join_interval = TimeInterval(data_dict['joinInterval'])

    @property
    def join_interval(self):
        """Optional interval of a time series column being joined to another time series

           Note: not valid outside of join defintion

           :return: the interval to join to the other time series at
           :rtype: TimeInterval
        """
        return self._join_interval


class Join(object):
    """An object that represents the definition of a join within a view"""

    def __init__(self, data_dict):
        if data_dict is None:
            data_dict = {}

        self._dataset_name = data_dict.get('dataSet', {})['name']
        self._column_options = {key: ColumnOptions(value) for (key, value) in data_dict.get('columnOptions', {}).items()}
        self._joins = [Join(j) for j in data_dict.get('joins', [])]

    @property
    def dataset_name(self):
        return self._dataset_name

    @property
    def column_options(self):
        return self._column_options

    @property
    def joins(self):
        """Optional data source to be joined to this data source

        :return: list of zero or more additional joins
        :rtype: list
        """
        return self._joins


class ViewDefinition(object):
    """A description of the definition of a view"""

    def __init__(self, data_dict=None):
        if data_dict is None:
            data_dict = {}

        self._view_name = data_dict['viewName']
        self._dataset_name = data_dict['dataSetName']
        self._column_metadata = {key: ColumnMetadata(value) for (key, value) in data_dict.get('columns', {}).items()}
        self._joins = [Join(j) for j in data_dict.get('joins', [])]

    @property
    def view_name(self):
        """Gets the name of the view

        :return: the view name
        :rtype: string
        """
        return self._view_name

    @property
    def dataset_name(self):
        """Gets the dataset name that is used on the 'left' side of the join

        :return: DataSet name
        :rtype: string
        """
        return self._dataset_name

    @property
    def column_metadata(self):
        """Gets the column metadata for this View.

        :return: List of the column metadata.
        :rtype: list
        """
        return self._column_metadata

    @property
    def joins(self):
        """Gets the joins defined by this view

        :return: list of joins
        :rtype: list
        """
        return self._joins


class ViewData(ViewDefinition):
    """A view definition including the data associated with the view"""

    def __init__(self, data_dict=None):
        if data_dict is None:
            data_dict = {}
        ViewDefinition.__init__(self, data_dict)

        self._data = data_dict['data']

    @property
    def data(self):
        """Gets the data for this View.

        :return: The data as a list of dict.
        :rtype: list
        """
        return self._data
