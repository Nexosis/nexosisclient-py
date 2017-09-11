import unittest
import json
from nexosisapi.view_definition import ViewDefinition
from nexosisapi.join import Join


class ViewModelUnitTests(unittest.TestCase):

    def test_can_parse_hash(self):
        view_def = ViewDefinition(
            {'viewName': 'testPyView', 'dataSetName': 'testDataset', 'joins': [{"calendar": {"name": "TestCalendar"}}]})
        self.assertEqual("TestCalendar", view_def.joins[0].join_target.name)

    def test_named_calendar_join_outputs_json(self):
        named_join_def = Join({"calendar": {"name": "TestCalendar"}})
        actual = json.dumps(named_join_def.to_hash())
        self.assertEqual('{"calendar": {"name": "TestCalendar"}}', actual)

    def test_url_calendar_join_outputs_json(self):
        url_join_def = Join({'calendar': {'url': 'http://example.com/mycal.ical'}})
        actual = json.dumps(url_join_def.to_hash())
        self.assertEqual('{"calendar": {"url": "http://example.com/mycal.ical"}}',actual)

    def test_cal_with_tz_outputs_json(self):
        tz_join_def = Join({'calendar': {'name': 'TestCalendar', 'timeZone': 'Americas/New_York'}})
        actual = json.dumps(tz_join_def.to_hash(), sort_keys=True)
        self.assertEqual('{"calendar": {"name": "TestCalendar", "timeZone": "Americas/New_York"}}', actual)