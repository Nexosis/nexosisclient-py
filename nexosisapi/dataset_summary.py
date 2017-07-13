class DatasetSummary(object):
    def __init(self, data_dict):
        self._name = data_dict['dataSetName']
        self._column_metadata = data_dict.get('columns', None)

    @property
    def name(self):
        return self._name

    @property
    def column_metadata(self):
        return self._column_metadata
