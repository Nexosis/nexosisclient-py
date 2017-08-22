from nexosisapi.column_metadata import ColumnMetadata
from nexosisapi.join import Join

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
