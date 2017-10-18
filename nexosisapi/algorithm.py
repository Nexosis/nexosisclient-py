class Algorithm(object):
    """A description of the algorithm used to generate results"""
    def __init__(self, data_dict=None):
        if data_dict is None:
            data_dict = {}

        self._name = data_dict.get('name')
        self._desc = data_dict.get('description')
        self._key = data_dict.get('key')

    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def key(self):
        return self._key

    def __repr__(self):
        return "Algorithm({'key': %s, 'name': %s, 'description': %s}" % (self._key, self._name, self._desc)