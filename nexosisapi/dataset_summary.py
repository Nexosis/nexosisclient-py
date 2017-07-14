from nexosisapi.column_metadata import ColumnMetadata


class DatasetSummary(object):
    def __init__(self, data_dict):
        self._name = data_dict['dataSetName']
        self._column_metadata = {key: ColumnMetadata(value) for key, value in data_dict.get('columns', {}).items()}

    @property
    def name(self):
        return self._name

    @property
    def column_metadata(self):
        return self._column_metadata
