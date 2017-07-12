import json


class Datasets(object):
    def __init__(self, base_client):
        self._client = base_client

    def create(self, dataset_name, data, metadata=None):
        """save data in a named dataset

        :param str dataset_name: the name of the dataset
        :param list(dict) data: a list of dict's where each dict is the set of values in the data set.
        :param dict metadata: a dict of string to ColumnMetadata items where the string key matches one of the keys
            from the entries in the data dicts

        :returns DatasetSummary: information about the saved dataset
        """
        return self._create(dataset_name, json.dumps({'data': data, 'columns': metadata}), 'application/json')

    def create_csv(self, dataset_name, csv_file):
        """save data from a csv file in a named dataset

        :param str dataset_name: the name of the dataset
        :param file csv_file: an open file to read the csv data from

        :returns DatasetSummary: information about the saved dataset
        """
        return self._create(dataset_name, csv_file.read(), 'text/csv')

    def _create(self, dataset_name, content, content_type):
        if dataset_name is None:
            raise ValueError('dataset_name is required and was not provided')

        self._client.request('PUT', data=content, headers={'Content-Type': 'text/csv'})

    def list(self):
        pass

    def remove(self):
        pass
