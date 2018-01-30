from nexosisapi.data_source_type import DataSourceType
import dateutil.parser

class VocabularySummary(object):
    """Summary information about a Vocabulary"""

    def __init__(self, data_dict=None):
        if data_dict is None:
            data_dict = {}

        self._id = data_dict.get('id', None)
        self._data_source_name = data_dict.get('dataSourceName', None)
        self._column_name = data_dict.get('columnName', None)
        self._data_source_type = DataSourceType[data_dict.get('dataSourceType', 'dataSet')]
        self._created_on_date = dateutil.parser.parse(data_dict.get('createdOnDate', None))
        self._created_by_session_id = data_dict.get('createdBySessionId', None)



    @property
    def id(self):
        """The id of the Vocabulary

        :return: the vocabulary id
        :rtype: string
        """
        return self._id

    @property
    def data_source_name(self):
        """The name of the data source from which the vocabulary was built

        :return: the data source name
        :rtype: string
        """
        return self._data_source_name

    @property
    def column_name(self):
        """The name of the column in the data source from which the vocabulary was built

        :return: the column name
        :rtype: string
        """
        return self._column_name

    @property
    def data_source_type(self):
        """The type of the data source (DataSource or View) from which the vocabulary was built

        :return: the data source type
        :rtype: DataSourceType
        """
        return self._data_source_type

    @property
    def created_on_date(self):
        """The datetime that the vocabulary was created

        :return: the created on date
        :rtype: string
        """
        return self._created_on_date

    @property
    def created_by_session_id(self):
        """The session id that generated the vocabulary

        :return: the session id
        :rtype: string
        """
        return self._created_by_session_id
