from datetime import datetime, date
import json
import requests

from enum import Enum
from nexosisapi.column_metadata import ColumnMetadata
from .client_error import ClientError


def _process_response(response):
    if len(response.content) == 0:
        return None

    # content type is probably something like 'application/json; charset: utf-8', so this processes that
    content_type_value = response.headers['content-type']
    content_type = content_type_value.split(';')[0]

    if content_type == 'application/json':
        return response.json()
    else:
        return response.content


def _json_encode(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, ColumnMetadata):
        return {'dataType': obj.data_type, 'role': obj.role}
    if isinstance(obj, Enum):
        return obj.name
    raise TypeError("Type %s not serializable" % type(obj))


class HttpClient(object):
    def __init__(self, key, uri):
        self._key = key
        self._uri = uri

    def _generate_headers(self):
        return {
            'api-key': self._key,
            'User-Agent': 'Nexosis-Python-API-Client/1.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def _get_uri(self, fragment):
        return '%s/%s' % (self._uri, fragment)

    def _process_args(self, args):
        # if headers specified, then generate defaults and update with the ones specified
        # or just set them if none specified
        default_headers = self._generate_headers()
        if 'headers' in args:
            user_headers = args['headers']
            args['headers'] = default_headers
            args['headers'].update(user_headers)
        else:
            args['headers'] = default_headers

        # copy data to json for proper serialization
        if 'data' in args and args['headers']['Content-Type'] == 'application/json':
            args['data'] = json.dumps(args['data'], default=_json_encode)

        return args

    # TODO: should be a better way to do this re: the 'verb' argument
    def request(self, verb, uri_path, **kwargs):
        response = requests.request(verb, self._get_uri(uri_path), **self._process_args(kwargs))
        if response.ok:
            return _process_response(response)
        else:
            error = response.json()
            raise ClientError(uri_path, response.status_code, error)
