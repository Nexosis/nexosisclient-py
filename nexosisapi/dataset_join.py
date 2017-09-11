class DatasetJoin(object):
    """An object that represents the definition of a join target within a join"""

    def __init__(self, data_dict):
        self._name = data_dict.get('name')

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return "DatasetJoin({'dataSet' : { 'name':'%s'}})" % self.name
