import os
import tempfile
import unittest
from datetime import datetime
import csv

from nexosisapi import Client, ClientError
from nexosisapi.column_metadata import ColumnMetadata, ColumnType, Role, Imputation, Aggregation


class DatasetsIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.test_client = Client(key=os.environ["NEXOSIS_API_TESTKEY"],
                                  uri=os.environ["NEXOSIS_API_TESTURI"])
        self.ds_name = "data-%s" % datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/data.csv')) as f:
            csv_data = csv.DictReader(f)
            self.data = [dict(d) for d in csv_data]

    def tearDown(self):
        try:
            self.test_client.datasets.remove(self.ds_name)
        except ClientError:
            pass

    def test_create(self):
        result = self.test_client.datasets.create(self.ds_name, self.data)

        self.assertEqual(self.ds_name, result.name)
        self.assertEqual(ColumnType.numeric, result.column_metadata['observed'].data_type)
        self.assertEqual(Role.target, result.column_metadata['observed'].role)
        self.assertEqual(ColumnType.date, result.column_metadata['timestamp'].data_type)
        self.assertEqual(Role.timestamp, result.column_metadata['timestamp'].role)

    def test_create_with_measure_type(self):
        metadata = {'observed': ColumnMetadata({'dataType': 'numericMeasure', 'role': 'target'}),
                    'timestamp': ColumnMetadata({'dataType': 'date', 'role': 'timestamp'})}
        result = self.test_client.datasets.create(self.ds_name, self.data, metadata)

        self.assertEqual(Imputation.mean, result.column_metadata['observed'].imputation)
        self.assertEqual(Aggregation.mean, result.column_metadata['observed'].aggregation)

    def test_create_with_metadata(self):
        metadata = {'observed': ColumnMetadata({'dataType': 'string', 'role': 'none'}),
                    'timestamp': ColumnMetadata({'dataType': 'date', 'role': 'timestamp'})}
        result = self.test_client.datasets.create(self.ds_name, self.data, metadata)

        self.assertEqual(self.ds_name, result.name)
        self.assertEqual(metadata['observed'].data_type, result.column_metadata['observed'].data_type)
        self.assertEqual(metadata['observed'].role, result.column_metadata['observed'].role)
        self.assertEqual(metadata['timestamp'].data_type, result.column_metadata['timestamp'].data_type)
        self.assertEqual(metadata['timestamp'].role, result.column_metadata['timestamp'].role)

    def test_create_assign_imputation_aggregation(self):
        metadata = {'observed': ColumnMetadata({'dataType': 'numeric', 'role': 'target', 'imputation' : 'mode', 'aggregation' : 'median'}),
                    'timestamp': ColumnMetadata({'dataType': 'date', 'role': 'timestamp'})}

        result = self.test_client.datasets.create(self.ds_name, self.data, metadata)

        self.assertEqual(self.ds_name, result.name)
        self.assertEqual(Aggregation.median, result.column_metadata['observed'].aggregation)
        self.assertEqual(Imputation.mode, result.column_metadata['observed'].imputation)


    def test_create_adding_data_adds_more_data(self):
        # initial data added, items 0-9
        self.test_client.datasets.create(self.ds_name, self.data[0:10])
        result_first = self.test_client.datasets.get(self.ds_name)
        self.assertEqual(10, len(result_first.data))

        # more data added, items 10-end
        self.test_client.datasets.create(self.ds_name, self.data[10:])

        result = self.test_client.datasets.get(self.ds_name, page_size=1000)

        # make sure the saved data has extended the initial data upload to the full data set
        self.assertEqual(len(self.data), len(result.data))

    def test_create_from_csv(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/data.csv')) as f:
            result = self.test_client.datasets.create_csv(self.ds_name, f)

        self.assertEqual(self.ds_name, result.name)

        check = self.test_client.datasets.get(self.ds_name, page_size=1000)
        self.assertEqual(len(self.data), len(check.data))

    def test_list_datasets(self):
        self.test_client.datasets.create(self.ds_name, self.data)

        ds_list = self.test_client.datasets.list()

        self.assertIn(self.ds_name, map(lambda x: x.name, ds_list))

    def test_list_with_filtering(self):
        self.test_client.datasets.create(self.ds_name, self.data)

        ds_list = self.test_client.datasets.list(self.ds_name[:10])

        self.assertIn(self.ds_name, [x.name for x in ds_list])

    def test_get(self):
        self.test_client.datasets.create(self.ds_name, self.data)

        dataset = self.test_client.datasets.get(self.ds_name, page_size=1000)

        def sorter(d): return d['timestamp']

        self.assertListEqual(sorted(self.data, key=sorter), sorted(dataset.data, key=sorter))

        self.assertEqual(dataset.metadata['observed'].data_type, ColumnType.numeric)
        self.assertEqual(dataset.metadata['observed'].role, Role.target)
        self.assertEqual(dataset.metadata['observed'].imputation, Imputation.zeroes)
        self.assertEqual(dataset.metadata['observed'].aggregation, Aggregation.sum)
        self.assertEqual(dataset.metadata['timestamp'].data_type, ColumnType.date)
        self.assertEqual(dataset.metadata['timestamp'].role, Role.timestamp)

    def test_get_filtered(self):
        self.test_client.datasets.create(self.ds_name, self.data)

        dataset = self.test_client.datasets.get(self.ds_name,
                                                start_date=datetime.strptime('2008-06-01', '%Y-%m-%d'),
                                                end_date=datetime.strptime('2008-06-30', '%Y-%m-%d'))

        self.assertEqual(30, len(dataset.data))

    def test_get_as_csv(self):
        self.test_client.datasets.create(self.ds_name, self.data)

        temp_file = os.path.join(tempfile.gettempdir(),
                                 '%s%s.tmp' % (tempfile.gettempprefix(), datetime.now().strftime('%f')))

        with open(temp_file, 'wb') as f:
            self.test_client.datasets.get_csv(self.ds_name, f, page_size=1000)

        with open(temp_file, 'r') as f:
            # the +1 is for the headers written to the file
            self.assertEqual(len(self.data) + 1, len(f.readlines()))

        os.remove(temp_file)

    def test_remove(self):
        self.test_client.datasets.create(self.ds_name, self.data)

        self.test_client.datasets.remove(self.ds_name)

        try:
            self.test_client.datasets.get(self.ds_name)
        except ClientError as e:
            self.assertEqual(404, e.status)
        else:
            self.assertFalse(True, 'expected ClientError for data set that does not exist')

    def test_remove_some_data(self):
        self.test_client.datasets.create(self.ds_name, self.data)

        self.test_client.datasets.remove(self.ds_name, end_date=datetime.strptime('2008-06-30', '%Y-%m-%d'))

        partial = self.test_client.datasets.get(self.ds_name, page_size=1000)
        self.assertEqual(len(self.data) - 30, len(partial.data))
