from nexosisapi.algorithm import Algorithm

class AlgorithmContestant(object):
    def __init__(self, data_dict):
        self._id = data_dict['id']
        self._algorithm = Algorithm(data_dict['algorithm'])
        self._metrics = data_dict['metrics']
        self._links = data_dict['links']
        self._datasource_properties = data_dict['dataSourceProperties']
        self._data = data_dict.get('data',[])

    @property
    def id(self):
        return self._id

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def metrics(self):
        return self._metrics

    @property
    def links(self):
        return self._links

    @property
    def datasource_properties(self):
        return self._datasource_properties

    @property
    def data(self):
        return self._data