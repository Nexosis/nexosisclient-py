class ErrorResponse(object):
    def __init__(self, body):
        self._status = body.get('statusCode')
        self._message = body.get('message')
        self._error_type = body.get('errorType')
        self._details = body.get('errorDetails')

    @property
    def status(self):
        return self._status

    @property
    def error_type(self):
        return self._error_type

    @property
    def message(self):
        return self._message

    @property
    def details(self):
        return self._details


class ClientError(Exception):
    def __init__(self, url, status, body):
        self._url = url
        self._status = status
        self._error_details = ErrorResponse(body)

    @property
    def url(self):
        return self._url

    @property
    def status(self):
        return self._status

    @property
    def error_details(self):
        return self._error_details
