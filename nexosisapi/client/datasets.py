from nexosisapi.dataset import Dataset
from nexosisapi.dataset_summary import DatasetSummary
from nexosisapi.paged_list import PagedList


class Datasets(object):
    """Dataset based API operations"""

    def __init__(self, base_client):
        self._client = base_client

    def create(self, dataset_name, data, metadata=None):
        """Save data in a named dataset

        :param str dataset_name: the name of the dataset
        :param list data: a `list` of `dict` where each dict is the set of values in the data set.
        :param dict metadata: a dict of `str` keys to `ColumnMetadata` items where the string key matches one
            of the keys from the entries in the data dicts

        :return: a `DatasetSummary` describing the dataset
        :rtype: DatasetSummary
        """
        return self._create(dataset_name, {'data': data, 'columns': metadata}, 'application/json')

    def create_csv(self, dataset_name, csv_file):
        """Save data from a CSV file in a named dataset

        :param str dataset_name: the name of the dataset
        :param file csv_file: an open file to read the csv data from

        :return: a `DatasetSummary` describing the dataset
        :rtype: DatasetSummary
        """
        return self._create(dataset_name, csv_file.read(), 'text/csv')

    def _create(self, dataset_name, content, content_type):
        if dataset_name is None:
            raise ValueError('dataset_name is required and was not provided')

        response = self._client.request('PUT', '/data/%s' % dataset_name, data=content,
                                        headers={'Content-Type': content_type})

        return DatasetSummary(response)

    def list(self, partial_name='', page_number=0, page_size=50):
        """Get the list of saved datasets, optionally filtering by name

        :param str partial_name:
        :return: a `list` of DatasetSummary objects representing the dataset stored
        :rtype: list
        """
        query = {
            'page': page_number,
            'pageSize': page_size,
            'partialName': partial_name}
        listing = self._client.request('GET', '/data', params=query)

        return PagedList.from_response(
            [DatasetSummary(item) for item in listing.get('items', [])],
            listing)

    def get(self, dataset_name, page_number=0, page_size=50, start_date=None, end_date=None, include=None):
        """Get the data stored in a data set

        :param str dataset_name: name of the dataset
        :param int page_number: zero-based page number of results to retrieve
        :param int page_size: count of results to retrieve in each page (default 50, max 1000).
        :param datetime start_date: the first date to return in the response
        :param datetime end_date: the last date to return in the response
        :param include: string or array of strings specifying the names of the columns from the dataset to return
        :return: a `Dataset` with the data queried
        :rtype: Dataset
        """
        if dataset_name is None:
            raise ValueError('dataset_name is required and was not provided')

        params = Datasets.process_parameters(page_number, page_size, start_date, end_date, include)

        dataset = self._client.request('GET', '/data/%s' % dataset_name, params=params)

        return Dataset(dataset)

    def get_csv(self, dataset_name, csv_file, page_number=0, page_size=50, start_date=None, end_date=None,
                include=None):
        """Get the data stored in a data set, and write it to a file

        :param str dataset_name: name of the dataset
        :param FileIO csv_file: an open, writeable text file to save the data to
        :param int page_number: zero-based page number of results to retrieve
        :param int page_size: count of results to retrieve in each page (default 50, max 1000).
        :param datetime start_date: the first date to return in the response
        :param datetime end_date: the last date to return in the response
        :param include: string or array of strings specifying the names of the columns from the dataset to return
        """
        if dataset_name is None:
            raise ValueError('dataset_name is required and was not provided')
        if csv_file is None:
            raise ValueError('csv_file is required and was not provided')

        params = Datasets.process_parameters(page_number, page_size, start_date, end_date, include)

        data = self._client.request('GET', '/data/%s' % dataset_name, params=params, headers={'Accept': 'text/csv'})

        csv_file.write(data)

    def remove(self, dataset_name, start_date=None, end_date=None, cascade=None):
        """Delete a dataset by name

        :param str dataset_name: name of the dataset
        :param datetime start_date: the starting date to remove from the dataset
        :param datetime end_date: the ending date to remove from the dataset
        :param list cascade: set the cascade options of the removal.

        The cascade list can contain 'forecast', 'session', 'view' or any
        combination of the three.
        When 'forecast' is included, all related forecasts will also be removed.
        When 'session' is included, all related sessions will also be removed.
        When 'view' is included, all related views will also be removed.
        """
        if dataset_name is None:
            raise ValueError('dataset_name is required and was not provided')

        filter_options = {}
        if start_date:
            filter_options['startDate'] = start_date
        if end_date:
            filter_options['endDate'] = end_date
        if cascade:
            filter_options['cascade'] = cascade

        self._client.request('DELETE', '/data/%s' % dataset_name, params=filter_options)

    @staticmethod
    def process_parameters(page_number, page_size, start_date, end_date, include):
        params = {'page': page_number, 'pageSize': page_size}
        if start_date is not None:
            params['startDate'] = start_date
        if end_date is not None:
            params['endDate'] = end_date
        if include is not None:
            params['include'] = include
        return params
