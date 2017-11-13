class Link(object):
    def __init__(self, rel, href):
        self._rel = rel
        self._href = href

    @property
    def rel(self):
        return self._rel

    @rel.setter
    def rel(self, value):
        self._rel = value

    @property
    def href(self):
        return self._href

    @href.setter
    def href(self, value):
        self._href = value

