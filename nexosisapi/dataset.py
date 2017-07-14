from nexosisapi.column_metadata import ColumnMetadata


class Dataset(object):

    def __init__(self, data_dict={}):
        """
        A Dataset is the representation of your data as stored by the Nexosis API

        :arg dict data_dict: the dictionary containing the data for this object
        """
        self._data = data_dict.get('data')
        self._metadata = {key: ColumnMetadata(value) for (key, value) in data_dict.get('metadata', {}).items()}
        self._links = data_dict.get('links')

    @property
    def data(self):
        """Gets the data for this Dataset.

        :return: The data.
        :rtype: list(dict)
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data for the Dataset.

        :param list(dict) data_type: the specified data type of the metadata
        """
        self._data = data

    @property
    def metadata(self):
        """Gets the column metadata for this Dataset.

        :return: The data.
        :rtype: list(dict)
        """
        return self._data

    @metadata.setter
    def metadata(self, metadata):
        """Sets the column metadata for the Dataset.

        :param dict(str,ColumnMetadata) metadata: a dict of ColumnMetadata keyed by column names
        """
        self._metadata = metadata

    @property
    def links(self):
        """Gets the links for this Dataset.

        :return: The links.
        :rtype: list(dict)
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links for the Dataset.

        :param list(str) links: list of string links
        """
        self._links = links
