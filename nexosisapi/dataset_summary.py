from nexosisapi.column_metadata import ColumnMetadata


class DatasetSummary(object):
    def __init__(self, data_dict):
        self._name = data_dict['dataSetName']
        cols = data_dict.get('columns') or {}
        self._column_metadata = {key: ColumnMetadata(value) for key, value in cols.items()}

    @property
    def name(self):
        return self._name

    @property
    def column_metadata(self):
        return self._column_metadata

    def __repr__(self):
        return "Dataset({\n\
    'dataSetName': %s\n\
    'columns': %s,\n\
})" % (self._name, self._column_metadata)
