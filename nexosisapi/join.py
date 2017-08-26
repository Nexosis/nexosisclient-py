from nexosisapi.column_options import ColumnOptions

class Join(object):
    """An object that represents the definition of a join within a view"""

    def __init__(self, data_dict):
        if data_dict is None:
            data_dict = {}
        
        ds = data_dict.get('dataSet') or {}
        cols = data_dict.get('columnOptions') or {}
        joins = data_dict.get('joins') or []

        self._dataset_name = ds['name']
        self._column_options = {key: ColumnOptions(value) for (key, value) in cols.items()}
        self._joins = [Join(j) for j in joins]

    @property
    def dataset_name(self):
        return self._dataset_name

    @property
    def column_options(self):
        return self._column_options

    @property
    def joins(self):
        """Optional data source to be joined to this data source

        :return: list of zero or more additional joins
        :rtype: list
        """
        return self._joins

    def __repr__(self):
        return """Join({
    'dataSet': {'name': '%s'},
    'columnOptions': %s,
    'joins': %s
})""" % (self.dataset_name, self.column_options, self.joins)
