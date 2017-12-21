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

    def import_from_s3(self, dataset_name, bucket_name, path, region='us-east-1', creds = None, metadata=None):
        """
        Import a json or csv file (optionally g-zipped) from AWS S3 as a dataset
        :param dataset_name: name of the resulting dataset
        :param bucket_name: s3 bucket
        :param path: path to object within bucket
        :param region: location of the bucket within AWS
        :param metadata: column metadata to apply to the dataset
        :param creds: an optional dict of AWS IAM accesKeyId and secretAccessKey values.
        :return: a response object which includes the unique importId you can use to check on status.
        """
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
        if creds is not None:
            body.update(creds)

        response = self._client.request('POST', '/imports/s3', data=body)

        return ImportResponse(response)


    def import_from_azure(self, dataset_name, connection_string, container, blob, metadata=None):
        """
        Import a json or csv file (optionally g-zipped) from Azure storage as a dataset
        :param dataset_name: name of the resulting dataset
        :param connection_string: azure connection string for resource
        :param container: the name of the storage container
        :param blob: path to the blob. Inlude any folders within the container.
        :param metadata: column metadata to apply to the dataset
        :return: a response object which includes the unique importId you can use to check on status.
        """
        if dataset_name is None or not dataset_name:
            raise ValueError('dataset_name is required and was not provided')
        if connection_string is None or not connection_string:
            raise ValueError('connection_string is required and was not provided')
        if container is None:
            raise ValueError('container is required and was not provided')
        if blob is None:
            raise ValueError('blob is required and was not provided')

        body = {
            'dataSetName': dataset_name,
            'connectionString': connection_string,
            'container': container,
            'blob': blob,
            'columns': metadata
        }
        response = self._client.request('POST', '/imports/azure', data=body)
        return ImportResponse(response)

    def import_from_url(self, dataset_name, url, content_type=None):
        """
        Import a json or csv file (optionally g-zipped) from a url as a dataset
        :param dataset_name: name of the resulting dataset
        :param url: the location to access the file contents
        :param content_type: optional indicator of 'json' or 'csv' if the type cannot be inferred.
        :return: a response object which includes the unique importId you can use to check on status.
        """
        if dataset_name is None or not dataset_name:
            raise ValueError('dataset_name is required and was not provided')
        if url is None or not url:
            raise ValueError('url is required and was not provided')
        if content_type != 'json' and content_type != 'csv':
            content_type = None
        body = {
            'dataSetName': dataset_name,
            'url': url
        }
        if content_type is not None:
            body['contentType'] = content_type
        response = self._client.request('POST','/imports/url', data=body)

    def get(self, import_id):
        if import_id is None:
            raise ValueError('import_id is required and was not provided')

        response = self._client.request('GET', '/imports/%s' % import_id)
        return ImportResponse(response)
