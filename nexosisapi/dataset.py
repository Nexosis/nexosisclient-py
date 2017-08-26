from nexosisapi.column_metadata import ColumnMetadata


class Dataset(object):
    def __init__(self, data_dict=None):
        """
        A Dataset is the representation of your data as stored by the Nexosis API

        :arg dict data_dict: the dictionary containing the data for this object
        """
        if data_dict is None:
            data_dict = {}
        self._data = data_dict.get('data')
        self._metadata = {key: ColumnMetadata(value) for (key, value) in data_dict.get('columns', {}).items()}
        self._links = data_dict.get('links')

    @property
    def data(self):
        """Gets the data for this Dataset.

        :return: The data as a list of dict.
        :rtype: list
        """
        return self._data

    @property
    def metadata(self):
        """Gets the column metadata for this Dataset.

        :return: A list of :class:nexosisapi.ColumnMetadata.
        :rtype: list
        """
        return self._metadata

    @property
    def links(self):
        """Gets the links for this Dataset.

        :return: A list of dict where each dict contains a link
        :rtype: list
        """
        return self._links

    def __repr__(self):
        return """Dataset({\n\
    'metadata': %s,
    'data': %s,
    'links': %s
})""" % (self._metadata, self._data, self._links)
