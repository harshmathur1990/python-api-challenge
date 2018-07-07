import traceback
import csv

import os
import requests
import sys
from django.core.management.base import BaseCommand


base_url = 'http://127.0.0.1:8000'


def processor(response):
    return response.json()


def call_url(url, processor=None):
    response = requests.get(url)
    if processor:
        return processor(response)
    return response.json()


def dump_data_to_csv(filename, data):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as f:
        fieldnames = ['Name', 'Start Date', 'Finish Date', 'Category']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for _d in data:
            writer.writerow(_d)


def filter_data(data, category):
    _rv = list()
    for _d in data:
        if _d.get('category') == category:
            _rv.append(_d)
    return _rv


def change_keys_to_title_case(data):
    rv = list()
    for _d in data:
        _rv = dict()
        for k, v in _d.items():
            _rv[' '.join(k.split('_')).title()] = v
        rv.append(_rv)
    return rv


def fetch_data_from_api_and_create_csv(url, category, filename):
    next = True
    while next:
        data = call_url(url, processor)
        results = data.get('results')
        category_data = filter_data(results, category)
        category_data = change_keys_to_title_case(category_data)
        dump_data_to_csv(filename, category_data)
        if data.get('next'):
            next = True
            url = data.get('next')
            continue
        next = False


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = base_url + '/departures'
        try:
            fetch_data_from_api_and_create_csv(url, 'Adventurous', 'adventurous_data.csv')
        except Exception as e:
            err = traceback.format_exc()
            sys.stderr.write(err)
