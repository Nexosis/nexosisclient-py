import json

from nexosisapi.dataset import Dataset
from nexosisapi.dataset_summary import DatasetSummary


class Datasets(object):
    def __init__(self, base_client):
        self._client = base_client

    def create(self, dataset_name, data, metadata=None):
        """save data in a named dataset

        :param str dataset_name: the name of the dataset
        :param list data: a :class:`list` of :class:`dict` where each dict is the set of values in the data set.
        :param dict metadata: a dict of `str` keys to :class:`ColumnMetadata` items where the string key matches one
            of the keys from the entries in the data dicts

        :return: a :class:`DatasetSummary` describing the dataset
        :rtype: DatasetSummary
        """
        return self._create(dataset_name, json.dumps({'data': data, 'columns': metadata}), 'application/json')

    def create_csv(self, dataset_name, csv_file):
        """save data from a csv file in a named dataset

        :param str dataset_name: the name of the dataset
        :param file csv_file: an open file to read the csv data from

        :return: a :class:`DatasetSummary` describing the dataset
        :rtype: DatasetSummary
        """
        return self._create(dataset_name, csv_file.read(), 'text/csv')

    def _create(self, dataset_name, content, content_type):
        if dataset_name is None:
            raise ValueError('dataset_name is required and was not provided')

        response = self._client.request('PUT', '/data/%s' % dataset_name, data=content,
                                        headers={'Content-Type': content_type})

        return DatasetSummary(response)

    def list(self, partial_name=''):
        """

        :param str partial_name:
        :return: a :class:`list` of DatasetSummary objects representing the dataset stored
        :rtype: list
        """
        listing = self._client.request('GET', '/data', params={'partialName': partial_name})
        return [DatasetSummary(item) for item in listing.get('items', [])]

    def get(self, dataset_name, page_number=0, page_size=100, start_date=None, end_date=None, include=None):
        """Get the data stored in a data set

        :param str dataset_name: name of the dataset
        :param int page_number: zero-based page number of results to retrieve
        :param int page_size: count of results to retrieve in each page (default 100, max 100).
        :param datetime start_date: the first date to return in the response
        :param datetime end_date: the last date to return in the response
        :param include: string or array of strings specifying the names of the columns from the dataset to return
        :return: a :class:`Dataset` with the data queried
        :rtype: Dataset
        """
        if dataset_name is None:
            raise ValueError('dataset_name is required and was not provided')

        params = {'page': page_number, 'pageSize': page_size}
        if start_date is not None:
            params['startDate'] = start_date
        if end_date is not None:
            params['startDate'] = end_date
        if include is not None:
            params['include'] = include

        dataset = self._client.request('GET', '/data/%s' % dataset_name, params=params)

        return Dataset(dataset)

    def get_csv(self, dataset_name, page_number=0, page_size=100, start_date=None, end_date=None, include=None):
        pass

    def remove(self, dataset_name, filter_options=None):
        self._client.request('DELETE', '/data/%s' % dataset_name, params=filter_options)
