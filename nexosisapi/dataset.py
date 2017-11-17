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
        self._page_number = data_dict['pageNumber'] if 'pageNumber' in data_dict else 0
        self._total_pages = data_dict['totalPages'] if 'totalPages' in data_dict else 0
        self._page_size = data_dict['pageSize'] if 'pageSize' in data_dict else 50
        self._item_total = data_dict['totalCount'] if 'totalCount' in data_dict else 0

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

        :return: A list of ColumnMetadata.
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

    @property
    def page_number(self):
        return self._page_number

    @page_number.setter
    def page_number(self, value):
        self._page_number = value

    @property
    def total_pages(self):
        return self._total_pages

    @total_pages.setter
    def total_pages(self, value):
        self._total_pages = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        self._page_size = value

    @property
    def item_total(self):
        return self._item_total

    @item_total.setter
    def item_total(self, value):
        self._item_total = value

    def __repr__(self):
        return """Dataset({\n\
    'metadata': %s,
    'data': %s,
    'links': %s,
    'page_number': %s,
    'total_pages': %s,
    'page_size': %s,
    'item_total': %s
    
})""" % (self._metadata, self._data, self._links, self.page_number, self.total_pages, self.page_size, self.item_total)
