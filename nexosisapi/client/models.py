from nexosisapi.model_summary import ModelSummary, PredictResults
from nexosisapi.paged_list import PagedList


class Models(object):
    """Model based API operations"""

    def __init__(self, client):
        self._client = client

    def list(self, page_number=0, page_size=50, datasource_name=None, created_after=None, created_before=None):
        """Get a list of all models, optionally filtered on model properties

        :param int page_number: zero-based page number of results to retrieve
        :param int page_size: count of results to retrieve in each page (default 50, max 1000).
        :param str datasource_name: the name of the data source the model is related to
        :param datetime created_after: only include sessions requested before this date
        :param datetime created_before: only include sessions requested after this date
        """
        query = {
            'page': page_number,
            'pageSize': page_size,
            'dataSourceName': datasource_name,
            'createdBefore': created_before,
            'createdAfter': created_after,
        }
        response = self._client.request('GET', 'models', params=query)
        return PagedList.from_response(
            [ModelSummary(model) for model in response.get('items', [])],
            response)

    def get_model(self, model_id):
        """Get a model by id

        :param str model_id: the id of the model to get
        :return:
        """
        if model_id is None:
            raise ValueError('model_id is required and was not provided')

        response = self._client.request('GET', 'models/%s' % model_id)
        return ModelSummary(response)

    def predict(self, model_id, features, extra_parameters={}):
        """Predicts target values for a set of features using a model.

        :param str model_id: the id of the model to use for prediction
        :param list features: a list of dict objects with the features needed for prediction
        :param extended capability for a particular model. includeClassScores=True for classifcation models to return scores.
        :return: PredictResults
        """
        if model_id is None:
            raise ValueError('model_id is required and was not provided')

        response = self._client.request('POST', 'models/%s/predict' % model_id, data={'data': features, 'extraParameters': extra_parameters})

        return PredictResults(response)


    def remove(self, model_id):
        """Remove a model by id

        :param str model_id: the id of the model to delete
        """
        self._client.request('DELETE', 'models/%s' % model_id)

    def remove_models(self, datasource_name=None, created_after=None, created_before=None):
        """Remove models, optionally filtering on model parameters
       
        :param datasource_name: the name of the data source the model is related to
        :param created_after: only include sessions requested before this date
        :param created_before: only include sessions requested after this date
        """
        query = {
            'dataSourceName': datasource_name,
            'createdBefore': created_before,
            'createdAfter': created_after,
        }
        self._client.request('DELETE', 'models', params=query)
