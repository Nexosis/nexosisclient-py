class CalendarJoin(object):
    def __init__(self, data_dict):
        self._name = data_dict.get('name')
        self._url = data_dict.get('url')
        self._time_zone = data_dict.get('timeZone')

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def time_zone(self):
        return self._time_zone

    def __repr__(self):
        return "CalendarJoin({'calendar':{ 'name' : '%s', 'url' : '%s', 'timeZone' : '%s'}})" % (
            self.name, self.url, self.time_zone)

    def to_hash(self):
        obj_hash = {}
        if self.name is None:
            obj_hash['url'] = self.url
        else:
            obj_hash['name'] = self.name
        if self.time_zone is not None:
            obj_hash['timeZone'] = self.time_zone
        return obj_hash
