from nexosisapi.paged_list import PagedList
from nexosisapi.view_definition import ViewDefinition, ViewData, Join


class Views(object):
    """View based API operations"""

    def __init__(self, client):
        self._client = client

    def list(self, partial_name='', dataset_name='', page_number=0, page_size=50):
        """Get the list of saved views, optionally filtering by view and/or dataset name

        :param str partial_name: optional name to filter view names on
        :param str dataset_name: optional filter to limit views based on dataset name
        :param int page_number: optional zero-based page number of results to retrieve
        :param int page_size: optional count of results to retrieve in each page (default 50, max 1000).
        :return: a `list` of ViewDefinition objects representing the views stored
        :rtype: list
        """
        listing = self._client.request('GET', '/views',
                                       params={'partialName': partial_name, 'dataSetName': dataset_name,
                                               'page': page_number, 'pageSize': page_size})
        return PagedList.from_response(
            [ViewDefinition(item) for item in listing.get('items', [])],
            listing)

    def create(self, name, dataset_name, right_datasource_name):
        """Create a view or update an existing one by name

        :returns: the processed configuration of the view
        :rtype: ViewDefinition 
        """
        if name is None:
            raise ValueError('name is required to create a view')
        if dataset_name is None:
            raise ValueError('dataset_name must be given to create a view definition')
        if right_datasource_name is None:
            raise ValueError('right_datasource_name must be given to create a view definition')

        view = ViewDefinition({
            'viewName': name,
            'dataSetName': dataset_name,
            'joins': [{'dataSet': {'name': right_datasource_name}}]
        })

        return self.create_by_definition(view)

    def create_by_definition(self, view_definition):
        """Create a view or update an existing one by name

        :param ViewDefinition view_definition: a ViewDefinition object populated with the configuration of the view

        :returns: the processed configuration of the view
        :rtype: ViewDefinition
        """
        if view_definition is None:
            raise ValueError('a view defintion must be given to create a view')

        view_name = view_definition.view_name
        if view_name is None:
            raise ValueError('a view definition must give the view a name')

        response = self._client.request('PUT', '/views/%s' % view_name, data=view_definition)
        return ViewDefinition(response)

    def get(self, view_name, page_number=0, page_size=50, start_date=None, end_date=None, include=None):
        """Get a specific view and the data resulting in running the view

        :param str view_name: the view name to pull data from
        :param int page_number: optional zero-based page number of results to retrieve
        :param int page_size: optional count of results to retrieve in each page (default 50, max 1000).
        :param datetime start_date: optional first date to return in the response
        :param datetime end_date: optional last date to return in the response
        :param include: optional string or array of strings specifying the names of the columns from the dataset to return

        :returns: A ViewData object describing the view and the data resulting from running the view
        :rtype: ViewData
        """
        if view_name is None:
            raise ValueError('a view definition must give the view a name')

        params = {'page': page_number, 'pageSize': page_size}
        if start_date is not None:
            params['startDate'] = start_date
        if end_date is not None:
            params['endDate'] = end_date
        if include is not None:
            params['include'] = include

        response = self._client.request('GET', '/views/%s' % view_name, params=params)

        return ViewData(response)

    def remove(self, view_name, cascade=None):
        """Remove a view by name

        :param str view_name: the view name to pull data from
        :param object cascade: include this parameter to also remove the sessions associated with the view when removing the view
        """
        if view_name is None:
            raise ValueError('a view name must be provided to know which one to remove')

        params = {}

        if cascade is not None:
            params = {'cascade': 'sessions'}

        self._client.request('DELETE', 'views/%s' % view_name, params=params)
