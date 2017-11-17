import csv
import os
import unittest

from nose.tools import nottest

from nexosisapi import ClientError


def all():
    path = os.path.dirname(os.path.realpath(__file__))
    return unittest.defaultTestLoader.discover(path)

@nottest
def build_test_dataset(test_client, file, dataset_name):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file)) as f:
        csv_data = csv.DictReader(f)
        data = [dict(d) for d in csv_data]
    try:
        test_client.datasets.get(dataset_name)
    except ClientError as e:
        if e.status == 404:
            test_client.datasets.create(dataset_name, data)
        else:
            raise
    return data
