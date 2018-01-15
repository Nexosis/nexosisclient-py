class FakeHttpClient(object):
    def __init__(self, return_value):
        self._return = return_value
        self._verb = None
        self._uri = None
        self._args = None

    @property
    def verb(self):
        return self._verb

    @property
    def uri(self):
        return self._uri

    @property
    def args(self):
        return self._args

    def request(self, verb, uri, **kwargs):
        self._verb = verb
        self._uri = uri
        self._args = kwargs
        return self._return

    def request_with_headers(self, verb, uri_path, **kwargs):
        return self.request(verb=verb, uri=uri_path, **kwargs), None, {}

