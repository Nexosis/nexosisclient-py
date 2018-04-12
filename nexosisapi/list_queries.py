from nexosisapi.sort_order import SortOrder
import datetime
from dateutil.parser import parse


class ListQuery(object):

    def __init__(self, page_number=0, page_size=50, sort_order=SortOrder.ASC, sort_by=None):
        """
         :param page_number: page number, defaults to 0
         :param page_size: number of items per page, defaults to 50; 1000 max.
         :param sort_order: direction of sorted value if any. Defaults to ASC
         :param sort_by: a string value mapped to a property of the list type. See specific query type for details.
        """
        self._page_number = page_number
        self._page_size = page_size
        self._sort_order = sort_order
        self._sort_by = sort_by

    @property
    def page_number(self):
        return self._page_number

    @page_number.setter
    def page_number(self, value):
        self._page_number = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        self._page_size = value

    @property
    def sort_order(self):
        return self._sort_order

    @sort_order.setter
    def sort_order(self, value):
        self._sort_order = value

    @property
    def sort_by(self):
        return self._sort_by

    @sort_by.setter
    def sort_by(self, value):
        self._sort_by = value

    def __base_parameters__(self):
        query = {}
        if self.page_number is not None:
            query.update({'page': self.page_number})
        if self.page_size is not None:
            query.update({'pageSize': self.page_size})
        if self._sort_by is not None:
            query.update({'sortBy': self._sort_by})
            query.update({'sortOrder': self.sort_order.name})
        return query

    @staticmethod
    def __assert_valid_sort__(sort_value, *valid_keys):
        if sort_value is None:
            return
        if sort_value not in valid_keys:
            raise ValueError("The sort_by value {0} is not valid for this list query type.".format(sort_value))

    @staticmethod
    def __convert_date_field__(candidate_value):
        if candidate_value is None:
            return None
        elif type(candidate_value) is str:
            try:
                return parse(candidate_value)
            except ValueError:
                return None
        return candidate_value


class DatasetListQuery(ListQuery):
    """
    ..note:: sort by properties include dataSetName, dataSetSize, rowCount, dateCreated, and lastModified
    """

    def __init__(self, page_number=0, page_size=50, sort_order=SortOrder.ASC, sort_by=None, partial_name=None):
        ListQuery.__assert_valid_sort__(sort_by, 'dataSetName', 'dataSetSize', 'rowCount', 'dateCreated',
                                        'lastModified')
        super(DatasetListQuery, self).__init__(page_number, page_size, sort_order, sort_by)
        self._partial_name = partial_name

    @property
    def partial_name(self):
        return self._partial_name

    @partial_name.setter
    def partial_name(self, value):
        self._partial_name = value

    def query_parameters(self):
        query = {}
        if self.partial_name is not None:
            query.update({'partialName': self.partial_name})
        query.update(self.__base_parameters__())
        return query


class SessionListQuery(ListQuery):
    """
    ..note:: sort by properties include id, name, type, status, dataSourceName, and requestedDate
    """

    def __init__(self, page_number=0, page_size=50, sort_order=SortOrder.ASC, sort_by=None, options={}):
        """
        :param options: query options from one or more of the following:
            - str datasource_name: the name of the data source the session is related to
            - str event_name: filter on the event name given when running an impact analysis
            - datetime requested_before: only include sessions requested before this date
            - datetime requested_after: only include sessions requested after this date
            - SessionType session_type: filter on the type of session
        """
        ListQuery.__assert_valid_sort__(sort_by, 'id', 'name', 'type', 'status', 'dataSourceName', 'requestedDate')
        super(SessionListQuery, self).__init__(page_number, page_size, sort_order, sort_by)
        self._datasource_name = options.get('datasource_name')
        self._event_name = options.get('event_name')
        self._model_id = options.get('model_id')
        self._requested_after_date = ListQuery.__convert_date_field__(options.get('requested_after_date'))
        self._requested_before_date = ListQuery.__convert_date_field__(options.get('requested_before_date'))
        self._session_type = options.get('session_type')

    @property
    def datasource_name(self):
        return self._datasource_name

    @datasource_name.setter
    def datasource_name(self, value):
        self._datasource_name = value

    @property
    def event_name(self):
        return self._event_name

    @event_name.setter
    def event_name(self, value):
        self._event_name = value

    @property
    def model_id(self):
        return self._model_id

    @model_id.setter
    def model_id(self, value):
        self._model_id = value

    @property
    def requested_after_date(self):
        return self._requested_after_date

    @requested_after_date.setter
    def requested_after_date(self, value):
        self._requested_after_date = value

    @property
    def requested_before_date(self):
        return self._requested_before_date

    @requested_before_date.setter
    def requested_before_date(self, value):
        self._requested_before_date = value

    @property
    def session_type(self):
        return self._session_type

    def query_parameters(self):
        query = {}
        if self.datasource_name is not None:
            query.update({'dataSourceName': self.datasource_name})
        if self.event_name is not None:
            query.update({'eventName': self.event_name})
        if self.model_id is not None:
            query.update({'modelId': self.model_id})
        if self.requested_after_date is not None:
            query.update({'requestedAfterDate': self.requested_after_date.strftime('%FT%T%z')})
        if self.requested_before_date is not None:
            query.update({'requestedBeforeDate': self.requested_before_date.strftime('%FT%T%z')})
        if self.session_type is not None:
            query.update({'sessionType': self.session_type})
        query.update(self.__base_parameters__())
        return query


class ModelListQuery(ListQuery):
    """
        ..note:: sort by properties include id, modelName, dataSourceName, type, createdDate, and lastUsedDate
    """

    def __init__(self, page_number=0, page_size=50, sort_order=SortOrder.ASC, sort_by=None, options={}):
        ListQuery.__assert_valid_sort__(sort_by, 'id', 'modelName', 'dataSourceName', 'type', 'createdDate',
                                        'lastUsedDate')
        super(ModelListQuery, self).__init__(page_number, page_size, sort_order, sort_by)
        self._datasource_name = options.get('datasource_name')
        self._created_after_date = ListQuery.__convert_date_field__(options.get('created_after_date'))
        self._created_before_date = ListQuery.__convert_date_field__(options.get('created_before_date'))

    @property
    def datasource_name(self):
        return self._datasource_name

    @datasource_name.setter
    def datasource_name(self, value):
        self._datasource_name = value

    @property
    def created_after_date(self):
        return self._created_after_date

    @created_after_date.setter
    def created_after_date(self, value):
        self._created_after_date = value

    @property
    def created_before_date(self):
        return self._created_before_date

    @created_before_date.setter
    def created_before_date(self, value):
        self._created_before_date = value

    def query_parameters(self):
        query = {}
        if self.datasource_name is not None:
            query.update({'dataSourceName': self.datasource_name})
        if self.created_after_date is not None:
            query.update({'createdAfterDate': self.created_after_date.strftime('%FT%T%z')})
        if self.created_before_date is not None:
            query.update({'createdBeforeDate': self.created_before_date.strftime('%FT%T%z')})
        query.update(self.__base_parameters__())
        return query


class ImportListQuery(ListQuery):
    """
       ..note:: sort by properties include id, dataSetName, requestedDate, and currentStatusDate
    """

    def __init__(self, page_number=0, page_size=50, sort_order=SortOrder.ASC, sort_by=None, options={}):
        ListQuery.__assert_valid_sort__(sort_by, 'id', 'dataSetName', 'requestedDate', 'currentStatusDate')
        super(ImportListQuery, self).__init__(page_number, page_size, sort_order, sort_by)
        self._dataset_name = options.get('dataset_name')
        self._requested_after_date = ListQuery.__convert_date_field__(options.get('requested_after_date'))
        self._requested_before_date = ListQuery.__convert_date_field__(options.get('requested_before_date'))

    @property
    def dataset_name(self):
        return self._dataset_name

    @dataset_name.setter
    def dataset_name(self, value):
        self._dataset_name = value

    @property
    def requested_after_date(self):
        return self._requested_after_date

    @requested_after_date.setter
    def requested_after_date(self, value):
        self._requested_after_date = value

    @property
    def requested_before_date(self):
        return self._requested_before_date

    @requested_before_date.setter
    def requested_before_date(self, value):
        self._requested_before_date = value

    def query_parameters(self):
        query = {}
        if self.dataset_name is not None:
            query.update({'dataSetName': self.dataset_name})
        if self.requested_after_date is not None:
            query.update({'requestedAfterDate': self.requested_after_date.strftime('%FT%T%z')})
        if self.requested_before_date is not None:
            query.update({'requestedBeforeDate': self.requested_before_date.strftime('%FT%T%z')})
        query.update(self.__base_parameters__())
        return query
