import os
import sys
import tempfile
import unittest
from datetime import datetime
import csv

from nexosisapi import Client, ClientError
from nexosisapi.view_definition import ViewDefinition
from nexosisapi.calendar_join import CalendarJoin

class ViewsIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"],
                                  uri=os.environ["NEXOSIS_API_TESTURI"])
        self.ds_name = "data-%s" % datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.ds_name_right = 'right-' + self.ds_name

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/data.csv')) as f:
            csv_data = csv.DictReader(f)
            self.data = [dict(d) for d in csv_data]

        try:
            self.test_client.datasets.get(self.ds_name)
        except ClientError as error:
            if error.status == 404:
                self.test_client.datasets.create(self.ds_name, self.data)
            else:
                raise

        try:
            self.test_client.datasets.get(self.ds_name_right)
        except ClientError as error:
            if error.status == 404:
                self.test_client.datasets.create(self.ds_name_right, self.data)
            else:
                raise

    def tearDown(self):
        try:
            self.test_client.views.remove("alpha-beta-mike")
            self.test_client.datasets.remove(self.ds_name, cascade="view")
            self.test_client.datasets.remove(self.ds_name_right)
        except ClientError as error:
            sys.stderr.write(error)

    def test_create_view(self):
        self.test_client.views.create('alpha-beta-mike', self.ds_name, self.ds_name_right)

    def test_delete_view(self):
        self.test_client.views.create('alpha-beta-mike', self.ds_name, self.ds_name_right)

        self.test_client.views.remove('alpha-beta-mike')

        try:
            self.test_client.views.get('alpha-beta-mike')
        except ClientError as error:
            self.assertEqual(404, error.status)

    def test_list_views(self):
        self.test_client.views.create('alpha-beta-mike', self.ds_name, self.ds_name_right)

        views = self.test_client.views.list(partial_name='alpha-beta-mike')

        self.assertEqual(1, len(views))
        self.assertEqual('alpha-beta-mike', views[0].view_name)

    def test_get_view(self):
        view_data = self.test_client.views.create('alpha-beta-mike', self.ds_name, self.ds_name_right)

        self.assertEqual('alpha-beta-mike', view_data.view_name)
        self.assertEqual(self.ds_name, view_data.dataset_name)

    def test_add_with_named_calendar(self):
        view_def = ViewDefinition({'viewName': 'testPyView', 'dataSetName': self.ds_name, 'joins': [{'calendar': {'name': 'Nexosis.Holidays-US'}}]})
        created_view = self.test_client.views.create_by_definition(view_def)
        self.assertIsNotNone(created_view)
        self.assertIsInstance(created_view.joins[0].join_target, CalendarJoin)

    def test_add_with_url_calendar(self):
        iCal_url = 'https://calendar.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics'
        view_def = ViewDefinition({'viewName': 'testPyViewiCal', 'dataSetName': self.ds_name,
                                   'joins': [{'calendar': {'url': iCal_url}}]})
        created_view = self.test_client.views.create_by_definition(view_def)
        self.assertIsNotNone(created_view)
        self.assertEqual(iCal_url,created_view.joins[0].join_target.url)
