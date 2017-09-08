from nexosisapi.column_options import ColumnOptions
from nexosisapi.calendar_join import CalendarJoin
from nexosisapi.dataset_join import DatasetJoin

class Join(object):
    """An object that represents the definition of a join within a view"""

    def __init__(self, data_dict):
        if data_dict is None:
            data_dict = {}
        
        ds = data_dict.get('dataSet')
        if(ds is not None):
            self._dataset_name = ds['name']
            self._join_target = DatasetJoin(ds)
        else:
            self._join_target = CalendarJoin(data_dict.get('calendar'))
        cols = data_dict.get('columnOptions') or {}
        joins = data_dict.get('joins') or []


        self._column_options = {key: ColumnOptions(value) for (key, value) in cols.items()}
        self._joins = [Join(j) for j in joins]

    @property
    def dataset_name(self):
        return self._dataset_name

    @property
    def join_target(self):
        return self._join_target

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
    %s,
    'columnOptions': %s,
    'joins': %s
})""" % (self.join_target, self.column_options, self.joins)

    def to_hash(self):
        if isinstance(self.join_target, DatasetJoin):
            return {'dataSet': {'name': self.join_target.name}}
        else:
            return {'calendar': self.join_target.to_hash()}
