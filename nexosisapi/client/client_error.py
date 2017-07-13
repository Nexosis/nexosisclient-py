class ErrorResponse(object):
    def __init__(self, body):
        self._status = body['statusCode']
        self._message = body['message']
        self._error_type = body['errorType']
        self._details = body['errorDetails']

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


class ClientError(BaseException):
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
