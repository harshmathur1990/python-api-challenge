import csv
import os
import requests
import sys


def processor(response):
    if response.ok:
        return response.json()
    else:
        sys.stdout.write('Requests Error, Status Code: {}, Response Body: {}\n'.format(response.status_code, response.text))
        sys.exit(1)


def get_call(url, response_processor=None):
    try:
        response = requests.get(url)
        if response_processor:
            return response_processor(response)
        return response.json()
    except requests.exceptions.Timeout:
        sys.stderr.write('url: {} timed out\n'.format(url))
        sys.exit(1)
    except requests.exceptions.TooManyRedirects:
        sys.stderr.write('url: {} Too many redirects\n'.format(url))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        sys.stderr.write(str(e)+'\n')
        sys.exit(1)


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
