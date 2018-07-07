import csv
import os
import requests


def processor(response):
    return response.json()


def get_call(url, processor=None):
    response = requests.get(url)
    if processor:
        return processor(response)
    return response.json()


def dump_data_to_csv(filename, data, fieldnames):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for _d in data:
            writer.writerow(_d)


def change_dict_keys_to_title_case(data):
    rv = list()
    for _d in data:
        _rv = dict()
        for k, v in _d.items():
            _rv[' '.join(k.split('_')).title()] = v
        rv.append(_rv)
    return rv
