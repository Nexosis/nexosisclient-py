from nexosisapi.time_interval import TimeInterval

class ColumnOptions(object):
    """The options defined on a specific column within a join"""

    def __init__(self, data_dict):
        if data_dict is None:
            data_dict = {}

        self._join_interval = TimeInterval[data_dict.get('joinInterval') or 'day']
        self._alias = data_dict.get('alias')

    @property
    def join_interval(self):
        """Optional interval of a time series column being joined to another time series

           Note: not valid outside of join defintion

           :return: the interval to join to the other time series at
           :rtype: TimeInterval
        """
        return self._join_interval

    @property
    def alias(self):
        """Optional alias for the column

           :return: the aliased name of the column
           :rtype: string
        """
        return self._join_interval


    def __repr__(self):
        return "{'join_interval': '%s', 'alias': '%s'}" % (self._join_interval.name, self._alias)
