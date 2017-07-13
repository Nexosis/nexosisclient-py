from datetime import datetime, date
import json
import requests

from .client_error import ClientError


class HttpClient(object):
    def __init__(self, key, uri):
        self._key = key
        self._uri = uri

    @staticmethod
    def _json_serial(obj):
        """JSON serializer for datetime since it is not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type %s not serializable" % type(obj))

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

        # transform data to json using our serializer
        if 'data' in args and args['headers']['Content-Type'] == 'application/json':
            args['json'] = json.dumps(args['data'], default=HttpClient._json_serial)
            del args['data']

        return args

    # should be a better way to do this?
    def request(self, verb, uri_path, **kwargs):
        response = requests.request(verb, self._get_uri(uri_path), **self._process_args(kwargs))
        if response.ok:
            return response.json()
        else:
            error = response.json(default=HttpClient._json_serial)
            raise ClientError(uri_path, response.status_code, error)
