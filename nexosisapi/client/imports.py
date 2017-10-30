from nexosisapi.import_response import ImportResponse
from nexosisapi.paged_list import PagedList


class Imports(object):
    def __init__(self, client):
        self._client = client

    def list(self, page_number=0, page_size=50):
        query = {
            'page': page_number,
            'pageSize': page_size}
        response = self._client.request('GET', '/imports', params=query)
        return PagedList.from_response(
            [ImportResponse(r) for r in response.get('items', [])],
            response)

    def import_from_s3(self, dataset_name, bucket_name, path, region='us-east-1', metadata=None):
        if dataset_name is None:
            raise ValueError('dataset_name is required and was not provided')
        if bucket_name is None:
            raise ValueError('bucket_name is required and was not provided')
        if path is None:
            raise ValueError('path is required and was not provided')

        body = {
            'dataSetName': dataset_name,
            'bucket': bucket_name,
            'path': path,
            'region': region,
            'columns': metadata
        }
        response = self._client.request('POST', '/imports/s3', data=body)

        return ImportResponse(response)

    def get(self, import_id):
        if import_id is None:
            raise ValueError('import_id is required and was not provided')

        response = self._client.request('GET', '/imports/%s' % import_id)
        return ImportResponse(response)
