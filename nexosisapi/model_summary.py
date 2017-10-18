from nexosisapi.algorithm import Algorithm
from nexosisapi.column_metadata import ColumnMetadata


class ModelSummary(object):
    def __init__(self, data_dict=None):
        if data_dict is None:
            data_dict = {}

        self._model_id = data_dict.get('modelId')
        self._prediction_domain = data_dict.get('predictionDomain')
        self._datasource_name = data_dict.get('dataSourceName')
        self._created_on = data_dict.get('createdDate')
        self._algorithm = Algorithm(data_dict.get('algorithm'))
        cols = data_dict.get('columns') or {}
        self._column_metadata = {key: ColumnMetadata(value) for key, value in cols.items()}
        self._metrics = data_dict.get('metrics')

    @property
    def model_id(self):
        return self._model_id

    @property
    def prediction_domain(self):
        return self._prediction_domain

    @property
    def datasource_name(self):
        return self._datasource_name

    @property
    def created_on(self):
        return self._created_on

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def column_metadata(self):
        return self._column_metadata

    @property
    def metrics(self):
        return self._metrics

    def __repr__(self):
        return """PredictResults({'modelId': '%s', 'predictionDomain': '%s', 'dataSourceName': '%s', 'createdOn': '%s', 'algorithm': '%s', 'columnMetadata': %s, 'metrics': %s}""" % (
            self._model_id,
            self._prediction_domain,
            self._datasource_name,
            self._created_on,
            self._algorithm,
            self._column_metadata,
            self._metrics
        )


class PredictResults(ModelSummary):
    def __init__(self, data_dict=None):
        if data_dict is None:
            data_dict = {}

        ModelSummary.__init__(self, data_dict)

        self._data = data_dict.get('data')

    @property
    def data(self):
        return self._data

    def __repr__(self):
        return """PredictResults({'modelId': '%s', 'predictionDomain': '%s', 'dataSourceName': '%s', 'createdOn': '%s', 'algorithm': '%s', 'columnMetadata': %s, 'metrics': %s
            data: %s}""" % (
            self._model_id,
            self._prediction_domain,
            self._datasource_name,
            self._created_on,
            self._algorithm,
            self._column_metadata,
            self._metrics,
            self._data
        )

